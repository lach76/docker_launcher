#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Docker Control APIs

import os
import json
import urllib2
import subprocess

START_PORT_NO = 6000
class TDockerContainer:
    def __init__(self, registry_url, host_ip_addr):
        self.registry_url = registry_url
        self.host_ip_addr = host_ip_addr
        self.refreshContainerInfo()

    def refreshContainerInfo(self):
        repositories = self.read_registry(self.registry_url)
        containers = self.read_container()

        used_port_list = self.get_container_port(containers)

        self.registry_image = {}
        for registry in repositories.keys():
            image_list = repositories[registry]
            for image_name in image_list:
                recommend_name = self.get_container_name(image_name)
                recommend_port = self.get_container_port(recommend_name, containers)
                status = self.get_container_status(recommend_name, containers)
                int_ip = self.get_container_internalip(recommend_name, containers)

                if recommend_port is None:
                    recommend_port, used_port_list = self.get_recommend_port(used_port_list, START_PORT_NO)

                ext_ip = "%s:%s" % (self.host_ip_addr, recommend_port)
                self.registry_image[image_name] = {'container_name':recommend_name, 'container_port':recommend_port, 'status' : status, 'internal_ip':int_ip, 'expose_ip':ext_ip}

    def get_host_ip_addr(self):
        return self.host_ip_addr

    def get_container_info(self, image_name):
        return self.registry_image[image_name]

    def get_container_image_list(self):
        return self.registry_image.keys()

    def get_container_name(self, image_name):
        return image_name.split('/')[-1].replace(':', '-')

    def get_container_port(self, containers, container_name = None, protocol = '22/tcp'):
        if container_name is None:
            results = []
            for container_name, container_info in containers.iteritems():
                try:
                    results.append(self.get_port(container_info[3], protocol))
                except:
                    continue
        else:
            try:
                results = self.get_port(containers[container_name][3], protocol)
            except:
                results = None

        return results

    def get_port(self, container_dict_network, protocol):
        return container_dict_network[protocol]['HostPort']

    def get_container_status(self, container_name, containers):
        result = ''
        try:
            result = containers[container_name][0]
        except:
            result = 'not running'

        return result

    def get_container_internalip(self, container_name, containers):
        result = ''
        try:
            result = containers[container_name][2]
        except:
            result = '0.0.0.0'

        return result

    def get_recommend_port(self, used_port_list, start_port):
        for port in range(start_port, start_port + 100):
            port = str(port)
            if port not in used_port_list:
                used_port_list.append(port)
                return port, used_port_list

        return None, used_port_list

    def read_registry(self, url):
        catalog_url = os.path.join(*[url, 'v2', '_catalog'])
        catalog = json.loads(urllib2.urlopen(catalog_url).read())
        if not catalog.has_key('repositories'):
            return {}

        repositories = {}
        for repo in catalog['repositories']:
            repositories[repo] = []
            tags_url = os.path.join(*[url, 'v2', repo, 'tags', 'list'])
            tags = json.loads(urllib2.urlopen(tags_url).read())
            if tags.has_key('tags'):
                for tag in tags['tags']:
                    image_name = os.path.join(*[url, repo]) + ':%s' % tag
                    image_name = image_name.replace('http://', '')  # remove protocol
                    repositories[repo].append(image_name)

        return repositories

    def read_container(self):
        output = subprocess.check_output('docker ps --format "{{.Names}}" -a', shell = True)
        lines = output.splitlines()
        if len(lines) == 0:
            return {}

        output = subprocess.check_output('docker inspect %s' % ' '.join(lines), shell = True)
        run_image_list = json.loads(output)
        run_images = {}
        for image in run_image_list:
            name = image['Name'][1:]
            status = image['State']['Status']
            imagename = image['Config']['Image']
            internalipaddr = image['NetworkSettings']['Networks']['bridge']['IPAddress']
            exposeports = image['Config']['ExposedPorts']
            for key, value in exposeports.iteritems():
                if image['HostConfig']['PortBindings'] is not None:
                    exposeports[key] = image['HostConfig']['PortBindings'][key][0]

            run_images[name] = [status, imagename, internalipaddr, exposeports]

        return run_images
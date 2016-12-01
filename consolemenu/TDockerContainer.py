#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Docker Control APIs

import os
import json
import urllib2
import subprocess
import time

START_PORT_NO = 6000
class TDockerContainer:
    def __init__(self, registry_url, host_ip_addr, cmd_prefix = ''):
        self.registry_url = registry_url
        self.host_ip_addr = host_ip_addr
        self.cmd_prefix = cmd_prefix
        self.used_port_list = []
        self.repo = {}
        self.refreshContainerInfo()

    def get_registry_url(self):
        return self.registry_url

    def getNewPort(self):
        for new_port in range(START_PORT_NO, START_PORT_NO + 100):
            if new_port in self.used_port_list:
                continue
            else:
                break

        return new_port

    def getRepo(self):
        return self.repo

    def getContainerNameFromImageName(self, image_name):
        containerName = image_name.split('/')[-1]
        return containerName.replace(":",".") + ".%d" % int(time.time())

    def refreshContainerInfo(self):
        # get image list from registry
        # repositories[repo] = [imagename1, ....]
        self.used_port_list = []
        repositories = self.readRegistry(self.registry_url)

        # get loaded container info
        # container[container_name] = [status, imageName, internalIpAddr, exposePorts]
        containers = self.readContainer()

        registry = {}
        for key, value in repositories.iteritems():
            for image_tag in value:
                registry[image_tag] = {}
            registry['undefined'] = {}

        for container_name, value in containers.iteritems():
            container_image_name = value[1]
            if not registry.has_key(container_image_name):
                container_image_name = 'undefined'
            status = value[0]
            internalIp = value[2]
            exposePort = self.getPort(value[3], "22/tcp")

            if exposePort < START_PORT_NO:
                exposePort = self.getNewPort()
            self.used_port_list.append(exposePort)

            registry[container_image_name][container_name] = {"imagename":value[1], "status":status, "internalIp":internalIp, "exposePort":exposePort}

        repo = {}
        for key, value in repositories.iteritems():
            repo[key] = {}
            for imagename in value:
                repo[key][imagename] = registry[imagename]

        self.repo = repo

    def getPort(self, container_dict_network, protocol):
        try:
            return int(container_dict_network[protocol]['HostPort'])
        except:
            return 0

    def readRegistry(self, url):
        catalog_url = url + "/v2/_catalog"
        catalog = json.loads(urllib2.urlopen(catalog_url).read())
        if not catalog.has_key('repositories'):
            return {}

        #print("Get Local Registry Image List : [%s]" % catalog_url)
        repositories = {}
        for repo in catalog['repositories']:
            repositories[repo] = []
            tags_url = url + "/v2/" + repo + "/tags/list"
            tags = json.loads(urllib2.urlopen(tags_url, timeout=5).read())

            #print("  - repo : [%s]" % repo)
            if tags.has_key('tags'):
                for tag in tags['tags']:
                    image_name = os.path.join(*[url, repo]) + ':%s' % tag
                    image_name = image_name.replace('http://', '')  # remove protocol
                    #print("    * image : [%s]" % image_name)
                    repositories[repo].append(image_name)

        return repositories

    def readContainer(self):
        output = subprocess.check_output(self.cmd_prefix + 'docker ps --format "{{.Names}}" -a', shell = True)
        lines = output.splitlines()
        if len(lines) == 0:
            return {}

        run_images = {}
        for image_name in lines:
            output = subprocess.check_output(self.cmd_prefix + 'docker inspect %s' % image_name, shell=True)
            json_output = json.loads(output)
            if len(json_output) < 1:
                continue
            inspect_result = json_output[0]

            name = image_name
            status = inspect_result['State']['Status']
            imageName = inspect_result['Config']['Image']
            internalIpAddr = inspect_result['NetworkSettings']['Networks']['bridge']['IPAddress']
            exposePorts = {}
            if inspect_result['Config'].has_key('ExposedPorts'):
                exposePorts = inspect_result['Config']['ExposedPorts']
                for key, value in exposePorts.iteritems():
                    if inspect_result['HostConfig']['PortBindings'] is not None:
                        exposePorts[key] = inspect_result['HostConfig']['PortBindings'][key][0]

            run_images[name] = [status, imageName, internalIpAddr, exposePorts]

        return run_images

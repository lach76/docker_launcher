#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Registry의 이미지를 사용하는 Container는 하나의 VM에 하나만 있다고 가정

import time
import curses
import os
import urllib2
import json
import socket

import TDockerContainer

MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"
SKIP = 'skip'
ADM_COMMAND = "admcommand"

def get_title_str(container_info, display = True):
    container_name = container_info['container_name']
    if display:
        if container_name.endswith('-latest'):
            container_name = container_name.replace('-latest', '')
        else:
            container_tags = container_name.split('-')[-1]
            count = container_tags.count('.')
            container_name = '  ' + '  ' * count + '- ' + container_name

    return '%s - (%s) [%s]' % (container_name, container_info['expose_ip'], container_info['status'])

# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent):
      # work out what text to display as the last menu option
    if parent is None:
        lastoption = "Go to shell"
    else:
        lastoption = "Return to previous menu"

    optioncount = len(menu['options']) # how many options in this menu

    pos=0 #pos is the zero-based index of the hightlighted menu option. Every time runmenu is called, position returns to 0, when runmenu ends the position is returned and tells the program what opt$
    oldpos=None # used to prevent the screen being redrawn every time
    x = None #control for while loop, let's you scroll through options until return key is pressed then returns pos to program

    # Loop until return key is pressed
    while x !=ord('\n'):
        if pos != oldpos:
            oldpos = pos
            screen.border(0)

            if menu.has_key('title'):
                title = menu['title']
            else:
                container_info = DockerContainers.get_container_info(menu['image_name'])
                title = get_title_str(container_info, display = False)

            screen.addstr(2,2, title, curses.A_STANDOUT) # Title for this menu
            screen.addstr(4,2, menu['subtitle'], curses.A_BOLD) #Subtitle for this menu

            # Display all the menu items, showing the 'pos' item highlighted
            for index in range(optioncount):
                textstyle = normalcolor
                if pos==index:
                    textstyle = highlight

                if menu['options'][index].has_key('image_name'):
                    image_name = menu['options'][index]['image_name']
                    container_info = DockerContainers.get_container_info(image_name)
                    if container_info['status'].startswith('run'):
                        textstyle = textstyle + curses.A_BOLD

                if menu['options'][index].has_key('title'):
                    title = menu['options'][index]['title']
                else:
                    title = get_title_str(container_info)

                screen.addstr(6+index,4, "* " + title, textstyle)

            # Now display Exit/Return at bottom of menu
            textstyle = normalcolor
            if pos==optioncount:
                textstyle = highlight
            screen.addstr(7+optioncount,4, "* %s" % (lastoption), textstyle)
            screen.refresh()
            # finished updating screen

        x = screen.getch() # Gets user input

        # What is user input?
        #if x >= ord('1') and x <= ord(str(optioncount+1)):
        #  pos = x - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
        if x == 258: # down arrow
            if pos < optioncount:
                pos += 1
            else: pos = 0
        elif x == 259: # up arrow
            if pos > 0:
                pos += -1
            else: pos = optioncount

    # return index of the selected item
    return pos

def go_shell_mode():
    curses.def_prog_mode()
    exec_command('reset')

def go_curses_mode():
    screen.clear()
    curses.reset_prog_mode()
    curses.curs_set(0)

# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent=None):
    optioncount = len(menu['options'])
    exitmenu = False
    while not exitmenu: #Loop until the user exits the menu
        getin = runmenu(menu, parent)
        if getin == optioncount:
            exitmenu = True
        elif menu['options'][getin]['type'] == ADM_COMMAND:
            # Get Input from User
            screen.clear()
            screen.border(0)
            screen.addstr(2, 2, menu['options'][getin]['subtitle'])
            screen.refresh()
            curses.echo()
            curses.curs_set(1)
            input = screen.getstr(10, 10, 60)
            curses.curs_set(0)
            curses.noecho()

            go_shell_mode()

            exec_command('sudo %s %s' % (menu['options'][getin]['command'], input))
            exec_command('echo "Now Build Containers are restarting..."')
            exec_command('sudo service docker restart')

            go_curses_mode()
            pass

        elif menu['options'][getin]['type'] == COMMAND:
            image_name = menu['options'][getin]['image_name']
            container_info = DockerContainers.get_container_info(image_name)
            if menu['options'][getin]['cmd_name'] == 'start':
                go_shell_mode()
                container_name = container_info['container_name']
                docker_image_name = image_name
                cmd_port = '-p %s:22' % container_info['container_port']
                cmd_share = '-v /home:/home:rw -v /nfsroot:/nfsroot:rw -v /tftpboot:/tftpboot:rw -v /opt:/opt:rw -v /etc:/.tetc:ro'
                cmd_images = '--name %s %s' % (container_name, docker_image_name)

                command = 'docker run -d -P --restart=always %s %s %s' % (cmd_port, cmd_share, cmd_images)
                exec_command(command)
                go_curses_mode()

            elif menu['options'][getin]['cmd_name'] == 'stop':
                go_shell_mode()
                container_name = container_info['container_name']
                exec_command('docker stop %s' % container_name)
                exec_command('docker rm %s' % container_name)
                go_curses_mode()

            elif menu['options'][getin]['cmd_name'] == 'remove':
                # just add .deleted in tag name
                screen.clear()
                screen.border(0)
                screen.addstr(2, 2, "Image Name : [%s]" % container_info['container_real_name'])
                screen.addstr(4, 4, "Remove it? (yes / no)")
                curses.curs_set(1)
                curses.echo()
                input = screen.getstr(4, 26, 4)
                curses.curs_set(0)
                curses.noecho()
                input.lower()
                if input != 'yes':
                    screen.clear()
                    continue

                go_shell_mode()
                print 'not implemented yet...'
                #remove image : %s' % container_info['container_real_name']
                #exit()
                #container_name = container_info['container_name']
                go_curses_mode()

                pass

            elif menu['options'][getin]['cmd_name'] == 'restart':
                go_shell_mode()
                container_name = container_info['container_name']
                exec_command('docker restart %s' % container_name)
                go_curses_mode()

            elif menu['options'][getin]['cmd_name'] == 'connect':
                go_shell_mode()
                home = os.path.expanduser("~")
                command = 'ssh-keygen -f "%s/.ssh/known_hosts" -R %s' % (home, container_info['internal_ip'])
                exec_command(command)
                command = 'ssh -o StrictHostKeyChecking=no %s' % container_info['internal_ip']
                exec_command(command)
                go_curses_mode()

            elif menu['options'][getin]['cmd_name'] == 'commit':
                # Get Input from User
                screen.clear()
                screen.border(0)
                screen.addstr(2, 2, "Input the name of build environments")
                screen.addstr(4, 2, "    ex > distribution.version.dev:platform.tag")
                screen.addstr(5, 2, "         ubuntu.12.04.dev:octo2x")
                screen.addstr(5, 2, "         ubuntu.12.04.dev:octo2x.wine")
                screen.refresh()
                curses.echo()
                container_basename = container_info['container_name']
                container_realname = container_info['container_real_name']
                screen.addstr(10, 10, container_realname + '.')

                tag_index = len(container_realname) + 1#container_realname.index(':') + 1
                curses.curs_set(1)
                input = '.' + screen.getstr(10, 10 + tag_index, 20)

                container_tag_name = container_realname + input

                reg_url = DockerContainers.get_registry_url()
                reg_url = reg_url.replace('http://', '')
                container_tag_name = os.path.join(reg_url, container_tag_name)

                txt = "    Do you really want to commit image? (yes/no) "
                screen.addstr(12, 2, txt)
                input = screen.getstr(12, 2 + len(txt))

                curses.curs_set(0)
                curses.noecho()

                if input != 'yes':
                    screen.clear()
                    continue

                go_shell_mode()

                # Stop and Remove Docker container
                command = 'docker stop %s' % container_basename
                exec_command(command)

                # commit
                command = 'docker commit %s %s' % (container_basename, container_tag_name)
                exec_command(command)

                # remove container
                command = 'docker rm %s' % container_basename
                exec_command(command)

                # push container
                command = 'docker push %s' % container_tag_name
                exec_command(command)

                go_curses_mode()

            DockerContainers.refreshContainerInfo()
            make_container_list()

        elif menu['options'][getin]['type'] == MENU:
                screen.clear() #clears previous screen on key press and updates display based on pos
                processmenu(menu['options'][getin], menu) # display the submenu
                optioncount = len(menu['options'])
                screen.clear() #clears previous screen on key press and updates display based on pos
        elif menu['options'][getin]['type'] == EXITMENU:
                exitmenu = True

def exec_command(command):
    #print command
    os.system(command)

def get_interface_ip(ifname):
    import fcntl
    import struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127."):
        interfaces = ["eth0", "eth1", "eth2", "wlan0", "wlan1", "wifi0", "ath0", "ath1", "ppp0", "enp4s0"]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip

def get_default_options(image_name):
    return [
        {'title':'-------------------------------------', 'type':SKIP, 'image_name':image_name},
        {'title':'Connect', 'type':COMMAND, 'cmd_name':'connect', 'image_name':image_name}
    ]

def get_default_options_adm(image_name):
    return [
        {'title':'-------------------------------------', 'type':SKIP, 'image_name':image_name},
        {'title':'Start', 'type':COMMAND, 'cmd_name':'start', 'image_name':image_name},
        {'title':'Stop', 'type':COMMAND, 'cmd_name':'stop', 'image_name':image_name},
        {'title':'Restart', 'type':COMMAND, 'cmd_name':'restart', 'image_name':image_name},
        {'title':'Remove Image', 'type':COMMAND, 'cmd_name':'remove', 'image_name':image_name},
        {'title':'Commit Image', 'type':COMMAND, 'cmd_name':'commit', 'image_name':image_name},
        {'title':'-------------------------------------', 'type':SKIP, 'image_name':image_name},
        {'title':'Connect', 'type':COMMAND, 'cmd_name':'connect', 'image_name':image_name}
    ]

menu_data_base = {
  'title': "Development Environment Launcher", 'type':MENU, 'subtitle':'Please select an options....',
  'options':[]
}

def make_container_list():
    options = []
    container_image_list = DockerContainers.get_container_image_list()
    container_image_list.sort()
    for image in container_image_list:
        container_info = DockerContainers.get_container_info(image)
        if current_user in admin_user_list:
            sub_options = get_default_options_adm(image)
        else:
            sub_options = get_default_options(image)

        data = {'image_name':image, 'type':MENU, 'subtitle':'Start / Stop / Connect Build Environment. Select it', 'options':sub_options}
        options.append(data)

    run_path = os.path.dirname( os.path.abspath( __file__ ) )
    admin_options = [
        {'title':'Add User', 'subtitle':'Add User - Enter User Name', 'type':ADM_COMMAND, 'command':os.path.join(run_path, 'add_user.sh')},
        {'title':'Remove User', 'subtitle':'Remove User - Enter User Name', 'type':ADM_COMMAND, 'command':os.path.join(run_path, 'remove_user.sh')},
        {'title':'-------------------------------------', 'subtitle':'', 'type':SKIP}
    ]

    skip_options = [
        {'title':'-------------------------------------', 'type':SKIP}
    ]

    logout_options = [
    ]

    menu_data_base['title'] = "Development Environment Config Manager - [%s]" % current_user
    if current_user in admin_user_list:
        menu_data_base['options'] = skip_options + admin_options + options + skip_options + logout_options
    else:
        menu_data_base['options'] = skip_options + options

if __name__ == '__main__':
    import getpass

    admin_user_list = ['humax', 'kimjh']
    current_user = getpass.getuser()
    host_ip_address = get_lan_ip()

    if current_user not in admin_user_list:
        docker_prefix = 'sudo '
    else:
        docker_prefix = ''
    # load docker repository and get current running info
    DockerContainers = TDockerContainer.TDockerContainer('http://10.0.218.196:5000', host_ip_address, docker_prefix)
    make_container_list()

    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad(1)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    highlight = curses.color_pair(1)
    normalcolor = curses.A_NORMAL
    runcolor = curses.color_pair(2)

    processmenu(menu_data_base)

    curses.endwin()
    os.system('clear')

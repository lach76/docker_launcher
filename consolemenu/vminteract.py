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

def get_title_str(container_info):
    return '%s - (%s) [%s]' % (container_info['container_name'], container_info['expose_ip'], container_info['status'])

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
                title = get_title_str(container_info)

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
            input = screen.getstr(10, 10, 60)
            curses.noecho()

            curses.def_prog_mode()    # save curent curses environment
            os.system('reset')

            os.system('sudo %s %s' % (menu['options'][getin]['command'], input))
            os.system('echo "Now Build Containers are restarting..."')
            os.system('sudo service docker restart')

            screen.clear() #clears previous screen
            curses.reset_prog_mode()   # reset to 'current' curses environment
            curses.curs_set(1)         # reset doesn't do this right
            curses.curs_set(0)
            pass

        elif menu['options'][getin]['type'] == COMMAND:
            curses.def_prog_mode()    # save curent curses environment
            os.system('reset')

            if menu['options'][getin]['title'] == 'Log-Out':
                os.system('exit')
                exit()

            image_name = menu['options'][getin]['image_name']
            container_info = DockerContainers.get_container_info(image_name)
            if menu['options'][getin]['title'] == 'Start':
                container_name = container_info['container_name']
                docker_image_name = image_name
                cmd_port = '-p %s:22' % container_info['container_port']
                cmd_share = '-v /home:/home -v /nfsroot:/nfsroot -v /tftpboot:/tftpboot -v /opt:/opt -v /etc:/.tetc'
                cmd_images = '--name %s %s' % (container_name, docker_image_name)

                command = 'docker run -d -P --restart=always %s %s %s' % (cmd_port, cmd_share, cmd_images)
                os.system(command)

            elif menu['options'][getin]['title'] == 'Stop':
                container_name = container_info['container_name']
                os.system('docker stop %s' % container_name)
                os.system('docker rm %s' % container_name)

            elif menu['options'][getin]['title'] == 'Restart':
                container_name = container_info['container_name']
                os.system('docker restart %s' % container_name)

            elif menu['options'][getin]['title'] == 'Connect':
                home = os.path.expanduser("~")
                command = 'ssh-keygen -f "%s/.ssh/known_hosts" -R %s' % (home, container_info['internal_ip'])
                os.system(command)
                command = 'ssh -o StrictHostKeyChecking=no %s' % container_info['internal_ip']
                os.system(command)

            DockerContainers.refreshContainerInfo()
            screen.clear() #clears previous screen

            curses.reset_prog_mode()   # reset to 'current' curses environment
            curses.curs_set(1)         # reset doesn't do this right
            curses.curs_set(0)
        elif menu['options'][getin]['type'] == MENU:
                screen.clear() #clears previous screen on key press and updates display based on pos
                processmenu(menu['options'][getin], menu) # display the submenu
                screen.clear() #clears previous screen on key press and updates display based on pos
        elif menu['options'][getin]['type'] == EXITMENU:
                exitmenu = True

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
    {'title':'Connect', 'type':COMMAND, 'image_name':image_name},
    ]

def get_default_options_adm(image_name):
    return [
    {'title':'-------------------------------------', 'type':SKIP, 'image_name':image_name},
    {'title':'Start', 'type':COMMAND, 'image_name':image_name},
    {'title':'Stop', 'type':COMMAND, 'image_name':image_name},
    {'title':'Restart', 'type':COMMAND, 'image_name':image_name},
    {'title':'Connect', 'type':COMMAND, 'image_name':image_name}
    ]

menu_data_base = {
  'title': "Development Environment Launcher", 'type':MENU, 'subtitle':'Please select an options....',
  'options':[]
}

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
        {'title':'Log-Out', 'type':COMMAND, 'command':''}
    ]

    menu_data_base['title'] = "Development Environment Config Manager - [%s]" % current_user
    if current_user in admin_user_list:
        menu_data_base['options'] = skip_options + admin_options + options + skip_options + logout_options
    else:
        menu_data_base['options'] = skip_options + options

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

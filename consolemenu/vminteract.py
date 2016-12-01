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

ITEMTYPE_REPO="repo"
ITEMTYPE_TAG="tag"
ITEMTYPE_CONTAINER="container"

ITEMTYPE_ADDUSER="adduser"
ITEMTYPE_REMOVEUSER="removeuser"
ITEMTYPE_CONTAINER_CONNECT="connect"
ITEMTYPE_REPO_START="start"
ITEMTYPE_REPO_STOP="stop"
ITEMTYPE_REPO_RESTART="restart"
ITEMTYPE_CONTAINER_REMOVE="remove"
ITEMTYPE_CONTAINER_COMMIT="commit"
ITEMTYPE_REPO_TAGGING="tagging"

def get_title_str(container_info, display = True):
    container_name = container_info['container_name']
    if display:
        container_name = container_name.replace('-latest', '')
        """
        if container_name.endswith('-latest'):
            container_name = container_name.replace('-latest', '')
        else:
            container_tags = container_name.split('-')[-1]
            count = container_tags.count('.')
            container_name = '  ' + '  ' * count + '- ' + container_name
        """

    return '%s - (%s) [%s]' % (container_name, container_info['expose_ip'], container_info['status'])

def getTitleString(menu):
    if menu.has_key('depth'):
        depth = menu['depth']
    else:
        depth = 0

    running_flag = False
    detailInfo = ""
    if menu.has_key('container_info'):
        running_string = "not running"
        container_info = menu['container_info']
        if container_info['status'] == 'running':
            running_flag = True
            running_string = "running"
        internalIp = container_info['internalIp']
        exposePort = container_info['exposePort']

        detailInfo = " - %s [%s - %s:%d]" % (running_string, internalIp, host_ip_address, exposePort)

    return "  " * depth + menu['title'] + detailInfo, running_flag

def findNearestIndex(menuList, tIndex, tIncre):
    menuCount = len(menuList)
    while True:
        tIndex = (tIndex + tIncre) % menuCount
        try:
            if menuList[tIndex]['type'] == SKIP:
                continue
            else:
                break
        except:
            break

    return tIndex

ITEM_START_ROW = 6
# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent):
    displayMenuList = []
    # work out what text to display as the last menu option
    displayMenuList.append({"title": "---------------------------------------------------------------------", "type": SKIP})
    if parent is None:
        displayMenuList.append({"title": "Go to shell", "type":EXITMENU})
    else:
        displayMenuList.append({"title": "Return to previous menu", "type":EXITMENU})

    # display title
    screen.addstr(2, 2, menu['title'], curses.A_STANDOUT)
    screen.addstr(4, 4, menu['subtitle'], curses.A_BOLD)

    menulist = menu['options'] + displayMenuList

    # set default position
    cur_pos = findNearestIndex(menulist, 0, 1)
    input = None

    while input != ord('\n'):   # loop until Enter key pressed
        screen.border(0)
        skip_pos_list = []
        for index, menuitem in enumerate(menulist):
            skipflag = False
            try:
                if menuitem['type'] == SKIP:
                    skipflag = True
            except:
                skipflag = False

            if skipflag:
                skip_pos_list.append(index)

            textstyle = normalcolor
            if cur_pos == index:
                textstyle = highlight

            title, running = getTitleString(menuitem)
            if running:
                textstyle += curses.A_BOLD
            screen.addstr(ITEM_START_ROW + index, 4, "* " + title, textstyle)

        screen.refresh()

        input = screen.getch()
        if input == 258:    # arrow_down
            cur_pos = findNearestIndex(menulist, cur_pos, 1)
        elif input == 259:      # arrow_up
            cur_pos = findNearestIndex(menulist, cur_pos, -1)

    return cur_pos, menulist[cur_pos]

def go_shell_mode():
    curses.def_prog_mode()
    exec_command(['reset'])

def go_curses_mode():
    screen.clear()
    curses.reset_prog_mode()
    curses.curs_set(0)

def getMenuList(itemInfo):
    subMenu = {
        "title":"Managing %s" % itemInfo['title'],
        "target":itemInfo['title'],
        "containerInfo":None,
        "type":MENU,
        "subtitle":"Start / Stop / Connect / Rebuild Development Environments",
        "options":[
        ]
    }

    submenuTagAdmin = [
        {'title': '---------------------------------------------------------------------', 'type': SKIP},
        {'title': 'Start Container', 'type': COMMAND, 'itemtype': ITEMTYPE_REPO_START},
        {'title': 'Remove Image', 'type': COMMAND, 'itemtype': ITEMTYPE_CONTAINER_REMOVE}
    ]
    submenuContainer = [
        {'title': '---------------------------------------------------------------------', 'type': SKIP},
        {'title': 'Connect', 'type': COMMAND, 'itemtype':ITEMTYPE_CONTAINER_CONNECT},
    ]
    submenuContainerAdmin = [
        {'title': '---------------------------------------------------------------------', 'type': SKIP},
        {'title': 'Restart Container', 'type': COMMAND, 'itemtype': ITEMTYPE_REPO_RESTART},
        {'title': 'Stop Container', 'type': COMMAND, 'itemtype': ITEMTYPE_REPO_STOP},
        {'title': 'Commit Container Image', 'type': COMMAND, 'itemtype': ITEMTYPE_CONTAINER_COMMIT}
    ]

    # data = {"itemtype": ITEMTYPE_CONTAINER, "title": reg_container_name, "depth": 2, "type": MENU, "container_info": reg_container_info}
    # container[container_name] = [status, imageName, internalIpAddr, exposePorts]
    itemType = itemInfo['itemtype']
    if itemType == ITEMTYPE_REPO:
        return None

    if itemType == ITEMTYPE_TAG:
        if isAdminUser():
            subMenu['options'].extend(submenuTagAdmin)
        else:
            return None

    if itemType == ITEMTYPE_CONTAINER:
        subMenu['container_info'] = itemInfo['container_info']
        subMenu['options'].extend(submenuContainer)
        if isAdminUser():
            subMenu['options'].extend(submenuContainerAdmin)

    return subMenu

def isAdminUser():
    adminList = ['humax', 'kimjh']
    if getpass.getuser() in adminList:
        return True

    return False

def startContainer(itemInfo):
    global DockerContainers

    image_name = itemInfo['target'] # image name
    expose_port = DockerContainers.getNewPort()
    container_name = DockerContainers.getContainerNameFromImageName(image_name)

    cmd_port = '-p %s:22' % expose_port
    cmd_share = '-v /home:/home:rw -v /nfsroot:/nfsroot:rw -v /tftpboot:/tftpboot:rw -v /opt:/opt:rw -v /etc:/.tetc:ro'
    cmd_images = '--name %s %s' % (container_name, image_name)

    command = 'docker run -d -P --restart=always %s %s %s' % (cmd_port, cmd_share, cmd_images)

    exec_command([command], itemInfo = itemInfo)
    pass

def stopContainer(itemInfo):
    commandList = []
    commandList.append('docker stop %s' % itemInfo['target'])
    commandList.append('docker rm %s' % itemInfo['target'])
    exec_command(commandList, itemInfo = itemInfo)


def restartContainer(itemInfo):
    exec_command(['docker restart %s' % itemInfo['target']], itemInfo = itemInfo)

def removeContainer(itemInfo):
    screen.addstr(itemInfo['itemrow'], 6, "Now Supported!!!")
    screen.refresh()
    time.sleep(1)
    screen.clear()

def connectContainer(itemInfo):
    container_info = itemInfo['container_info']

    home = os.path.expanduser("~")

    commandList = []
    command = 'ssh-keygen -f "%s/.ssh/known_hosts" -R %s' % (home, container_info['internalIp'])
    commandList.append(command)
    command = 'ssh -o StrictHostKeyChecking=no %s' % container_info['internalIp']
    commandList.append(command)
    exec_command(commandList, True, itemInfo = itemInfo)

def commitContainer(itemInfo):
    containerInfo = itemInfo['container_info']
    dockerImageName = containerInfo['imagename']
    queryString = "Input the name of container : %s" % dockerImageName
    curPos = queryString.rfind(':')
    if (curPos > 0):
        screen.addstr(itemInfo['itemrow'], 6, queryString)
        curses.echo()
        curses.curs_set(1)
        tagName = screen.getstr(itemInfo['itemrow'], 6 + curPos + 1, 10)
        newDockerImageName = dockerImageName[:dockerImageName.rfind(':') + 1] + tagName
        curses.curs_set(0)
        curses.noecho()

        commandList = []
        command = 'docker stop %s' % itemInfo['target']
        commandList.append(command)
        command = 'docker commit %s %s' % (itemInfo['target'], newDockerImageName)
        commandList.append(command)
        command = 'docker rm %s' % itemInfo['target']
        commandList.append(command)
        command = 'docker push %s' % newDockerImageName
        commandList.append(command)
        exec_command(commandList, itemInfo = itemInfo)

CommandList = {
    ITEMTYPE_REPO_START:   startContainer,
    ITEMTYPE_REPO_STOP:    stopContainer,
    ITEMTYPE_REPO_RESTART: restartContainer,
    ITEMTYPE_CONTAINER_REMOVE: removeContainer,
    ITEMTYPE_CONTAINER_CONNECT: connectContainer,
    ITEMTYPE_CONTAINER_COMMIT: commitContainer
}


def runCommandWithTarget(item_row, targetName, itemInfo, container_info):
    itemType = itemInfo['itemtype']
    if CommandList.has_key(itemType):
        CommandList[itemType]({"itemrow":item_row, "target":targetName, "info":itemInfo, "container_info":container_info})
        pass
    else:
        screen.addstr(item_row, 6, "Unknown command....")
        screen.refresh()
        time.sleep(1)
        screen.clear()

def runCommand(item_row, itemInfo):
    itemType = itemInfo['itemtype']
    if itemType in [ITEMTYPE_ADDUSER, ITEMTYPE_REMOVEUSER]:
        screen.addstr(item_row, 6, "NOT SUPPORTED!!!!")
        screen.refresh()
        time.sleep(1)
        screen.clear()

# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent=None):
    exitmenu = False

    while not exitmenu: #Loop until the user exits the menu
        if parent is None:
            # reload main menu tree (for container updates)
            menu = makeMenuTrees()

        menu_index, itemInfo = runmenu(menu, parent)
        menu_type = itemInfo['type']
        if menu_type == EXITMENU:
            exitmenu = True
        elif menu_type == MENU:
            screen.clear()
            subMenu = getMenuList(itemInfo)

            screen.clear()
            processmenu(subMenu, menu)
            screen.clear()
        elif menu_type == COMMAND:
            if menu.has_key('target'):
                if menu.has_key('container_info'):
                    runCommandWithTarget(menu_index + ITEM_START_ROW, menu['target'], itemInfo, menu['container_info'])
                else:
                    runCommandWithTarget(menu_index + ITEM_START_ROW, menu['target'], itemInfo, None)
                DockerContainers.refreshContainerInfo()
            else:
                runCommand(menu_index + ITEM_START_ROW, itemInfo)
        else:
            pass

        continue

def exec_command(commandList, shellmode = False, itemInfo = None):
    import subprocess
    if shellmode:
        go_shell_mode()

    if shellmode:
        command = ";".join(commandList)
        os.system(command)
    else:
        height, width = screen.getmaxyx()
        for command in commandList:
            screen.addstr(height - 3, 6, "CMD> %s" % command)
            screen.refresh()

            proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
        screen.clear()

    if shellmode:
        go_curses_mode()

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

def makeMenuTrees():
    menuTrees = {
        "title":"Development Environment Config Manager - [%s]" % current_user,
        "type":"MENU",
        "subtitle":"Please select an options...",
        "options":[
            {"title":"---------------------------------------------------------------------","type":SKIP},
            {"title":"Add User", "subtitle":"Add user - Enter user name", "type":COMMAND, "itemtype":ITEMTYPE_ADDUSER},
            {"title":"Remove User", "subtitle":"Remove user - Enter user name", "type":COMMAND, "itemtype":ITEMTYPE_REMOVEUSER},
            {"title":"---------------------------------------------------------------------","type":SKIP}
        ]
    }
    options = []
    docker_repo_dict = DockerContainers.getRepo()
    for repo, containers in docker_repo_dict.iteritems():
        data = {"itemtype":ITEMTYPE_REPO, "title":repo, "depth":0, "type":SKIP}
        menuTrees["options"].append(data)
        for container_image, container_info in containers.iteritems():
            data = {"itemtype":ITEMTYPE_TAG, "title":container_image, "depth":1, "type":MENU}
            menuTrees["options"].append(data)
            for reg_container_name, reg_container_info in container_info.iteritems():
                data = {"itemtype":ITEMTYPE_CONTAINER, "title":reg_container_name, "depth":2, "type":MENU, "container_info":reg_container_info}
                menuTrees["options"].append(data)


    return menuTrees

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
    DockerContainers = TDockerContainer.TDockerContainer('http://localhost:5000', host_ip_address, docker_prefix)
    menu = makeMenuTrees()

    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad(1)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    highlight = curses.color_pair(1)
    normalcolor = curses.A_NORMAL
    runcolor = curses.color_pair(2)

    processmenu(menu)

    curses.endwin()
    os.system('clear')

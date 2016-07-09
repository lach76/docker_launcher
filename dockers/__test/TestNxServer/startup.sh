#!/bin/bash

cp /mnt/passwd /etc/passwd
cp /mnt/group /etc/group
cp /mnt/shadow /etc/shadow
rm /var/lib/nxserver/home/.ssh/authorized_keys2
/usr/lib/nx/nxsetup --install --clean --purge --auto --setup-nomachine-key

mkdir /var/run/sshd
/usr/bin/supervisord -c /supervisord.conf

mkdir /tmp/.X11-unix
mkdir /tmp/.ICE-unix
chmod 1777 /tmp/.X11-unix
/etc/init.d/freenx-server start

while [ 1 ]; do
    /bin/bash
done
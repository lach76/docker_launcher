#!/bin/bash

# Run docker container with below options
# docker run -d -P -v /home:/home -v /nfsroot:/nfsroot -v /tftpboot:/tftpboot -v /opt:/opt -v /etc:/.tetc --name devenv ubuntu1404_base

## copy /tetc/pass to /etc/passwd
cp /.tetc/passwd /etc/passwd
cp /.tetc/shadow /etc/shadow
cp /.tetc/group /etc/group
cp /.tetc/gshadow /etc/gshadow

echo 'root:qauto2015%!' | chpasswd

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

#/usr/lib/nx/nxsetup --install --clean --purge --auto --setup-nomachine-key
#rm /var/lib/nxserver/home/.ssh/authorized_keys2
#/usr/lib/nx/nxsetup --install --clean --purge --auto --setup-nomachine-key

#mkdir /tmp/.X11-unix
#mkdir /tmp/.ICE-unix
#chmod 1777 /tmp/.X11-unix
#/etc/init.d/freenx-server start


#/etc/NX/nxserver --startup
#tail -f /usr/NX/var/log/nxserver.log
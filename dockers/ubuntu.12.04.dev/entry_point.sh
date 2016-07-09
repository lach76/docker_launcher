#!/bin/bash

# Run docker container with below options
# docker run -d -P -v /home:/home -v /nfsroot:/nfsroot -v /tftpboot:/tftpboot -v /opt:/opt -v /etc:/.tetc --name devenv ubuntu1404_base

## copy /tetc/pass to /etc/passwd
cp /.tetc/passwd /etc/passwd
cp /.tetc/shadow /etc/shadow
cp /.tetc/group /etc/group
cp /.tetc/gshadow /etc/gshadow

echo 'root:qauto2015%!' | chpasswd

mkdir /var/run/sshd
/usr/bin/supervisord -c /supervisord.conf

while [ 1 ]; do
    /bin/bash
done

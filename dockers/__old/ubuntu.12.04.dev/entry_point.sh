#!/bin/bash

# Run docker container with below options
# docker run -d -P -v /home:/home -v /nfsroot:/nfsroot -v /tftpboot:/tftpboot -v /opt:/opt -v /etc:/.tetc --name devenv_1204base ubuntu1204_base

# copy /tetc/pass to /etc/passwd
cp /.tetc/passwd /etc/passwd
cp /.tetc/shadow /etc/shadow
cp /.tetc/group /etc/group
cp /.tetc/gshadow /etc/gshadow

# Fix SSH Server
# mkdir /var/empty
# chown root:sys /var/empty
# chmod 755 /var/empty
# groupadd sshd
# useradd -g sshd -c 'sshd privsep' -d /var/empty -s /bin/false sshd

echo 'root:qauto2015%!' | chpasswd

exec "$@"

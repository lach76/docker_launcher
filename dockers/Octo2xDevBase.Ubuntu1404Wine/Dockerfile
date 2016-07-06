# Octo 2.x Development Default
# Version 0.1

FROM 10.0.218.196:5000/ubuntu.14.04.dev:octo2x
MAINTAINER SEiT@HUMAX

# Run container with below options
# docker run -d -P -p 6000:22 -v /home:/home -v /nfsroot:/nfsroot -v /tftpboot:/tftpboot -v /opt:/opt -v /etc:/.tetc --name octo2x_dev 10.0.218.196:5000/octo2x_devbase

#################################################################
# Packages
#################################################################
RUN dpkg --add-architecture i386 && add-apt-repository ppa:ubuntu-wine/ppa && \
    apt-get update && \
    apt-get install -y wine1.6

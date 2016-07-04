# Octo 2.x Development Default
# Version 0.1

FROM 10.0.218.196:5000/ubuntu.base:14.04
MAINTAINER SEiT@HUMAX

# Run container with below options
# docker run -d -P -p 6000:22 -v /home:/home -v /nfsroot:/nfsroot -v /tftpboot:/tftpboot -v /opt:/opt -v /etc:/.tetc --name octo2x_dev 10.0.218.196:5000/octo2x_devbase

#################################################################
# Packages
#################################################################
RUN sudo sed -i 's/kr.archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list
RUN dpkg --add-architecture i386 && add-apt-repository ppa:ubuntu-wine/ppa && \
    apt-get update && \
    apt-get install -y bc git-core gnupg flex bison gperf build-essential zip curl zlib1g-dev libc6-dev tmux \
    libncurses5-dev g++-multilib tofrodos flex \
    libglib2.0-dev uuid-dev lzop vim expect python-software-properties openssh-server \
    subversion lib32z1-dev lib32ncurses5-dev automake autoconf \
    python python-dev python-distribute python-pip \
    cmake \
    && \
    ln -s /usr/include/x86_64-linux-gnu/zconf.h /usr/include

# Downgrade bison 2.x for octo avinfo-1.0a15 package build
RUN wget http://kr.archive.ubuntu.com/ubuntu/pool/main/b/bison/libbison-dev_2.5.dfsg-2.1_amd64.deb && \
    wget http://kr.archive.ubuntu.com/ubuntu/pool/main/b/bison/bison_2.5.dfsg-2.1_amd64.deb && \
    dpkg -i libbison-dev_2.5.dfsg-2.1_amd64.deb && \
    dpkg -i bison_2.5.dfsg-2.1_amd64.deb && \
    rm libbison-dev_2.5.dfsg-2.1_amd64.deb && rm bison_2.5.dfsg-2.1_amd64.deb

# Make Login Message
COPY etc/motd /etc/motd

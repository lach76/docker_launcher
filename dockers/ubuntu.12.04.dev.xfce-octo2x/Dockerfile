# Octo 2.x Development Default
# Version 0.1

FROM 10.0.218.196:5000/ubuntu.12.04.dev.xfce
MAINTAINER SEiT@HUMAX

# Run container with below options
# docker run -d -P -p 6000:22 -v /home:/home -v /nfsroot:/nfsroot -v /tftpboot:/tftpboot -v /opt:/opt -v /etc:/.tetc --name octo2x_dev 10.0.218.196:5000/octo2x_devbase

#################################################################
# Packages
#################################################################
RUN sed -i 's/kr.archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list
#RUN dpkg --add-architecture i386 &&
RUN rm -fR /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get install -y bc git-core gnupg flex bison gperf build-essential zip curl zlib1g-dev libc6-dev tmux
#&& \

RUN apt-get install -y libncurses5-dev x11proto-core-dev libx11-dev libgl1-mesa-dev g++-multilib mingw32 tofrodos flex libesd0-dev
RUN apt-get install -y libglib2.0-dev uuid-dev nfs-common nfs-kernel-server lzop vim expect python-software-properties openssh-server
RUN apt-get install -y subversion lib32z1-dev lib32ncurses5-dev automake autoconf
RUN apt-get install -y python python-dev python-distribute python-pip
RUN apt-get install -y libxml-parser-perl cmake libnss3-tools
#RUN apt-get install -y wine1.6
#RUN ln -s /usr/include/x86_64-linux-gnu/zconf.h /usr/include

# Oracle JAVA Install
RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk8-installer

# Make Login Message
COPY etc/motd /etc/motd

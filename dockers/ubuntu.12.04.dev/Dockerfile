# Dockerfile to install NoMachine Workstation Evaluation v. 4 with MATE interface

FROM ubuntu:12.04
MAINTAINER SEiT@HUMAX

# Ubuntu 12.04 Base
ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root

# Change Default Source List
RUN sed -i 's/archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list

#  Install Default Packages
RUN apt-get update && \
    apt-get install -y python-software-properties software-properties-common \
    vim-tiny tree expect zip screen language-pack-ko language-pack-ko-base curl \
    subversion subversion-tools git-core ntp sudo openssh-server wget supervisor

# Oracle JAVA Install
#RUN \
#  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
#  add-apt-repository -y ppa:webupd8team/java && \
#  apt-get update && \
#  apt-get install -y oracle-java8-installer && \
#  rm -rf /var/lib/apt/lists/* && \
#  rm -rf /var/cache/oracle-jdk8-installer

# Set Default Configuration
    # set default shell script as bash
    RUN rm /bin/sh && ln -s /bin/bash /bin/sh

    # shell utils
    COPY usr/local/bin/urlcodec.sh /usr/local/bin/urlcodec.sh

    # locale configuration
    RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

    # allow sudo without password
    COPY etc/sudoers /etc/sudoers
    RUN chmod 440 /etc/sudoers

    # use nearest ntp server
    COPY etc/ntp.conf /etc/ntp.conf
    RUN service ntp restart

    # configure locale
    RUN locale-gen en_US.UTF-8
    RUN dpkg-reconfigure locales
    RUN \
    echo "export LC_ALL=en_US.UTF-8" >> /etc/bash.bashrc \
    && echo "export TERM=xterm" >> /etc/bash.bashrc \
    && echo "source ~/.bashrc" >> /etc/bash.bashrc

# Add Initial Run Script
ADD entry_point.sh /
ADD supervisord.conf /
#
EXPOSE 22

WORKDIR /
ENTRYPOINT ["/entry_point.sh"]

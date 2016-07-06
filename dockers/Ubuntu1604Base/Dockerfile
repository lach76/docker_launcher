# Ubuntu 16.04 x64 default Installation
# Version 0.1

FROM ubuntu:16.04
MAINTAINER SEiT@HUMAX

# Default package installation
RUN sed -i 's/archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list
RUN apt update
RUN apt install -y python-software-properties software-properties-common \
    vim tree expect zip screen language-pack-ko language-pack-ko-base curl \
    subversion subversion-tools git-core ntp
RUN apt install -y sudo

#################################################################
# Set configurations
#################################################################

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


# Install SSHD
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22

COPY entry_point.sh /entry_point.sh
RUN chmod 777 /entry_point.sh

CMD ["/usr/sbin/sshd", "-D"]
ENTRYPOINT ["/entry_point.sh"]

#ENTRYPOINT touch /nfsroot/a.touch


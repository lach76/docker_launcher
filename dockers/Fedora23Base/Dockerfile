# Fedora 23 x64 default Installation
# Version 0.1

FROM fedora:23
MAINTAINER SEiT@HUMAX

#################################################################
# Set configurations
#################################################################

#ENTRYPOINT touch /nfsroot/a.touch

RUN dnf install -y python-dnf-plugins-extras-migrate && dnf-2 migrate
RUN dnf -y update
RUN dnf -y reinstall glibc-common
RUN dnf -y install openssh-server
RUN dnf -y install supervisor sudo

RUN dnf -y groupinstall "Development Tools"
RUN dnf -y groupinstall "Development Libraries"
RUN dnf -y install glibc-devel.i686 glib2.i686 ncurses-devel ncurses-devel.i686 bc tar which bzip2 vim-common


RUN mkdir -p /var/run/sshd
RUN mkdir -p /var/run/supervisord
RUN echo "root:qauto2015%!" | chpasswd
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
RUN sed -i 's|session    required     pam_loginuid.so|session    optional     pam_loginuid.so|g' /etc/pam.d/sshd

ADD supervisord.conf /etc/supervisord.conf

COPY entry_point.sh /entry_point.sh
RUN chmod 777 /entry_point.sh

EXPOSE 22
CMD ["/usr/bin/supervisord", "-n"]
ENTRYPOINT ["/entry_point.sh"]

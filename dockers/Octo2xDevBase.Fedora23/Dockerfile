# Fedora 23 x64 default Installation
# Version 0.1

FROM 10.0.218.196:5000/fedora.23.dev
MAINTAINER SEiT@HUMAX

#################################################################
# Set configurations
#################################################################

#ENTRYPOINT touch /nfsroot/a.touch

RUN dnf -y groupinstall "Development Tools"
RUN dnf -y groupinstall "Development Libraries"
RUN dnf -y install glibc-devel.i686 glib2.i686 ncurses-devel ncurses-devel.i686 bc tar which bzip2 vim-common zlib.i686 zlib-devel.i686 file
RUN dnf -y install java-1.8.0-openjdk
# Make Login Message
COPY etc/motd /etc/motd
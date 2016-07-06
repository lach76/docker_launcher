# Octo 2.x Development Default
# Version 0.1

FROM 10.0.218.196:5000/ubuntu.14.04.dev
MAINTAINER SEiT@HUMAX

# Run container with below options
# docker run -d -P -p 6002:22 -v /home:/home -v /nfsroot:/nfsroot -v /tftpboot:/tftpboot -v /opt:/opt -v /etc:/.tetc --name yocto_dev 10.0.218.196:5000/yocto_devbase

#################################################################
# Build Pakcages
#################################################################

RUN sed -i 's/kr.archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list
#RUN dpkg --add-architecture i386 &&
RUN rm -fR /var/lib/apt/lists/*
RUN apt-get update
RUN dpkg --add-architecture i386
RUN apt-get update
RUN apt-get install -y build-essential gettext bison libfile-slurp-perl gawk \
        libncurses-dev autoconf flex doxygen libtool automake libpcre3-dev \
        zlib1g-dev libbz2-dev subversion minicom putty libssl-dev rpm \
        python-pexpect python-svn python-argparse vim tofrodos meld dos2unix \
        cmake uuid-dev ruby transfig libglib2.0-dev xutils-dev lynx-cur gperf \
        autopoint  python-dulwich  python-dev curl diffstat texinfo chrpath \
        sed wget cvs git-core coreutils unzip texi2html \
        libsdl1.2-dev docbook-utils python-pysqlite2 help2man \
        make gcc g++ desktop-file-utils libgl1-mesa-dev \
        libglu1-mesa-dev mercurial groff \
        gcj-jdk fakeroot openjdk-7-jdk maven ant \
        squashfs-tools intltool lzop libxml2-dev lib32ncurses5-dev \
        lib32z1 lib32bz2-1.0 \
        lib32stdc++6 lib32z1 lib32z1-dev

#################################################################
# REPO
#################################################################
RUN wget https://storage.googleapis.com/git-repo-downloads/repo -O /usr/local/bin/repo && chmod 777 /usr/local/bin/repo


# Make Login Message
COPY etc/motd /etc/motd

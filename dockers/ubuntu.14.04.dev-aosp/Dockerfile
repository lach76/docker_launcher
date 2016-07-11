#
# Minimum Docker image to build Android AOSP
#
FROM 10.0.218.196:5000/ubuntu.14.04.dev

MAINTAINER Kyle Manna <kyle@kylemanna.com>

# /bin/sh points to Dash by default, reconfigure to use bash until Android
# build becomes POSIX compliant
RUN echo "dash dash/sh boolean false" | debconf-set-selections && \
    dpkg-reconfigure -p critical dash

# Keep the dependency list as short as reasonable
RUN apt-get update && \
    apt-get install -y bc bison bsdmainutils build-essential curl \
        flex g++-multilib gcc-multilib git gnupg gperf lib32ncurses5-dev \
        lib32readline-gplv2-dev lib32z1-dev libesd0-dev libncurses5-dev \
        libsdl1.2-dev libwxgtk2.8-dev libxml2-utils lzop \
        openjdk-7-jdk \
        pngcrush schedtool xsltproc zip zlib1g-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install latest version of JDK
# See http://source.android.com/source/initializing.html#setting-up-a-linux-build-environment
WORKDIR /tmp
RUN curl -O http://mirrors.kernel.org/ubuntu/pool/universe/o/openjdk-8/openjdk-8-jre-headless_8u45-b14-1_amd64.deb && \
    curl -O http://mirrors.kernel.org/ubuntu/pool/universe/o/openjdk-8/openjdk-8-jre_8u45-b14-1_amd64.deb && \
    curl -O http://mirrors.kernel.org/ubuntu/pool/universe/o/openjdk-8/openjdk-8-jdk_8u45-b14-1_amd64.deb && \
    sum=`shasum ./openjdk-8-jre-headless_8u45-b14-1_amd64.deb | awk '{ print $1 }'` && \
    [ $sum == "e10d79f7fd1b3d011d9a4910bc3e96c3090f3306" ] || \
      ( echo "Hash mismatch. Problem downloading openjdk-8-jre-headless" ; exit 1; ) && \
    sum=`shasum ./openjdk-8-jre_8u45-b14-1_amd64.deb | awk '{ print $1 }'` && \
    [ $sum == "1e083bb952fc97ab33cd46f68e82688d2b8acc34" ] || \
      ( echo "Hash mismatch. Problem downloading openjdk-8-jre" ; exit 1; ) && \
    sum=`shasum ./openjdk-8-jdk_8u45-b14-1_amd64.deb | awk '{ print $1 }'` && \
    [ $sum == "772e904961a2a5c7d2d129bdbcfd5c16a0fab4bf" ] || \
      ( echo "Hash mismatch. Problem downloading openjdk-8-jdk" ; exit 1; ) && \
    dpkg -i *.deb && \
    apt-get -f install && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Improve rebuild performance by enabling compiler cache
ENV USE_CCACHE 1


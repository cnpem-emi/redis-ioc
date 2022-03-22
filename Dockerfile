FROM debian:10-slim

# set correct timezone
ENV DEBIAN_FRONTEND noninteractive
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV APT_PROXY TA-TiRack-CO-FWSrv-1.abtlus.org.br

RUN set -ex; \
    echo "Acquire::http { Proxy \"http://${APT_PROXY}:3142\"; }" > /etc/apt/apt.conf.d/proxy ;\
    apt-get update &&\
    apt-get install -y --fix-missing --no-install-recommends \
        build-essential \
        ca-certificates \
        gettext-base \
        git \
        libpcre3-dev \
        libreadline-gplv2-dev \
        logrotate \
        tzdata \
        wget \
        python3 \
        curl \
        python3-pip \
        python3-setuptools \
        && rm -rf /var/lib/apt/lists/*  && \
    dpkg-reconfigure --frontend noninteractive tzdata

# --- General Usage ---
# IOC operation variables
ENV EPICS_VERSION R3.15.8
ENV EPICS_HOST_ARCH linux-x86_64
ENV EPICS_BASE /opt/epics-${EPICS_VERSION}/base
ENV EPICS_MODULES /opt/epics-${EPICS_VERSION}/modules
ENV PATH ${EPICS_BASE}/bin/${EPICS_HOST_ARCH}:/opt/procServ:${PATH}

ENV EPICS_CA_AUTO_ADDR_LIST YES

# Pyepics libca location
ENV PYEPICS_LIBCA ${EPICS_BASE}/lib/${EPICS_HOST_ARCH}/libca.so

# --- EPICS BASE ---
ARG EPICS_BASE_URL=https://github.com/epics-base/epics-base/archive/${EPICS_VERSION}.tar.gz
LABEL br.com.lnls-sirius.epics-base=${EPICS_BASE_URL}
RUN set -x;\
    set -e;\
    mkdir -p ${EPICS_MODULES};\
    wget -O /opt/epics-R3.15.8/base-3.15.8.tar.gz ${EPICS_BASE_URL};\
    cd /opt/epics-${EPICS_VERSION};\
    tar -zxf base-3.15.8.tar.gz;\
    rm base-3.15.8.tar.gz;\
    mv epics-base-R3.15.8 base;\
    cd base;\
    make -j$(nproc)

WORKDIR /opt/epics-${EPICS_VERSION}

# --- EPICS MODULES ---

# sscan-R2-11-3
ARG SSCAN_VERSION=R2-11-4
ARG SSCAN_URL=https://github.com/epics-modules/sscan/archive/${SSCAN_VERSION}.tar.gz
LABEL br.com.lnls-sirius.sscan=${SSCAN_URL}
ENV SSCAN ${EPICS_MODULES}/sscan-${SSCAN_VERSION}
RUN set -x;\
    set -e;\
    cd ${EPICS_MODULES};\
    wget -O ${SSCAN}.tar.gz ${SSCAN_URL};\
    tar -xvzf ${SSCAN}.tar.gz;\
    rm ${SSCAN}.tar.gz;\
    cd ${SSCAN};\
    sed -i\
        -e '7s/^/#/'\
        -e '10s/^/#/'\
        -e '14cEPICS_BASE='${EPICS_BASE} \
        configure/RELEASE;\
    make -j$(nproc)

# synApps Calc Module
ARG CALC_VERSION=R3-7-4
ARG CALC_URL=https://github.com/epics-modules/calc/archive/${CALC_VERSION}.tar.gz
LABEL br.com.lnls-sirius.calc=${CALC_URL}
ENV CALC ${EPICS_MODULES}/synApps/calc-${CALC_VERSION}
RUN set -x;\
    set -e;\
    cd ${EPICS_MODULES};\
    mkdir synApps;\
    cd synApps;\
    wget -O ${CALC}.tar.gz ${CALC_URL};\
    tar -xvzf ${CALC}.tar.gz;\
    rm ${CALC}.tar.gz;\
    cd ${CALC};\
    sed -i \
        -e '5s/^/#/'\
        -e '7,8s/^/#/'\
        -e '13cSSCAN='${SSCAN}\
        -e '20cEPICS_BASE='${EPICS_BASE} \
        configure/RELEASE;\
    make -j$(nproc)

# asynDriver
ARG ASYN_VERSION=R4-41
ARG ASYN_URL=https://github.com/epics-modules/asyn/archive/${ASYN_VERSION}.tar.gz
ENV ASYN ${EPICS_MODULES}/asyn-${ASYN_VERSION}
LABEL br.com.lnls-sirius.asyn=${ASYN_URL}
RUN set -x;\
    set -e;\
    cd ${EPICS_MODULES};\
    wget ${ASYN_URL} -O ${ASYN}.tar.gz;\
    tar -xvzf ${ASYN}.tar.gz;\
    rm -f ${ASYN}.tar.gz;\
    cd ${ASYN};\
    sed -i \
        -e '3,4s/^/#/'\
        -e '7s/^/#/'\
        -e '10s/^/#/'\
        -e '19cEPICS_BASE='${EPICS_BASE} \
        -e '15iCALC='${CALC}\
        -e '16iSSCAN='${SSCAN}\
        ${ASYN}/configure/RELEASE;\
    make -j$(nproc)

# Autosave
ARG AUTOSAVE_VERSION=R5-10-2
ARG AUTOSAVE_URL=https://github.com/epics-modules/autosave/archive/${AUTOSAVE_VERSION}.tar.gz
ENV AUTOSAVE ${EPICS_MODULES}/asyn-${AUTOSAVE_VERSION}
LABEL br.com.lnls-sirius.autosave=${AUTOSAVE_URL}
ENV AUTOSAVE ${EPICS_MODULES}/autosave-${AUTOSAVE_VERSION}
RUN set -x;\
    set -e;\
    cd ${EPICS_MODULES};\
    wget -O ${AUTOSAVE}.tar.gz ${AUTOSAVE_URL};\
    tar -zxvf ${AUTOSAVE}.tar.gz;\
    rm -f ${AUTOSAVE}.tar.gz;\
    cd ${AUTOSAVE};\
    sed -i \
        -e '7s/^/#/'\
        -e'10cEPICS_BASE='${EPICS_BASE}\
        configure/RELEASE;\
    make -j$(nproc)

# Caput Log
ARG CAPUTLOG_VERSION=R3.7
ARG CAPUTLOG_URL=https://github.com/epics-modules/caPutLog/archive/${CAPUTLOG_VERSION}.tar.gz
ENV CAPUTLOG ${EPICS_MODULES}/asyn-${CAPUTLOG_VERSION}
LABEL br.com.lnls-sirius.caputlog=${CAPUTLOG_URL}
ENV CAPUTLOG /opt/epics-R3.15.8/modules/caPutLog-${CAPUTLOG_VERSION}
RUN set -x;\
    set -e;\
    cd ${EPICS_MODULES};\
    wget -O ${CAPUTLOG}.tar.gz ${CAPUTLOG_URL};\
    tar -zxvf ${CAPUTLOG}.tar.gz;\
    rm -f ${CAPUTLOG}.tar.gz;\
    cd ${CAPUTLOG};\
    sed -i\
        -e '22cEPICS_BASE='${EPICS_BASE}\
        configure/RELEASE;\
    make -j$(nproc)

# Streamdevice
ARG STREAMDEVICE_URL=https://github.com/paulscherrerinstitute/StreamDevice
LABEL br.com.lnls-sirius.streamdevice=${STREAMDEVICE_URL}
ENV STREAMDEVICE ${EPICS_MODULES}/StreamDevice-2.8.18
ENV STREAM ${STREAMDEVICE}
LABEL br.com.lnls-sirius.streamdevice=${STREAMDEVICE_URL}
RUN set -x;\
    set -e;\
    cd ${EPICS_MODULES};\
    git clone ${STREAMDEVICE_URL} ${STREAM};\
    cd ${STREAM} &&\
    git fetch --all --tags &&\
    git checkout tags/2.8.18 && git status
RUN cd ${STREAM} &&\
    sed -i -e '20cASYN='${ASYN}\
           -e '21cCALC='${CALC}\
           -e '22s/^/#/'\
           -e '23cSSCAN='${SSCAN}\
           -e '25cEPICS_BASE='${EPICS_BASE}\
           configure/RELEASE && cat configure/RELEASE &&\
    echo 'PCRE_INCLUDE=/usr/include' > configure/RELEASE.Common.linux-x86_64 &&\
    echo 'PCRE_LIB=/usr/lib/x86_64-linux-gnu' >> configure/RELEASE.Common.linux-x86_64 &&\
    make -j$(nproc)

# procServ
RUN set -x;\
    set -e;\
    wget https://github.com/ralphlange/procServ/releases/download/v2.8.0/procServ-2.8.0.tar.gz;\
    tar -zxvf procServ-2.8.0.tar.gz;\
    cd procServ-2.8.0;\
    ./configure --enable-access-from-anywhere;\
    make install;\
    cd ..;\
    rm -rf procServ-2.8.0.tar.gz procServ-2.8.0

# Busy
ARG BUSY_VERSION=R1-7-3
ARG BUSY_URL=https://github.com/epics-modules/busy/archive/${BUSY_VERSION}.tar.gz
LABEL br.com.lnls-sirius.busy=${BUSY_URL}
ENV BUSY ${EPICS_MODULES}/busy-${BUSY_VERSION}
RUN set -x;\
    set -e;\
    cd ${EPICS_MODULES};\
    wget -O ${BUSY}.tar.gz ${BUSY_URL};\
    tar -zxf ${BUSY}.tar.gz;\
    rm -f ${BUSY}.tar.gz;\
    cd ${BUSY};\
    sed -i\
        -e '7,8s/^/#/'                     \
        -e '10cASYN='${ASYN}               \
        -e '13cAUTOSAVE='${AUTOSAVE}       \
        -e '16cBUSY='${BUSY}               \
        -e '19cEPICS_BASE='${EPICS_BASE}   \
        configure/RELEASE;\
    make -j$(nproc)

# Sequencer
RUN apt-get update &&\
    apt-get install -y --fix-missing --no-install-recommends re2c &&\
    rm -rf /var/lib/apt/lists/*

ARG SNCSEQ_URL=https://github.com/ISISComputingGroup/EPICS-seq/archive/vendor_2_2_8.tar.gz
LABEL br.com.lnls-sirius.seq=${SNCSEQ_URL}
ENV SNCSEQ ${EPICS_MODULES}/seq-2.2.8
RUN set -x;\
    set -e;\
    cd ${EPICS_MODULES};\
    wget -O ${SNCSEQ}.tar.gz ${SNCSEQ_URL};\
    tar -xvzf ${SNCSEQ}.tar.gz;\
    rm -f ${SNCSEQ}.tar.gz;\
    mv *seq* ${SNCSEQ};\
    cd ${SNCSEQ};\
    sed -i \
        -e '6cEPICS_BASE='${EPICS_BASE} \
        configure/RELEASE;\
    make -j$(nproc)

RUN set -x;\
    set -e;\
    cd ${EPICS_MODULES};\
    wget -O asyn-failover-0.1.1.tar.gz https://github.com/cnpem-iot/asyn-failover/archive/refs/tags/v0.1.1.tar.gz;\
    tar -xzf asyn-failover-0.1.1.tar.gz;\
    ls;\
    cd asyn-failover-0.1.1;\
    make

WORKDIR /opt/redis-ioc

RUN pip3 install setuptools pylightxl && mkdir -p sockets && mkdir -p log

COPY . . 

CMD ["/bin/bash", "-c", "set -e; cd scripts/; make run"]

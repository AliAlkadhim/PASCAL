FROM cern/cc7-base:latest
MAINTAINER Ali AlKadhim aa18dg@fsu.edu

# If not running docker with --volume /home/ali/Desktop/Pulled_Github_Repositories/PASCAL:/home then make those directories and copy stuff into them

RUN mkdir -p /home/queries /home/images /home/miscillaneous /home/notebooks /home/outputs /home/utils /home/logs
# Copy Stuff from host in the HOST_CURRENT_DIRECTORY/utilts to /home/ in the server
COPY queries/* /home/queries
# COPY images/* /home/images
COPY miscillaneous/* /home/miscillaneous
COPY notebooks/* /home/notebooks
# COPY outputs/* /home/outputs
COPY utils/* /home/utils


# Otherwise, if running docker with --volume /home/ali/Desktop/Pulled_Github_Repositories/PASCAL:/home then 


# install non-oracle dependencies
RUN yum -y update && \
        yum clean all && \
	yum install -y \
	gcc \
	openssl-devel \
	bzip2-devel \
	libffi-devel \
	zlib-devel \
	xz-devel \
	sqlite-devel \
	httpd \
	log4shib \
	lsof \
	nano \
	xmltooling-schemas \
	git \
        tree \
	python-virtualenv.noarch \
	which \
	mlocate \
	shibboleth \
 # enable epel YUM REPO before installing DNF.
        epel-release \
        # dnf \
        # dnf-plugins-core \
        # install binutils

RUN cd /home
# RUN git clone https://github.com/AliAlkadhim/PASCAL.git
# Change Cernonly repo to enabled. This is the 28th line in /etc/yum.repos.d/CentOS-CERN.repo
RUN sed -i '28s;enabled=0;enabled=1;g' /etc/yum.repos.d/CentOS-CERN.repo

RUN yum install -y \
    oracle-instantclient-tnsnames.ora \
    # (which is oracle-instantclient-tnsnames.ora-1.4.4-1.el7.cern.noarch)
    oracle-instantclient12.2 \
    oracle-instantclient12.2-sqlplus \
    oracle-instantclient-basic \
    oracle-instantclient-devel 

# Set the env TNS_ADMIN to home because that's where our .ora file will be saved to. 
ENV TNS_ADMIN=/home
#INSTALL PYTHON 3.7
RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz --no-check-certificate && \
        tar xzf Python-3.7.2.tgz && \
        cd Python-3.7.2 && \
        ./configure --prefix=/usr/local --enable-loadable-sqlite-extensions --enable-shared --with-lto --enable-optimizations && \
        make -j `nproc` && \
        make install

# UPDATE ENV
#ldconfig
ENV LD_LIBRARY_PATH=/lib:/usr/lib:/usr/local/lib
ENV PASCAL=/home

# if using git
# RUN mkdir /home/utils
# COPY utils/* /home/utils
# INSTALL DCA PYTHON PACKAGES AND SQLITE
RUN cd /home && \
        pip3.7 install -r utils/requirements.txt && \
        cd /usr/src && \
        wget https://www.sqlite.org/2019/sqlite-autoconf-3280000.tar.gz --no-check-certificate && \
        tar xzf sqlite-autoconf-3280000.tar.gz && \
        cd sqlite-autoconf-3280000 && \
        ./configure --enable-loadable-sqlite-extensions && \
        make -j 6 && \
        make install

# GIT CLONE DCA-GUI, but currently it's already there (copied from host)
##############################################################
# INSTALL BRAVE WITH DNF: https://brave.com/linux/#release-channel-installation
# need GLIBC_2.25 for brave! do "ldd --version | head -n1" to find your current versuion
# RUN dnf install dnf-plugins-core && \
# dnf config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo && \
# rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc && \
# dnf install brave-browser
### INSTALL FIREFOX WITH DNF
#dnf install firefox
# INSTALL SNAP
#       FIRST, ENABLE EPEL REPO
# edit nano /etc/yum.repos.d/epel.repo and set enabled=true
# then: yum install -y snapd
# then: snap install brave
# then: systemctl enable --now snapd.socket
# INSTALL BRAVE WITH SNAP


# INSTALL FIREFOX WITH APT
# FROM ubuntu:14.04
# RUN apt-get update && apt-get install -y firefox


# INSTALL CHROME WITH WGET AND YUM
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
# yum localinstall -y google-chrome-stable_current_x86_64.rpm
# check with google-chrome --no-sandbox
##############################################################
# X11 FORWARDING
# Replace 1000 with your user / group id
# RUN export uid=1000 gid=1000 && \
#     mkdir -p /home/developer && \
# #     mkdir -p  /etc/sudoers.d && \
# #     touch /etc/sudoers.d/developer && \
#     echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
#     echo "developer:x:${uid}:" >> /etc/group && \
#     echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
#     chmod 0440 /etc/sudoers.d/developer && \
#     chown ${uid}:${gid} -R /home/developer

# USER developer
# ENV HOME /home/developer
##############################################################
# X11 FORWARDING ANOTHER WAY
# ENV USERNAME=ali
# ENV UID=1000
# ENV GID=1000
# RUN groupadd -g 1000 ali
# RUN useradd -d /home/ali -s /bin/bash -m ali -u 1000 -g 1000
# USER ali
# ENV HOME /home/ali


#UPDATE LD_LIBRARY_PATH AGAIN
# ENV export LD_LIBRARY_PATH=/usr/local/lib:/usr/lib:/usr/local/lib64:/usr/lib64
ENV LD_LIBRARY_PATH=/lib:/usr/lib:/usr/local/lib
# UPDATE PIP
#python3 -m pip install urllib3==1.26.6
RUN pip3.7 install --upgrade pip && \
          pip3.7 install urllib3==1.26.6 jupyterlab pandas matplotlib numpy ipywidgets argparse
RUN jupyter nbextension enable --py widgetsnbextension
          


# make port 8888 discoverable before publishing it
EXPOSE 8888

# go to home directory when running container
WORKDIR /home/

# experiment with CMD - currently not needed
# CMD ["/usr/sbin/init"]

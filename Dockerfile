FROM ubuntu:16.04
MAINTAINER plebnet

WORKDIR /root

# This dockerfile starts tribler including market for use by plebnet

RUN apt update && apt install -y \
# General dependencies
    python-pip\
	git \
# Tribler (headless) dependencies
	python-twisted \
	python-libtorrent \
	python-apsw \
	python-chardet \
	python-cherrypy3 \
	python-nacl \
	python-m2crypto \
	python-configobj \
	python-netifaces \
	python-leveldb \
	python-decorator \
	python-feedparser \
# Market community dependencies
	python-keyring \
	python-libnacl \
	python-ecdsa \
	python-pbkdf2 \
	python-requests \
	python-protobuf \
	python-socks \
	python-dnspython \
	python-jsonrpclib \
	python-keyrings.alt \
# Market community reputation dependencies
	python-networkx \
	python-scipy

RUN apt install -y openvpn
	
RUN pip install pyaes psutil requests[security]

WORKDIR /root

# Install mechanicalsoup from git,
# at the time of writing the pypi version has a bug
# that prevents cloudomate from working in python 2.7
RUN git clone https://github.com/MechanicalSoup/MechanicalSoup.git
RUN pip install ./MechanicalSoup

# Install cloudomate
RUN git clone -b plebref https://github.com/Erackron/cloudomate.git
RUN pip install ./cloudomate

# Install plebnet
ADD . ./PlebNet
RUN pip install ./PlebNet
RUN pip install ./PlebNet/tribler/electrum

# Create config folder for cloudomate and plebnet
RUN mkdir .config
RUN plebnet setup

# Open up RESTapi port to host system
#WORKDIR /root/tribler
#RUN sed -ie 's/"127.0.0.1"/"0.0.0.0"/g' /root/tribler/Tribler/Core/Modules/restapi/rest_manager.py


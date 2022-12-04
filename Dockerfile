# syntax=docker/dockerfile:1.2
FROM python:3.8

LABEL NAME="python-3.8" \
      VERSION="3.8" \
      DESC="Python3.8 container"

# user arguments
ARG username=root
ARG skeleton=/home/dockeruser
ARG docker_uid=1000
ARG docker_gid=1000

# Install basic packages
RUN apt clean
RUN apt-get update -y && apt-get install -y \
  ca-certificates \
  sudo \
  curl \
  gnupg \
  lsb-release \
  iproute2 \
  iputils-ping \
  traceroute \
  net-tools \
  iptables \
  openssh-client \
  python3-pip \
  vim \
  telnet \
  bash

# Setup for Test
COPY docker-local-files/requirements.txt /tmp
RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt
RUN sed -i 's/@pytest.mark.hookwrapper/@pytest.hookimpl(hookwrapper=True)/' /usr/local/lib/python3.8/site-packages/pytest_csv/_reporter.py

# Clean image
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/*

# Create docker group to share the same group right permission with host
RUN groupadd -r -g ${docker_gid} docker

#Install E2E_tests
RUN install -o ${username} -g ${docker_gid} -m 755 -d /opt/workdir
COPY --chown=${username}}:${docker_gid} src /opt/workdir
COPY --chown=${username}}:${docker_gid} tests /opt/workdir

USER ${username}
RUN chmod g+rw -R /opt/workdir
ENV PYTHONPATH=/opt/workdir
WORKDIR /opt/workdir
FROM odoo:9
MAINTAINER Csaba Palankai <csaba.palankai@gmail.com>

USER root

# Make sure we can install packages
RUN apt-get update && apt-get install -y \
        python-setuptools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ADD /addons /mnt/extra-addons

USER odoo


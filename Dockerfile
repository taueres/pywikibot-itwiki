FROM alpine

MAINTAINER Sergio Santoro

RUN apk update
RUN apk add bash
RUN apk add python3
RUN apk add git
RUN apk add wget

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /tmp
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN pip install requests

RUN wget http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-2.0.4.tar.gz
RUN tar -xzf mysql-connector-python-2.0.4.tar.gz
RUN mv mysql-connector-python-2.0.4 /usr/lib/mysql-connector-python
RUN ln -s /usr/lib/mysql-connector-python/lib/mysql /usr/lib/python3.5/mysql

# INSTALL PYWIKIBOT
RUN git clone --depth=2 https://gerrit.wikimedia.org/r/pywikibot/core /root/pywikibot

WORKDIR /root/it-pywikibot

ENTRYPOINT ["/root/it-pywikibot/bin/run.sh"]

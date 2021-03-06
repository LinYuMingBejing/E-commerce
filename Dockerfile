FROM            python:3.6-onbuild
MAINTAINER      a828215362@gmail.com

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools 

RUN mkdir -p /usr/src/app  /var/log/gene /etc/supervisor/conf.d /var/log/supervisord

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
COPY entrypoint.sh /
COPY supervisord.conf /etc/
COPY supervisor-uwsgi.conf supervisor-worker.conf /etc/supervisor/conf.d/  

RUN  chmod +x /entrypoint.sh 
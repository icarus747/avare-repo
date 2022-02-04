FROM ubuntu:latest
#FROM avare-repo-bash

# Add crontab file in the cron directory
COPY app/* /app/

# Give execution rights on the cron job
RUN chmod +x /app/*

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#TimeZone
ARG TZ=America/Chicago
ENV TZ=$TZ
#Repo
ARG REPO='http://www.apps4av.org/new/'
ENV REPO=$REPO
#Limit Repo
ARG LIMIT='no'
ENV LIMIT=$LIMIT


RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


#Install Cron, WGET, and clean
RUN apt-get update
## RUN apt-get -y install -qq --force-yes cron wget aria2 python3 python3-pip
RUN apt-get -y install -qq cron wget aria2 python3 python3-pip
RUN apt-get -y clean

RUN pip3 install --no-cache-dir -r /app/requirements.txt

#Script that installes the cron job
ENTRYPOINT /app/entrypoint.sh

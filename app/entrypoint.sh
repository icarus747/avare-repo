#!/bin/bash

echo "Docker container downloading Avare updates."

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

#Run Repo once
echo "Creating Repo Directories."
python3 /app/repo_setup.py

echo "Runing init repo pull."
sh /app/repo.sh
sh /app/download.sh

echo "SHELL=/bin/bash
BASH_ENV=/container.env
*/10 * * * * /app/download.sh >> /var/log/cron.log 2>&1

00 12 30 * * /app/repo.sh >> /var/log/cron.log 2>&1

# This extra line makes it a valid cron" > scheduler.txt


crontab scheduler.txt
cron -f


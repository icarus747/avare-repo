# avare-repo
Docker app that is used to pull down charts from avare

# App Files
 - download.sh - Used to update weather, conus, and TFRs every 10 mins via container cronjob
 - entrypoint.sh - What docker runs at start up.
 - input.txt - Internal reference for download.sh. 
 - repo.sh - Called by container init or crontab to pull down the charts/etc. Will not pull a file if it has already been downloaded. Uses aria2c.
 - repo_setup.py - Script to create the environment. Called by entrypoint.sh
 - requirements.txt - Used during build to install the required python libraries.
 - Dockerfile - Used to build the container image. Uses Ubuntu as a base.
 - docker-compose.yml - suggested docker setup for this app to create a repository and a frontend webserver (nginx)


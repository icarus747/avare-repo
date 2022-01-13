# avare-repo
Docker app that is used to pull down charts from avare

# App Files
 - `download.sh` - Used to update weather, conus, and TFRs every 10 mins via container cronjob
 - `entrypoint.sh` - What docker runs at start up.
 - `input.txt` - Internal reference for download.sh. 
 - `repo.sh` - Called by container init or crontab to pull down the charts/etc. Will not pull a file if it has already been downloaded. Uses aria2c.
 - `repo_setup.py` - Script to create the environment. Called by entrypoint.sh
 - `requirements.txt` - Used during build to install the required python libraries.
 - `Dockerfile` - Used to build the container image. Uses Ubuntu as a base.
 - `docker-compose.yml` - Suggested docker setup for this app to create a repository and a frontend webserver (nginx)
 - `default` - Basic site configuration for nginx

# How to Start
Clone this project into your collection of docker containers directory.  It uses docker-compose for container management. When you first run the container it will build the avare-repo image so it might take a while to compile. 

After the image is created 'avare-repo' will clone Avare's repository to local disk. avare-web will start and present a directory frontend for the files.

In your Avare app on your phone/tablet proceed to `Menu ► Preferences ► Storage and Downloads ► Private Server Address`.  Here you can put in your server IP address or domain name. ie: `http://192.168.1.25/`
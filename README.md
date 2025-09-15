# avare-repo
Docker app that is used to pull down charts from avare

# App Files
There are three docker containers that run for the Avare repository. Nginx for the web interface, avare-repo to download the master zip files, and avare-wx to do 10 minuite updates to the weather/tfr/nexrad files. 

 - `version_checker.py` - Script to create the environment.
 - `check_weather.py` - Periodic updates to weather, tfr, nexrad data files
 - `requirements.txt` - Used during build to install the required python libraries.
 - `Dockerfile` - Used to build the container image. Uses Python:3.12-slim.
 - `docker-compose.yml` - Suggested docker setup for this app to create a repository and a frontend webserver (nginx)
 - `default` - Basic site configuration for nginx

# How to Start
Clone this project into your collection of docker containers directory.  It uses docker-compose for container management. When you first run the container it will build the avare-repo and avare-weather images so it might take a while to compile. 

After the image is created 'avare-repo' will clone Avare's repository to local disk. avare-web will start and present a directory frontend for the files. 'avare-weather' will do 10 min updates to the weather, tfr, nexrad files. 

In your Avare app on your phone/tablet proceed to `Menu ► Preferences ► Storage and Downloads ► Private Server Address`.  Here you can put in your server IP address or domain name. ie: `http://192.168.1.25/`

When your local repo is out of date, subfolder to regsions, just stop the container and start it back.  The `version_checker.py` file will look for the new data and sync it to your server.  Not that you will not need the old folder once it is out of date. Delete the older folder in `config/www/regions/xxxx`  where `xxxx` is the version number.  The lower number is the older data. 

### NOTE ###
This does not work with Avare-X.  The developers removed the private server option and requires additional container resources to make it work.  In short you have to use your local DNS server to point their domain to a local reverse proxy.  The reverse proxy will redirect to your server. It is possible with containers like pihole and traefik. 
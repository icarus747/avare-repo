#!/usr/bin/env python3
# By DangerZone
# Created 1/29/2021

import requests
from bs4 import BeautifulSoup
import os
import datetime
from yarl import URL


# wget --mirror --no-directories --no-verbose --directory-prefix=. http://www.apps4av.org/new/2101/databases.zip

def generate_input_file(url, zipfiles, filename):
    with open(filename, 'w') as output_file:
        for zipfile in zipfiles:
            fileurl = url / zipfile
            output_file.write(str(fileurl))
            output_file.write('\n')


def create_ver_dir(dir_path, version):
    dir_path = dir_path + version  # For Docker Container
    try:
        os.chdir(dir_path)
    except:
        os.mkdir(dir_path)
        os.chdir(dir_path)


def update_php(version):
    with open('version.php', 'w') as php_file:
        php_file.write(version)


def parse_web(response):
    zipfiles = []
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a', href=True):
        if '.txt' and '.zip' in link.attrs['href']:
            zipfiles.append(link.attrs['href'])
    return zipfiles


def get_version(url):
    response = requests.get(url / 'version.php')
    return response.text.strip('\n')

def get_static(url):
    static_url = url / "static"
    print(f"Static URL: {static_url}")
    return

def main():
    print(f'[{datetime.datetime.now()}] running avare repo download.')
    inputfiles = []
    url = URL(os.environ["REPO"].strip("'"))
    version = get_version(url)
    # dir_path = './' # For local testing
    dir_path = '/config/www/' # For Docker Container
    create_ver_dir(dir_path, version)
    create_ver_dir(dir_path, "static")
    os.chdir("../")
    update_php(version)
    version = version + '/'
    response = requests.get(url / version)
    zipfiles = parse_web(response)
    for x in zipfiles:
        inputfiles.append(version + x)
    generate_input_file(url, inputfiles, "input.txt")
    zipfiles = []
    inputfiles = []
    response = requests.get(url / "static")
    zipfiles = parse_web(response)
    for x in zipfiles:
        inputfiles.append("static/" + x)
    generate_input_file(url, inputfiles, "inputstatic.txt")
    print(f'[{datetime.datetime.now()}] finished avare repo download.')


if __name__ == '__main__':
    main()

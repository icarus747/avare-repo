import requests
from bs4 import BeautifulSoup
import re
import os
import datetime
from yarl import URL


def populate_repository(url, zipfiles, dir_path):

    for zipfile in zipfiles:
        fileurl = url / zipfile

        if os.path.exists(os.path.join(dir_path, zipfile)):
            print(f'[{datetime.datetime.now()}] Already downloaded: {fileurl}')
            continue
        else:
            print(f'[{datetime.datetime.now()}] Downloading: {fileurl}')
            response = requests.get(fileurl)

            with open(zipfile, 'wb') as output_file:
                file_bin = response.content
                print(f'[{datetime.datetime.now()}] \tWriting {zipfile} - {len(file_bin)} bytes')
                output_file.write(file_bin)


def parse_web(response):
    zipfiles = []
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a', href=True):
        if '.txt' and '.zip' in link.attrs['href']:
            zipfiles.append(link.attrs['href'])
    return zipfiles


def get_version(url):
    response = requests.get(url / 'version.php')
    return response.text


def main():
    print(f'[{datetime.datetime.now()}] running avare repo download.')
    url = URL('http://www.apps4av.org/new/')
    version = get_version(url)
    dir_path = './'+version
    try:
        os.chdir(dir_path)
    except:
        os.mkdir(dir_path, mode=0o644, dir_fd=None)
        os.chdir(dir_path)
    response = requests.get(url / version)
    zipfiles = parse_web(response)
    populate_repository(url / version, zipfiles, dir_path)
    print(f'[{datetime.datetime.now()}] finished avare repo download.')


if __name__ == '__main__':
    main()

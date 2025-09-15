import os
import time
import requests
from bs4 import BeautifulSoup

# Constants
BASE_URL = "http://www.apps4av.org/regions/"
DOWNLOAD_DIR = "/config/www/regions"  # Directory for saving downloaded files
CHECK_INTERVAL_SECONDS = 10 * 60  # 10 minutes in seconds

def fetch_zip_files():
    """Scrapes the 'regions' directory for .zip files."""
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        zip_files = []
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.zip'):
                zip_files.append(BASE_URL + href)
        
        return zip_files
    except requests.RequestException as e:
        print(f"Error fetching zip files: {e}")
        return []

def download_file(url):
    """Downloads a file and saves it to the specified directory."""
    local_filename = os.path.join(DOWNLOAD_DIR, os.path.basename(url))
    
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded {local_filename}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")

def check_for_updates():
    """Main logic for checking and downloading updated .zip files."""
    zip_files = fetch_zip_files()
    if zip_files:
        for file_url in zip_files:
            download_file(file_url)

if __name__ == "__main__":
    while True:
        check_for_updates()
        time.sleep(CHECK_INTERVAL_SECONDS)

import os
from glob import glob
import time
import subprocess
import requests
from bs4 import BeautifulSoup
from yarl import URL

# Constants
VERSION_URL = "http://www.apps4av.org/regions/version.php"
BASE_URL = URL(os.environ["REPO"])
CHECK_INTERVAL_DAYS = 30
VERSION_FILE = "/config/www/regions/version.php"  # Local version file
STATIC_PATH = "/config/www/regions/static"
INPUT_FILE = "input.txt"
DOWNLOAD_DIR = "/config/www/regions"  # Directory for downloading files


def get_remote_version():
    """Fetches the remote version from the version URL."""
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching remote version: {e}")
        return None


def get_local_version():
    """Reads the local version from the version.php file."""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    return None


def get_local_static():
    if len(glob(f"{STATIC_PATH}/*.zip")) >= 117:
        return True
    return False


def save_local_version(version):
    """Saves the given version to the version.php file."""
    with open(VERSION_FILE, "w") as f:
        f.write(version)


def fetch_files_from_directory(version):
    """Scrapes zip and txt files from the specified version directory."""
    dir_url = f"{BASE_URL}{version}/"
    try:
        response = requests.get(dir_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        files = []

        for link in soup.find_all("a"):
            href = link.get("href")
            if href and (href.endswith(".zip") or href.endswith(".txt")):
                full_path = dir_url + href
                files.append(full_path)

        return files
    except requests.RequestException as e:
        print(f"Error fetching files from directory: {e}")
        return []


def save_to_input_file(files):
    """Saves the list of file URLs to input.txt."""
    with open(INPUT_FILE, "w") as f:
        for file_url in files:
            f.write(file_url + "\n")


def download_files_with_aria2(version):
    """Calls aria2c to download the files listed in input.txt."""
    download_path = os.path.join(DOWNLOAD_DIR, version)

    # Create a directory for the new version
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Execute aria2c to download files into the version-specific directory
    try:
        subprocess.run(
            ["aria2c", "-i", INPUT_FILE, "-d", download_path, "--continue=true"],
            check=True,
        )
        print(f"Downloaded files to {download_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running aria2c: {e}")


def check_for_updates():
    """Main logic for checking and updating files."""
    remote_version = get_remote_version()
    if not remote_version:
        return

    local_version = get_local_version()

    if local_version != remote_version:
        print(f"New version found: {remote_version}")
        files = fetch_files_from_directory(remote_version)
        if files:
            save_to_input_file(files)
            download_files_with_aria2(remote_version)
            save_local_version(remote_version)
            print(f"Updated input.txt with {len(files)} files and downloaded them.")
        else:
            print("No files found to update.")
    else:
        print("Local version is up-to-date.")


def check_for_static():
    local_static = get_local_static()
    if not local_static:
        print("Local static files not found.")
        files = fetch_files_from_directory("static")
        if files:
            save_to_input_file(files)
            download_files_with_aria2("static")
        else:
            print("No files found to update.")
    else:
        print("Local static files are up-to-date.")


if __name__ == "__main__":
    print(f'****Using {BASE_URL} as source.****')
    while True:
        check_for_updates()
        check_for_static()
        time.sleep(CHECK_INTERVAL_DAYS * 24 * 60 * 60)

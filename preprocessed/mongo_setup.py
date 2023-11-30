import os
import sys
import platform
import requests
from zipfile import ZipFile
from tarfile import TarFile


def download_and_install_mongodb(version):
    system_platform = platform.system().lower()

    if system_platform == "windows":
        download_url = f"https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-{version}.zip"
        install_dir = "C:\\Program Files\\MongoDB"
    elif system_platform == "linux":
        download_url = f"https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{version}.tgz"
        install_dir = "/usr/local/mongodb"
    elif system_platform == "darwin":
        download_url = f"https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-{version}.tgz"
        install_dir = "/usr/local/mongodb"
    else:
        print("Unsupported operating system")
        sys.exit(1)

    # Download MongoDB
    response = requests.get(download_url)
    if response.status_code == 200:
        with open("mongodb_archive", "wb") as archive_file:
            archive_file.write(response.content)
    else:
        print(f"Failed to download MongoDB. HTTP Status Code: {response.status_code}")
        sys.exit(1)

    # Extract the downloaded archive
    if download_url.endswith(".zip"):
        with ZipFile("mongodb_archive", "r") as zip_ref:
            zip_ref.extractall(install_dir)
    else:
        with TarFile.open("mongodb_archive", "r:gz") as tar_ref:
            tar_ref.extractall(install_dir)

    # Rename the MongoDB directory
    extracted_dir = os.path.join(install_dir, os.listdir(install_dir)[0])
    os.rename(extracted_dir, os.path.join(install_dir, "mongodb"))

    # Add MongoDB bin directory to the system PATH
    if system_platform == "windows":
        os.environ["PATH"] += f";{install_dir}\\mongodb\\bin"
    else:
        os.environ["PATH"] += f":{install_dir}/mongodb/bin"

    # Cleanup: remove the downloaded archive
    os.remove("mongodb_archive")

    print("MongoDB installation complete.")


if __name__ == "__main__": 

    mongodb_version = "7.0.3"
    download_and_install_mongodb(mongodb_version)

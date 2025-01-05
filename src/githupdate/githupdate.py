import requests
import os
import zipfile
import shutil
from packaging import version

class githupdate:
    def __init__(self, repo_owner, repo_name, dir2update=os.path.dirname(__file__), fext=".zip", download_path=os.path.dirname(__file__)+'\\GHP\\'):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.download_path = download_path
        self.api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
        self.dir2update = dir2update
        self.fext=fext
        os.makedirs(self.download_path, exist_ok=True)

    def get_latest_release(self):
        response = requests.get(self.api_url)
        response.raise_for_status()
        return response.json()

    def download_latest_release(self):
        release: dict = self.get_latest_release()
        assets = release.get('assets', [])
        if not assets:
            raise Exception('No assets found for the latest release.')
        fileext = self.fext
        zip_assets = [asset for asset in assets if asset['name'].endswith(fileext)]
        if not zip_assets:
            raise Exception('No zip files found for the latest release.')

        asset = zip_assets[0]
        download_url = asset['browser_download_url']
        zip_path = os.path.join(self.download_path, asset['name'])

        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        return zip_path

    def is_latest_version(self, current_version):
        release = self.get_latest_release()
        latest_version = release['tag_name']
        return version.parse(current_version) >= version.parse(latest_version)

    def extract_zip(self, file_path, extract_to):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(file_path)

    def update(self, current_version):
        extract_to=self.dir2update
        if self.is_latest_version(current_version):
            return
        file_path = self.download_latest_release()
        self.extract_zip(file_path, extract_to)
        shutil.rmtree(self.download_path)
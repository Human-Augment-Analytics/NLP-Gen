from urllib.request import urlretrieve
from pathlib import Path
class Downloader:

    def __init__(self, url: str):
        self.url = url
    
    def download(self, path: str, name: str) -> Path:
        file_path = Path(path) / name
        urlretrieve(self.url, str(file_path))
        return file_path
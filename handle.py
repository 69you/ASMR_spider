import os, requests, time
from typing import Any, Dict
from tqdm import tqdm

class info:
    def __init__(self, info: Dict[str, Any]) -> None:
        self.info = info

    def print_info(self):
        print('**************************  --------------------    --------------------  **************************')
        print(f"ID: {self.info['id']}")
        print(f"標題: {self.info['title']}")
        print(f"社團名: {self.info['name']}")
        print(f"NSFW: {self.info['nsfw']}")
        print(f"標籤: {', '.join(tag['name'] for tag in self.info['tags'])}")
        print('**************************  --------------------  Starting Download  --------------------  **************************')

class download:
    def __init__(self, id: str, tracks: Dict[str, Any], headers: Dict[str, str]) -> None:
        self.id = id
        self.tracks = tracks
        self.headers = headers

    def count(self):
        for folder in [_ for _ in self.tracks if _['type'] == 'folder']:
            folder_path = os.path.join('.', 'RJ{}'.format(self.id), folder['title'])
            os.mkdir(folder_path)

    def search(self, data, current_path):
        for item in data:
            if "type" in item:
                if item["type"] == "folder":
                    folder_path = os.path.join(current_path, item["title"])
                    os.makedirs(folder_path, exist_ok=True)
                    self.search(item["children"], folder_path)
                else:
                    self.download_file(item.get("mediaDownloadUrl"), current_path, item.get("title"))

    def download_file(self, url, folder: str, file: str):
        response = requests.get(
            url=url,
            headers=self.headers,
            stream=True
        )
        path = os.path.join(folder, file)
        size = int(response.headers.get('content-length', 0))

        config = {
            'unit': 'B',
            'unit_scale': True,
            'unit_divisor': 1024,
            'miniters': 1
        }
        print(r"Downloading {}/{}".format(folder.split("\\")[-1], file))
        progress = tqdm(total=size, **config)
        start = time.time()

        with open(path, 'wb') as file:
            for data in response.iter_content(1024):
                progress.update(len(data))
                file.write(data)

                elapsed = time.time() - start
                if elapsed > 0:
                    download_speed = len(data) / elapsed
                    progress.set_postfix(speed=f"{self.format_size(download_speed)}/s")

        progress.close()

    def format_size(self, size):
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

        for unit in units:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024


import os
from time import sleep
import requests

DEFAULT_PORT = 8008

class MetaDefenderApi(object):

    def __init__(self, ip, port=DEFAULT_PORT):
        self.ip = ip
        self.port = port

    def scan_file(self, file_path):
        data = self._get_file_data(file_path)
        headers = {
            "filename": os.path.basename(file_path)
        }
        post_url = f"http://{self.ip}:{self.port}/file"
        r = requests.post(post_url, data=data, headers=headers)
        data_id = r.json()['data_id']
        sleep(2)
        get_url = f"http://{self.ip}:{self.port}/file/{data_id}"
        r = requests.get(get_url)
        results = r.json()
        return results

    # -------------------------------------------------------------------------
    # Private

    def _get_file_data(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        return data
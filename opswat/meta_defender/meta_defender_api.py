
import os
from time import sleep
import requests
from concurrent.futures import ThreadPoolExecutor

DEFAULT_PORT = 8008
DELAY = 0.5
NUM_THREAD_WORKERS = 25


class MetaDefenderApi(object):

    def __init__(self, ip, port=DEFAULT_PORT):
        self.ip = ip
        self.port = port

    def scan_file(self, file_path):
        data_id = self._upload_file_for_processing(file_path)
        return self._get_results(data_id)

    def scan_directory(self, directory_path):
        file_paths = self._get_file_paths_in_dir(directory_path)
        executor = ThreadPoolExecutor(max_workers=NUM_THREAD_WORKERS)
        futures = []
        for file_path in file_paths:
            futures.append(executor.submit(self.scan_file, file_path))
        while any([(not future.done()) for future in futures]):
            sleep(DELAY)
        return [future.result() for future in futures]

    # -------------------------------------------------------------------------
    # Private

    def _get_file_data(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        return data

    def _upload_file_for_processing(self, file_path):
        data = self._get_file_data(file_path)
        headers = {
            "filename": os.path.basename(file_path)
        }
        post_url = f"http://{self.ip}:{self.port}/file"
        r = requests.post(post_url, data=data, headers=headers)
        data_id = r.json()['data_id']
        return data_id

    def _get_results(self, data_id):
        get_url = f"http://{self.ip}:{self.port}/file/{data_id}"
        r = requests.get(get_url)
        results = r.json()
        while results['scan_results']['progress_percentage'] < 100:
            sleep(DELAY)
            r = requests.get(get_url)
            results = r.json()
        return results

    def _get_file_paths_in_dir(self, directory_path):
        file_paths = []
        for subdir, dirs, files in os.walk(directory_path):
            for file in files:
                file_paths.append(os.path.join(subdir, file))
        return file_paths
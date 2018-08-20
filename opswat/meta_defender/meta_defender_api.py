
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

    # -------------------------------------------------------------------------
    # Public main high level functions

    def scan_file(self, file_path, batch_id=None):
        """Scans a single file and returns the results."""
        data_id = self.upload_file_for_scan(file_path, batch_id=batch_id)
        return self.get_scan_results(data_id)

    def scan_directory(self, directory_path):
        """Uses batch to scan all files in directory. Returns batch result."""
        file_paths = self._get_file_paths_in_dir(directory_path)
        batch_id = self.create_batch(user_data="user-data-123")
        self._upload_files(file_paths, batch_id)
        #self.close_batch(batch_id)
        results = self.get_batch_results(batch_id)
        self.close_batch(batch_id)
        return results

    # -------------------------------------------------------------------------
    # Public helper functions

    def create_batch(self, user_data=None):
        """Creates batch."""
        headers = {
            "user-data": user_data or ""
        }
        url = f"http://{self.ip}:{self.port}/file/batch"
        r = requests.post(url, headers=headers)
        batch_id = r.json()['batch_id']
        return batch_id

    def get_batch_status(self, batch_id):
        """Returns current status of batch."""
        get_url = f"http://{self.ip}:{self.port}/file/batch/{batch_id}"
        r = requests.get(get_url)
        status = r.json()
        return status

    def get_scan_status(self, data_id):
        """Returns current status of scan."""
        url = f"http://{self.ip}:{self.port}/file/{data_id}"
        r = requests.get(url)
        status = r.json()
        return status

    def get_scan_results(self, data_id):
        """Waits for scan to complete and returns the status."""
        results = self.get_scan_status(data_id)
        while results['scan_results']['progress_percentage'] < 100:
            sleep(DELAY)
            results = self.get_scan_status(data_id)
        return results

    def get_batch_results(self, batch_id):
        """Waits for batch to complete and returns the results."""
        results = self.get_batch_status(batch_id)
        while results['scan_results']['scan_all_result_a'] == "In Progress":
            print("Waiting for batch to complete...")
            print('---------------------------')
            for key, val in results.items():
                print(key)
                print(val)
            sleep(DELAY)
            results = self.get_batch_status(batch_id)

        return results

    def upload_file_for_scan(self, file_path, batch_id=None):
        data = self._get_file_data(file_path)
        headers = {
            "filename": os.path.basename(file_path)
        }
        if batch_id:
            headers["batch"] = batch_id
        url = f"http://{self.ip}:{self.port}/file"
        r = requests.post(url, data=data, headers=headers)
        data_id = r.json()['data_id']
        return data_id

    def close_batch(self, batch_id):
        """Closes batch."""
        url = f"http://{self.ip}:{self.port}/file/batch/{batch_id}/close"
        r = requests.post(url)
        response = r.json()
        return response

    # -------------------------------------------------------------------------
    # Private

    def _get_file_data(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        return data

    def _get_file_paths_in_dir(self, directory_path):
        file_paths = []
        for subdir, dirs, files in os.walk(directory_path):
            for file in files:
                file_paths.append(os.path.join(subdir, file))
        return file_paths

    def _upload_files(self, file_paths, batch_id):
        """Uses pool of threads to upload files for scan."""
        executor = ThreadPoolExecutor(max_workers=NUM_THREAD_WORKERS)
        futures = []
        for file_path in file_paths:
            futures.append(executor.submit(self.upload_file_for_scan,
                                           file_path, batch_id))
        while any([(not future.done()) for future in futures]):
            sleep(DELAY)
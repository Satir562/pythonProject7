from pprint import pprint

import requests


def get_token():
    with open("tokin.txt", "r") as file:
        return file.readline()


class YandexDisk:
    files_url = "https://cloud-api.yandex.net:443/v1/disk/resources/files"
    upload_url = " https://cloud-api.yandex.net:443/v1/disk/resources/upload"
    file_path = "dz_yndex.txt"


    def __init__(self, token):
        self.token = token

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def get_upload_link(self, file_path):
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(self.upload_url, params=params, headers=self.headers)
        pprint(response.json())
        return response.json()

    def upload(self, file_path):
        href = self.get_upload_link(file_path).get("href")
        if not href:
            return

        with open(file_path, "rb") as file:
            response = requests.put(href, data=file)
            if response.status_code == 201:
                print("Файл загружен")
                return True
            print('файл не загружен потому что', response.status_code)
            return False


yandex_client = YandexDisk(get_token())
yandex_client.upload("file.json")
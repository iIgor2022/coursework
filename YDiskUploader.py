import requests
from progress.bar import IncrementalBar

class YDiskUploader:
    def __init__(self, token):
        self.token = token

    def _get_header(self):
        return {"Content-Type": "application/json",
                'Authorization': "OAuth {}".format(self.token)}

    def _get_upload_link(self, filename):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": f"VKPhotos/{filename}", "overwrite": "true"}
        response = requests.get(upload_url, headers=self._get_header(), params=params)
        return response.json()

    def _create_folder(self):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": "VKPhotos"}
        return requests.put(url, headers=self._get_header(), params=params).status_code

    def _check_token(self):
        url = "https://cloud-api.yandex.net/v1/disk/resources/files"
        return requests.get(url, headers=self._get_header()).status_code

    def upload(self, vk, count_photo=5):
        if self._check_token() == 401:
            print("Неверный токен Яндекс.Диск")
            return
        pbar = IncrementalBar("Обработанно и загружено:", max=count_photo)
        list_photos = vk.get_list_photos()
        if list_photos is None:
            return
        if list_photos["response"]["count"] < count_photo:
            count_photo = list_photos["response"]["count"]
            pbar.max -= count_photo - list_photos["response"]["count"]
        list_photos = vk.processing_list_photos(list_photos, pbar)
        status = self._create_folder()
        if status != 201 and status != 409:
            pbar.finish()
            print("Ошибка создания папки на Яндекс.Диск")
        json_data = []
        for item in range(count_photo):
            href = self._get_upload_link(list_photos[item][1]).get("href", "")
            requests.put(href, data=vk.download(list_photos[item][2]["url"]))
            dict_json = {"file_name": list_photos[item][1], "size": list_photos[item][2]}
            json_data.append(dict_json)
            pbar.next()

        pbar.finish()
        return json_data
# from progress.bar import IncrementalBar
import requests
import datetime
import configparser


class VKDownloader:
    def __init__(self, id_user):
        self.token = ""
        self.id = id_user

    def _read_ini(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        try:
            config["VK"]
        except KeyError:
            print("В файле ini отсутствует ключ VK")
            return None
        try:
            config["VK"]["token"]
        except KeyError:
            print("В файле ini отсутствует ключ token")
            return None

        if config['VK']['token'] is not None:
            return config['VK']['token']
        else:
            print("Отсутствует значение ключа token в файле ini")
            return None

    def _requrement_params(self):
        return {"access_token": f"{self.token}", "v": "5.131"}

    def get_list_photos(self):
        self.token = self._read_ini()
        if self.token is None:
            return None

        url = "https://api.vk.com/method/users.get"
        params = {"user_ids": self.id}
        response = requests.get(url, params={**params, **self._requrement_params()})

        try:
            response.json()['response']
        except KeyError:
            print(response.json()["error"]["error_msg"])
            return None

        if len(response.json()['response']) == 0:
            print(f"Пользователь {self.id} не найден")
            return None

        user_id = response.json()["response"][0]["id"]
        url = "https://api.vk.com/method/photos.get"
        params = {"owner_id": user_id, "album_id": "profile", "extended": 1, "photo_sizes": 1}
        response = requests.get(url, params={**self._requrement_params(), **params})
        if response.status_code == 200:
            return response.json()

    def download(self, url):
        return requests.get(url)

    def processing_list_photos(self, list_photo, pbar):
        dict_photo = []
        photo_names = []
        pbar.max += list_photo["response"]["count"]
        for items in list_photo["response"]["items"]:
            list_photo = [0, "", {}]
            for i in items["sizes"]:
                size = int(i["height"]) * int(i["width"])
                if size > list_photo[0]:
                    list_photo[0] = size
                    list_photo[2] = i
            if f'{items["likes"]["count"]}.jpg' in photo_names:
                now = datetime.datetime.now()
                list_photo[1] = f'{items["likes"]["count"]}_{now.strftime("%d-%m-%Y")}.jpg'
            else:
                list_photo[1] = f'{items["likes"]["count"]}.jpg'
                photo_names.append(f'{items["likes"]["count"]}.jpg')
            dict_photo.append(list_photo)
            pbar.next()

        for item in range(len(dict_photo) - 1):
            for j in range(len(dict_photo) - 1 - item):
                if dict_photo[j + 1][0] > dict_photo[j][0]:
                    dict_photo[j], dict_photo[j + 1] = dict_photo[j + 1], dict_photo[j]

        return dict_photo

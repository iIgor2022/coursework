import json
import os
import YDiskUploader
import VKDownloader

def save_json(json_data):
    if json_data is None:
        return
    with open("vk_photos.json", "w") as file_object:
        json.dump(json_data, file_object)
        print(f"Создан файл {os.path.join(os.getcwd(), 'vk_photos.json')}")


def main():
    token = input("ВВедите токен Яндекс.Диск: ")
    if token == "":
        print("Отсутствует значение токена Яндекс.Диск")
        return
    vk_id = input("ВВдеите ник пользователя ВКонтакте: ")
    if token == "":
        print("Отсутствует ник ползователя ВКонтакте")
        return
    count_photos = input("Укажите количество фото, которые Вы хотите сохранить. \n"
                         "По умолчанию 5. Если хотите оставить это значение нажмите Enter: ")
    if count_photos != "":
        try:
            count_photos = int(count_photos)
        except ValueError:
            print(f"Указанное значение {count_photos} не является целым числом")
            return
    else:
        count_photos = 5
    vk = VKDownloader.VKDownloader(vk_id)
    yadisk = YDiskUploader.YDiskUploader(token)
    save_json(yadisk.upload(vk, count_photos))


if __name__ == "__main__":
    main()

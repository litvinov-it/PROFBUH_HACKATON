# pipenv install opencv-python

import cv2
from ..config import redis_db
import numpy as np

def create_screenshots(path_to_video, path_to_images, filename, ext, segments):

    # Читаем видео
    video = cv2.VideoCapture(f"{path_to_video}{filename}.{ext}")

    seg_num = len(segments)

    for idx, segment in enumerate(segments):
        time = int(segment["start"] * 1000)
        # Устанавливаем время для скриншоты
        video.set(cv2.CAP_PROP_POS_MSEC, time)

        # Считываем скриншот
        ret, frame = video.read()

        # Если скриншот считался
        if ret:
            image_name = f"{filename}_{time}.jpg"
            # Записываем скриншот в файл
            cv2.imwrite(f"{path_to_images}{image_name}", frame)
            segments[idx]["images"] = image_name

            # Записываем прогресс в базу
            redis_db.hset(filename, "progress", f"{(idx/seg_num)*100}")

    video.release()

    return segments


def create_screenshots_every_t_seconds(path_to_video, path_to_images, filename, ext, segments, scr_time, end_time):

    # Читаем видео
    video = cv2.VideoCapture(f"{path_to_video}{filename}.{ext}")

    seg_num = len(segments)

    for idx, segment in enumerate(segments):
        time = int(segment["start"] * 1000)
        done = False

        try:
            next_time = int(segments[idx+1]["start"] * 1000)
        except Exception:
            if end_time != -1:
                next_time = end_time * 1000
            else:
                next_time = np.inf

        print(time)
        print(next_time)
        print("-----")

        segments[idx]["images"] = []
        while(time < next_time and done != True):

            # Устанавливаем время для скриншота
            video.set(cv2.CAP_PROP_POS_MSEC, time)

            # Считываем скриншот
            ret, frame = video.read()

            # Если скриншот считался
            if ret:
                image_name = f"{filename}_{time}.jpg"
                # Записываем скриншот в файл
                cv2.imwrite(f"{path_to_images}{image_name}", frame)
                segments[idx]["images"].append(image_name)
            else:
                done = True

            time += scr_time

        # Записываем прогресс в базу
        redis_db.hset(filename, "progress", f"{(idx/seg_num)*100}")

    video.release()
    return segments

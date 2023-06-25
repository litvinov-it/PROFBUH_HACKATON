import os
os.system("clear")

# pipenv install pytube
# documentation - https://pytube.io/en/latest/

from pytube import YouTube

from ..config import redis_db


def get_youtube_video(video_id, folder_to_download, ext="mp4"):

    def download_progress(stream, data_chunk, bytes_remaining):
        percents = ((stream.filesize-bytes_remaining)*100) / stream.filesize
        # Обновляем прогресс загрузки видео
        redis_db.hset(video_id, "progress", percents)

    # Получаем объект - видео
    yt = YouTube(f"https://www.youtube.com/watch?v={video_id}", on_progress_callback=download_progress)

    # filter позволяет посмотреть какие потоки доступны
    # Для разных файлов могут быть доступны разные потоки
    # Такой фильтр выведет потоки только для аудио c расширением mp4
    # ! В проекте надо будет выбрать из этого списка тот, у которого
    # ! abr с самым маленьким числом
    stream_variants =  yt.streams.filter(only_audio=False, file_extension=ext)

    # TODO Надо будет сделать автоматический выбор потока
    # for variant in stream_audio_variants:
    #     print(variant)

    # Скачиваем видео. 22 - качество 720p - 25fps
    stream = yt.streams.get_by_itag(22)
    stream.download(output_path=folder_to_download, filename=f"{video_id}.{ext}")


    # Это странно, но функция возвращает название (title) видео
    return yt.title




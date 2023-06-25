# pipenv install nltk

from .Transcript import get_transcript_video, preporcess_transcript, get_raw_text, get_raw_transcript
from .RestorePunctuation import restore_punctuation
from .RestoreTimecodes import restore_timecodes, set_timecodes
from .YouTubeDownload import get_youtube_video
from .Paragraphs import rand_paragraphs
from .CreateScreenshots import create_screenshots, create_screenshots_every_t_seconds
from .GPT import create_abstract, edit_paragraph, get_paragraph_title
from ..config import redis_db
from ..schemas import ArticleStatus
import json
import os
import time

import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")


def create_article(pk: str, end_time: int):

####  Получение субтитров

    # Обновляем статус для задачи
    redis_db.hset(pk, "status", ArticleStatus.GETTING_SUBTITLES.value)

    # Получаем субтитры
    transcript, manual = get_transcript_video(pk)


#### Обрабатываем субтитры

    # Обновляем статус для задачи
    redis_db.hset(pk, "status", ArticleStatus.PROCESSING_SUBTITLES.value)

    # Очищаем субтитры
    transcript = preporcess_transcript(transcript)


    # Если субтитры автоматические, восстанавливаем пунктуацию
    if manual == False:
        # Получаем сырой текст
        raw_text = get_raw_text(transcript)

        # Получаем предложения на основе сырого текста
        sentences = restore_punctuation(raw_text)
        del raw_text

        # Восстанавливаем временные отметки в предложениях
        transcript_str_with_timecodes = restore_timecodes(transcript, sentences[0])
        del sentences

    # Если субтритры мануальные
    else:
        # Преобразуем сабы в строу с таймкодами
        transcript_str_with_timecodes = get_raw_transcript(transcript)


    # Разделяем строку с отметками таймкодов на предложения.
    sentences_with_timecodes = sent_tokenize(transcript_str_with_timecodes)
    del transcript_str_with_timecodes

    # Вытаскиваем таймкоды
    sentences = set_timecodes(sentences_with_timecodes)
    del sentences_with_timecodes


#### Формируем параграфы

    paragraphs = rand_paragraphs(sentences, 5)
    del sentences


#### Пишем аннотацию

    # Обновляем статус для задачи
    redis_db.hset(pk, "status", ArticleStatus.ARTICLE_PARAPHRASING.value)

    abstract = create_abstract( get_raw_text(paragraphs), 300 )

    redis_db.hset(pk, "abstract", abstract)

    print(abstract)


#### Редактируем абзацы и получаем заголовки для каждого абзаца (ограничение бесплатного gpt - 3 запроса в минуту)
    for idx, paragraph in enumerate(paragraphs):
        edited_paragraph = edit_paragraph(paragraph["text"])
        paragraphs[idx]["edited_text"] = edited_paragraph
        print(edited_paragraph)
        time.sleep(20)

        paragraph_title = get_paragraph_title(paragraph["text"])
        paragraphs[idx]["title"] = paragraph_title
        print(paragraph_title)
        time.sleep(20)

#### Скачиваем видео

    # Обновляем статус для задачи
    redis_db.hset(pk, "status", ArticleStatus.DOWNLOADING_VIDEO.value)

    # Папка для хранения видео
    path_to_video = "downloads/"
    # Расширение для видео
    ext = "mp4"
    # Папка для скриншотов
    path_to_images = "app/static/images/screenshots/"

    # Скачиваем видео с YouTube, чтобы сделать скриншоты
    # и получаем название видео
    title = get_youtube_video(pk, path_to_video, ext)

    # Записываем название видео в базу
    redis_db.hset(pk, "title", title)


#### Создаем скриншоты

    # Обновляем статус для задачи
    redis_db.hset(pk, "status", ArticleStatus.CREATING_SCREENSHOTS.value)

    # paragraphs = create_screenshots(path_to_video, path_to_images, pk, ext, paragraphs)
    paragraphs = create_screenshots_every_t_seconds(path_to_video, path_to_images, pk, ext, paragraphs, 5000, end_time)


    # Удаляем файл с видео
    os.remove(f"{path_to_video}{pk}.{ext}")


#### Сохраняем полученную статью в базу

    # Обновляем статус для задачи
    redis_db.hset(pk, "status", ArticleStatus.SAVING_ARTICLE.value)

    # Записываем в базу данных полученную статью
    # ensure_ascii=False, чтобы сохранялась читабельная кодировка

    redis_db.hset(pk, "article", json.dumps(paragraphs, ensure_ascii=False))

    # Сохранить полученную статью в файл
    # папка downloads должна быть создана в корне
    # with open(f"downloads/{pk}.json", "w", encoding='utf8') as file:
    #     file.write(json.dumps(sentences, ensure_ascii=False))

    # Обновляем статус для задачи
    redis_db.hset(pk, "status", ArticleStatus.FINISHED.value)



# pipenv install youtube-transcript-api

from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript_video(video_id):

    # Получаем список субтитров
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # Ищем русские субтитры
    transcript_ru = transcript_list.find_transcript(['ru'])

    # Проверяем, являются ли субтритры автоматическими
    if transcript_ru.is_generated == True:
        manual = False
    else:
        manual = True

    # Парсим субтитры
    transcript = transcript_ru.fetch()

    return (transcript, manual)

def preporcess_transcript(transcript):
    """
    Подготавливает текст.
    Очищает от постфиксов ([музыка], [смех]), знака '\n'
    """

    idx = 0
    while (idx < len(transcript)):

        # Делаем первичную обработку текста
        # - удаляем постфиксы: [музыка], [смех]
        # - заменяем знаки "\n", "♪" на пустоту
        # - Удаляем знак "-", обозначающий диалог
        # - и очищаем отлишних пробелов cпереди и сзади
        transcript[idx]["text"] = del_postscript(transcript[idx]['text']).replace('\n', ' ').replace('♪', '').strip(' - ').strip(' ')

        # Если сегмент оказался пустым, то удаляем его.
        if not transcript[idx]["text"]:
            transcript.pop(idx)
            idx -= 1

        idx += 1

    return transcript


def del_postscript(text):
    """
    Удаляет постфиксы: [музыка], [смех]
    """
    startPostcript = text.find('[')
    endPostcript = text.find(']')
    if startPostcript != -1 and endPostcript != -1:
        postcript = text[startPostcript:][:endPostcript + 1]
        text = text.replace(postcript, '')
    return text


def get_raw_text(transcript):

    raw_text = ""
    for segment in transcript:
        raw_text += f"{segment['text'].lower()} "

    return raw_text


def get_raw_transcript(transcript):
    # Функция преобразует субтитры (список сегментов)
    # в строку cо вставками таймкодов

    raw_transcript = ""
    for segment in transcript:
        raw_transcript += f"_{segment['start']} {segment['text']} "

    return raw_transcript


def get_raw_sentences(sentences):
    # Функция преобразует список предложений
    # в строку.

    raw_sentences = ""
    for segment in sentences:
        raw_sentences += f"{segment} "

    return raw_sentences

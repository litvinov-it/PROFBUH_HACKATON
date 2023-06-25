from .Transcript import get_raw_transcript, get_raw_sentences
import re

def restore_timecodes(transcript, sentences):
    # Функция получает на вход
    # transcript - субтитры (список сегментов(словарей))
    # sentences - список предложений с пунктуацией, но без таймкодов.

    # На выходе возвращаем строку cо вставками таймкодов

    # Получаем текстовую строку из субтитров с метками времени
    raw_transcript = get_raw_transcript(transcript)

    # Получаем текстовую строку из предложений с пунктуацией.
    raw_sentences = get_raw_sentences(sentences)


    # Преобразуем строки в массивы символов
    raw_transcript = list(raw_transcript.strip())
    raw_sentences = list(raw_sentences.strip())

    # Устанавливаем метки в строке с предложениями
    transcript_str_with_timecodes = clone_timecodes(raw_transcript, raw_sentences)

    # Удаляем ненужные объекты
    del raw_transcript
    del raw_sentences

    return transcript_str_with_timecodes



def clone_timecodes(raw_transcript, raw_sentences):
    idx_tr = 0
    idx_sent = 0
    while idx_tr < len(raw_transcript):
        if raw_transcript[idx_tr].lower() != raw_sentences[idx_sent].lower():
            if raw_transcript[idx_tr] == "_":
                while raw_transcript[idx_tr] != " ":
                    raw_sentences.insert(idx_sent, raw_transcript[idx_tr])
                    idx_tr += 1
                    idx_sent += 1

                raw_sentences.insert(idx_sent, " ")
                idx_sent += 1
            else:
                idx_sent += 1
                continue
        else:
            idx_sent += 1

        idx_tr += 1

    # Преобразуем массив в строку
    return ''.join(raw_sentences)


def set_timecodes(sentences_with_timecodes):
    # Функция получает на вход список предложений.
    # В предложениях расставлены метки таймкодов
    # На выходе - список словарей (сегментов по 1 предложению).

    sentences = []

    for sentence in sentences_with_timecodes:

        # Находим индекс первого вхождения символа "_"
        idx_start = sentence.find("_")
        # Находим индекс последнего вхождения символа "_"
        idx_end = sentence.rfind("_")

        # Если в предложении есть таймкод
        if idx_start != -1:

            # Если таймкод вначале предложения, то забираем его.
            # Иначе берем последний таймкод из предыдущего предложения
            if idx_start == 0:
                timecode = get_timecode(sentence, idx_start)
            else:
                timecode = previous_timecode

            # Предыдущий таймкод = последний таймкод в предложении
            previous_timecode = get_timecode(sentence, idx_end)

        # Если в предложении нет таймкода
        else:
            timecode = previous_timecode

        # Очищаем предложение от таймкодов
        sentence = re.sub(r"_[0-9]+.[0-9]+ ", "", sentence)

        # Добавляем отметку времени и предложение
        # в результирующий список словарей
        sentences.append({
            "start": float(timecode),
            "text": sentence
        })

    return sentences

def get_timecode(sentence, idx):
    idx = idx + 1
    timecode = ""
    while sentence[idx] != " ":
        timecode += sentence[idx]
        idx += 1
    return timecode


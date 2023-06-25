import random

def rand_paragraphs(sentences, min=5, max=None):
    # sentences - список словарей (предложения).
    # start - мин кол-во предложений в абзаце
    # max - макс кол-во предложений в абзаце

    # Возвращает список словарей (абзацы)

    paragraphs = []
    p_counter = 0
    p_idx = -1
    for sentence in sentences:
        if p_counter == 0:
            if max is None:
                p_counter = min
            else:
                p_counter = random.randint(min, max)
            p_idx += 1
            paragraphs.append({})
            paragraphs[p_idx]["start"] = sentence["start"]
            paragraphs[p_idx]["text"] = ""

        paragraphs[p_idx]["text"] += " "+sentence["text"]
        p_counter -= 1

    return paragraphs

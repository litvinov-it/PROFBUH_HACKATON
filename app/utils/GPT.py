# pipenv install openai
# import openai
from ..config import chat_gpt


def create_abstract(content, length):

    #! Заглушка на ограничение пол кол-ву токенов
    if len(content) > 12000:
        return "Пока видео слишком длинное, чтобы мы смогли сделать аннотацию. Не успели допилить этот функционал."

    completion = chat_gpt.openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f'Напиши аннотацию русском языке на текст. Вот текст: {content}'}
        ]
    )

    return completion.choices[0].message.content



def edit_paragraph(content):

    completion = chat_gpt.openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f'Отредактируй текст. Вот текст: {content}'}
        ]
    )

    return completion.choices[0].message.content


def get_paragraph_title(content):
    completion = chat_gpt.openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f'Сгенерируй заголовок на русском языке для текста: {content}'}
        ]
    )

    return completion.choices[0].message.content

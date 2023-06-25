# pip install redis

import redis
import openai

# библиотека для запуска переменных окружения из файла .env
from dotenv import load_dotenv

import os

# активируем переменные окружения из файла .env
load_dotenv()

# получаем значение переменной
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

redis_db = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    password=REDIS_PASSWORD
)

# Ключ API для ChatGPT
GPT_KEY=os.environ.get("GPT_KEY")

class chatGPT:
    def __init__(self, key):
        self.openai = openai
        self.openai.api_key = key

chat_gpt = chatGPT(GPT_KEY)
from pydantic import BaseModel
from .config import redis_db
from enum import Enum
from typing import List, Optional


class Paragraph(BaseModel):
    start: float
    text: str
    edited_text: str
    title: str
    images: List[str]


class Article(BaseModel):
    title: str
    abstract: str
    paragraphs: List[Paragraph]


class TaskBase(BaseModel):
    pk: str
    end_time: Optional[int] = -1
    class Meta:
        database: redis_db

class Task(TaskBase):
    status: int
    progress: float


class ArticleStatus(Enum):
    # Встали в очередь
    QUEUE_UP = 0

    # Получаем субтитры
    GETTING_SUBTITLES = 1

    # Обрабатываем субтитры
    PROCESSING_SUBTITLES = 2

    # Перефразируем предложения
    ARTICLE_PARAPHRASING = 3

    # Скачиваем видео
    DOWNLOADING_VIDEO = 4

    # Создаем скриншоты
    CREATING_SCREENSHOTS = 5

    # Готовим статью к отправке
    SAVING_ARTICLE = 6

    # Готово
    FINISHED = 200

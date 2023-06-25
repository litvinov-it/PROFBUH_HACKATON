from fastapi import APIRouter, BackgroundTasks
from .. import schemas
from ..config import redis_db
from ..utils.Article import create_article
from ..schemas import ArticleStatus

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", response_model=schemas.Task)
async def set_task(task: schemas.TaskBase, background_tasks: BackgroundTasks):

    task_info = redis_db.hmget(task.pk, ["status", "end_time", "progress"])

    # Если задачи не существует, то создаем ее
    if task_info[0] is None:

        status = ArticleStatus.QUEUE_UP.value
        progress = 0

        if task.end_time == -1:
            end_time = -1

        # Записываем в базу новую задачу
        redis_db.hset(task.pk, mapping={
            "pk": task.pk,
            "end_time": end_time,
            "status": status,
            "progress": progress
        })

        # Задаем время существования записи в 24 часа
        redis_db.expire(task.pk, 86400)


        # Отправляем задачу в фон
        background_tasks.add_task(create_article, task.pk, task.end_time)

    else:
        status = task_info[0]
        end_time = task_info[1]
        progress = task_info[2]

    new_task = schemas.Task(
        pk = task.pk,
        status = status,
        end_time = end_time,
        progress = progress
    )

    return new_task

@router.get("/{pk}", response_model=schemas.Task)
def get_task_status(pk: str):

    task_info = redis_db.hmget(pk, ["status", "end_time", "progress"])
    task = schemas.Task(
        pk = pk,
        status = task_info[0],
        end_time = task_info[1],
        progress = task_info[2]
    )

    return task


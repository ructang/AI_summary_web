from celery import Celery
from config import settings

celery = Celery('tasks',
                broker=settings.REDIS_URL,
                backend=settings.REDIS_URL)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
) 
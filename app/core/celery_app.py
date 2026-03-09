from celery import Celery

# Use Redis as broker and backend
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

celery_app = Celery(
    "zwiggy_tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

# IMPORTANT
celery_app.autodiscover_tasks(["app.events"])

# Optional: use JSON serialization
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)
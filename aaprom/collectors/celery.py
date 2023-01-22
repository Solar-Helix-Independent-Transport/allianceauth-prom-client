from prometheus_redis_client import Histogram, Counter
from ..utils import PowersOf

DEFAULT_CELERY_BUCKETS = (
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    15.0,
    30.0,
    45.0,
    60.0,
    90.0,
    120.0,
    150.0,
    180.0,
    210.0,
    240.0,
    270.0,
    300.0,
    600.0,
    float("inf"),
)

# *********************************************************************************************************
# Celery Models  ******************************************************************************************
# *********************************************************************************************************

tasks_published = Counter(
    'celery_tasks_published_total',
    'Count of published tasks',
    labelnames=['task']
)
tasks_retried = Counter(
    'celery_tasks_retried_total',
    'Count of retried tasks',
    labelnames=['task']
)
tasks_executed = Counter(
    'celery_tasks_executed_total',
    'Count of executed (finished) tasks',
    labelnames=['task', 'state']
)

task_duration = Histogram(
    'celery_task_duration_seconds',
    'Duration of task execution in seconds',
    labelnames=['task', 'state'],
    buckets=DEFAULT_CELERY_BUCKETS
)

from prometheus_redis_client import Histogram, Counter
from ..utils import PowersOf

DEFAULT_CELERY_BUCKETS = (
    0.200,
    0.400,
    0.600,
    0.800,
    1.000,
    2.000,
    3.000,
    4.000,
    5.000,
    10.00,
    20.00,
    30.00,
    60.00,
    120.0,
    float("inf")
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

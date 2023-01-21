
from celery.signals import (
    after_task_publish,
    task_postrun,
    task_prerun,
    task_retry
)

from .utils import Time, TimeSince

from .collectors.celery import (
    task_duration,
    tasks_executed,
    tasks_published,
    tasks_retried
)

task_start_time = None  # Used to measure task execution time

@after_task_publish.connect()
def on_after_task_publish(sender=None, headers=None, body=None, **kwargs):
    """Dispatched when a task has been sent to the broker.
    Note that this is executed in the process that sent the task.
    """
    try:
        task_name = headers['task']
    except:  # headers['task'] is not always available
        task_name = 'UNKNOWN'
    tasks_published.labels(task=task_name).inc()

@task_prerun.connect()
def on_task_prerun(*args, **kwargs):
    """Dispatched before a task is executed."""
    global task_start_time
    task_start_time = Time()

@task_postrun.connect()
def on_task_postrun(task, state, **kwargs):
    """Dispatched after a task has been executed."""
    task_state = state.lower()
    task_execution_time = TimeSince(task_start_time)
    task_name = task.__module__ + "." + task.__name__

    task_duration.labels(
        task=task_name,
        state=task_state,
    ).observe(task_execution_time)
    tasks_executed.labels(task=task_name, state=task_state).inc()

@task_retry.connect()
def on_task_retry(sender=None, **kwargs):
    """Dispatched when a task will be retried."""
    task_name = sender.__module__ + "." + sender.__name__  # sender is task
    tasks_retried.labels(task=task_name).inc()

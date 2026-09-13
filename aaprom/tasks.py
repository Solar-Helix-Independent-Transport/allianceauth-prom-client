import logging

from celery import shared_task
from django.apps import apps

logger = logging.getLogger(__name__)


@shared_task
def update_wh_mapper_gauges():
    """Refreshes the aa-wh-mapper active map/user gauges from the DB.

    Schedule this via CELERYBEAT_SCHEDULE (see README) - it's a no-op if
    aa-wh-mapper isn't installed.
    """
    if not apps.is_installed("wh_mapper"):
        return

    from wh_mapper.models import MapPresence

    from .collectors.wh_mapper import wh_mapper_active_maps, wh_mapper_active_users

    try:
        wh_mapper_active_maps.set(
            MapPresence.objects.values("map_id").distinct().count()
        )
        wh_mapper_active_users.set(
            MapPresence.objects.values("user_id").distinct().count()
        )
    except Exception as e:
        logger.error(e)

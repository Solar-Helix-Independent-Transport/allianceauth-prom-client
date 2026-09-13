import logging

from django.dispatch import receiver

from .collectors.wh_mapper import wh_mapper_map_event_total
from wh_mapper.signals import map_changed

logger = logging.getLogger(__name__)


@receiver(map_changed)
def wh_mapper_map_changed_callback(sender, map_id, event, data, user=None, **kwargs):
    logger.debug(
        f"AA-Prom-Exporter - wh_mapper map {map_id} - event {event} (user: {user})"
    )
    try:
        user_character_name = user.profile.main_character.character_name if user and hasattr(user, "profile") and hasattr(user.profile, "main_character") else None
        category, _, action = event.partition(".")
        wh_mapper_map_event_total.labels(
            category=category,
            action=action or "unknown",
            actor=user_character_name if user_character_name else "system",
        ).inc()
    except Exception as e:
        logger.error(e)

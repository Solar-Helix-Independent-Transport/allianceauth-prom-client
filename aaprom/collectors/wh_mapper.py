from aaprom.redis_metrics import Counter, CommonGauge

# *********************************************************************************************************
#    WH Mapper Models    **********************************************************************************
# *********************************************************************************************************

wh_mapper_map_event_total = Counter(
    'wh_mapper_map_event_total',
    'Count of aa-wh-mapper map_changed events by category, action and actor',
    labelnames=["category", "action", "actor"]
)

# Refreshed periodically by aaprom.tasks.update_wh_mapper_gauges (see the
# CELERYBEAT_SCHEDULE entry documented in the README) rather than pushed on
# every signal - counting distinct maps/users is a DB query, not something
# to run on every map_changed event. expire means a stalled/removed task
# makes these drop out of scrape output instead of reporting a stale count
# forever.
wh_mapper_active_maps = CommonGauge(
    "wh_mapper_active_maps",
    "Number of aa-wh-mapper maps with at least one open MapPresence (websocket) connection",
    expire=60 * 15
)

wh_mapper_active_users = CommonGauge(
    "wh_mapper_active_users",
    "Number of distinct users with at least one open MapPresence (websocket) connection",
    expire=60 * 15
)

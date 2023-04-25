from prometheus_redis_client import Counter

# *********************************************************************************************************
#    BOT Models    ****************************************************************************************
# *********************************************************************************************************

bot_slash_command = Counter(
    'bot_slash_command_total',
    'Slash commands run',
    labelnames=["command", "user", "guild"]
)

bot_tasks_executed = Counter(
    'bot_tasks_executed_total',
    'Count of executed (finished) tasks',
    labelnames=['task', 'state']
)

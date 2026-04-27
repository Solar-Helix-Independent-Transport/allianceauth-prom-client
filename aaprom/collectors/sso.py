from prometheus_redis_client import Histogram

DEFAULT_LATENCY_BUCKETS = (
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
#    SSO Models    ****************************************************************************************
# *********************************************************************************************************

sso_latency = Histogram(
    "sso_refresh_latency_by_status_seconds",
    "Histogram of sso refresh time by status.",
    labelnames=["status"],
    buckets=DEFAULT_LATENCY_BUCKETS
)

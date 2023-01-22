from prometheus_redis_client import Histogram

DEFAULT_LATENCY_BUCKETS = (
    0.025,
    0.05,
    0.075,
    0.1,
    0.15,
    0.2,
    0.25,
    0.3,
    0.35,
    0.4,
    0.45,
    0.5,
    0.55,
    0.6,
    0.65,
    0.7,
    0.75,
    0.8,
    0.85,
    0.9,
    0.95,
    1.0,
    1.5,
    2.0,
    2.5,
    3.0,
    3.5,
    4.0,
    4.5,
    5.0,
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

from prometheus_redis_client import Histogram, Counter, CommonGauge
from ..utils import PowersOf

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
    2.2,
    3.0,
    3.5,
    4.0,
    4.5,
    5.0,
    10.0,
    20,
    30,
    60,
    120,
    float("inf")
)

# *********************************************************************************************************
#    ESI Models    ****************************************************************************************
# *********************************************************************************************************

esi_bucket = Counter(
    'esi_request_total',
    'Esi Requests and response codes',
    labelnames=["endpoint", "status_code"]
)

esi_latency_by_endpoint = Histogram(
    "esi_requests_latency_by_endpoint_seconds",
    "Histogram of request processing time labelled by view.",
    labelnames=["endpoint", "status_code"],
    buckets=DEFAULT_LATENCY_BUCKETS
)

esi_error_bucket = CommonGauge(
    "esi_error_bucket_avail",
    "Errors remaining in the ESI error bucket"
)

esi_rate_bucket = CommonGauge(
    "esi_rate_bucket",
    "Rate bucket remaining",
    labelnames=["bucket"],
    expire=60*15
)
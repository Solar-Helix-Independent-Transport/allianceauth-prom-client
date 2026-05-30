from aaprom.redis_metrics import Histogram, Counter, CommonGauge

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
#    ESI Models    ****************************************************************************************
# *********************************************************************************************************

esi_bucket = Counter(
    'esi_request_total',
    'Esi Requests and response codes',
    labelnames=["endpoint", "status_code", "compatibility_date", "cache_status"]
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
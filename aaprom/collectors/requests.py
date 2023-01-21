from prometheus_redis_client import Histogram, Counter
from ..utils import PowersOf

# *********************************************************************************************************
# Request Models ******************************************************************************************
# *********************************************************************************************************

DEFAULT_LATENCY_BUCKETS = (
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    10.0,
    25.0,
    50.0,
    75.0,
    float("inf")
)

requests_total = Counter(
    "django_http_requests_before_middlewares_total",
    "Total count of requests before middlewares run."
)

responses_total = Counter(
    "django_http_responses_before_middlewares_total",
    "Total count of responses before middlewares run."
)

requests_latency_before = Histogram(
    "django_http_requests_latency_including_middlewares_seconds",
    (
        "Histogram of requests processing time (including middleware "
        "processing time)."
    ),
    buckets=DEFAULT_LATENCY_BUCKETS,
)

requests_unknown_latency_before = Counter(
    "django_http_requests_unknown_latency_including_middlewares_total",
    (
        "Count of requests for which the latency was unknown (when computing "
        "django_http_requests_latency_including_middlewares_seconds)."
    )
)

requests_latency_by_view_method = Histogram(
    "django_http_requests_latency_seconds_by_view_method",
    "Histogram of request processing time labelled by view.",
    labelnames=["view", "method"],
    buckets=DEFAULT_LATENCY_BUCKETS
)

requests_unknown_latency = Counter(
    "django_http_requests_unknown_latency_total",
    "Count of requests for which the latency was unknown."
)

# Set in process_request ******************************************************************************

requests_ajax = Counter(
    "django_http_ajax_requests_total",
    "Count of AJAX requests."
)

requests_by_method = Counter(
    "django_http_requests_total_by_method_total",
    "Count of requests by method.",
    labelnames=["method"]
)

requests_by_transport = Counter(
    "django_http_requests_total_by_transport_total",
    "Count of requests by transport.",
    labelnames=["transport"]
)

# Set in process_view     ******************************************************************************

requests_by_view_transport_method = Counter(
    "django_http_requests_total_by_view_transport_method_total",
    "Count of requests by view, transport, method.",
    labelnames=["view", "transport", "method"]
)

requests_body_bytes = Histogram(
    "django_http_requests_body_total_bytes",
    "Histogram of requests by body size.",
    buckets=PowersOf(2, 30)
)

# Set in process_template_response *********************************************************************

responses_by_templatename = Counter(
    "django_http_responses_total_by_templatename_total",
    "Count of responses by template name.",
    labelnames=["templatename"]
)

# Set in process_response       ************************************************************************

responses_by_status = Counter(
    "django_http_responses_total_by_status_total",
    "Count of responses by status.",
    labelnames=["status"]
)

responses_by_status_view_method = Counter(
    "django_http_responses_total_by_status_view_method_total",
    "Count of responses by status, view, method.",
    labelnames=["status", "view", "method"]
)

responses_body_bytes = Histogram(
    "django_http_responses_body_total_bytes",
    "Histogram of responses by body size.",
    buckets=PowersOf(2, 30)
)

responses_by_charset = Counter(
    "django_http_responses_total_by_charset_total",
    "Count of responses by charset.",
    labelnames=["charset"]
)

responses_streaming = Counter(
    "django_http_responses_streaming_total",
    "Count of streaming responses."
)

# Set in process_exception  ****************************************************************************

exceptions_by_type = Counter(
    "django_http_exceptions_total_by_type_total",
    "Count of exceptions by object type.",
    labelnames=["type"]
)

exceptions_by_view = Counter(
    "django_http_exceptions_total_by_view_total",
    "Count of exceptions by view.",
    labelnames=["view"]
)


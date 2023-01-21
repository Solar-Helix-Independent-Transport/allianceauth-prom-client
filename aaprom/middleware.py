from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from prometheus_redis_client import Counter, Histogram

from aaprom.utils import PowersOf, Time, TimeSince

from aaprom.collectors.requests import (
    requests_total,
    responses_total,
    requests_latency_before,
    requests_unknown_latency_before,
requests_latency_by_view_method,
requests_unknown_latency,
requests_unknown_latency,
requests_ajax,
requests_by_method,
requests_by_transport,
requests_by_view_transport_method,
requests_body_bytes,
responses_by_templatename,
responses_by_status,
responses_by_status_view_method,
responses_body_bytes,
responses_by_charset,
responses_streaming,
exceptions_by_type,
exceptions_by_view
)


class Metrics:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def register_metric(self, metric_cls, name, documentation, labelnames=(), **kwargs):
        return metric_cls(name, documentation, labelnames=labelnames, **kwargs)

    def __init__(self, *args, **kwargs):
        self.register()

    def register(self):
        self.requests_total = requests_total
        self.responses_total = responses_total
        self.requests_latency_before = requests_latency_before
        self.requests_unknown_latency_before = requests_unknown_latency_before
        self.requests_latency_by_view_method = requests_latency_by_view_method
        self.requests_unknown_latency = requests_unknown_latency

        # Set in process_request
        self.requests_ajax = requests_ajax
        self.requests_by_method = requests_by_method
        self.requests_by_transport = requests_by_transport

        # Set in process_view
        self.requests_by_view_transport_method = requests_by_view_transport_method
        self.requests_body_bytes = requests_body_bytes

        # Set in process_template_response
        self.responses_by_templatename = responses_by_templatename

        # Set in process_response
        self.responses_by_status = responses_by_status
        self.responses_by_status_view_method = responses_by_status_view_method
        self.responses_body_bytes = responses_body_bytes
        self.responses_by_charset = responses_by_charset
        self.responses_streaming = responses_streaming

        # Set in process_exception
        self.exceptions_by_type = exceptions_by_type
        self.exceptions_by_view = exceptions_by_view


class PrometheusBeforeMiddleware(MiddlewareMixin):
    """Monitoring middleware that should run before other middlewares."""

    metrics_cls = Metrics

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics = self.metrics_cls.get_instance()

    def process_request(self, request):
        self.metrics.requests_total.inc()
        request.prometheus_before_middleware_event = Time()

    def process_response(self, request, response):
        self.metrics.responses_total.inc()
        if hasattr(request, "prometheus_before_middleware_event"):
            self.metrics.requests_latency_before.observe(
                TimeSince(request.prometheus_before_middleware_event)
            )
        else:
            self.metrics.requests_unknown_latency_before.inc()
        return response


class PrometheusAfterMiddleware(MiddlewareMixin):
    """Monitoring middleware that should run after other middlewares."""

    metrics_cls = Metrics

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics = self.metrics_cls.get_instance()

    def _transport(self, request):
        return "https" if request.is_secure() else "http"

    def _method(self, request):
        m = request.method
        if m not in (
            "GET",
            "HEAD",
            "POST",
            "PUT",
            "DELETE",
            "TRACE",
            "OPTIONS",
            "CONNECT",
            "PATCH",
        ):
            return "<invalid method>"
        return m

    def label_metric(self, metric, request, response=None, **labels):
        return metric.labels(**labels) if labels else metric

    def process_request(self, request):
        transport = self._transport(request)
        method = self._method(request)
        self.label_metric(self.metrics.requests_by_method, request, method=method).inc()
        self.label_metric(
            self.metrics.requests_by_transport, request, transport=transport
        ).inc()

        # Mimic the behaviour of the deprecated "Request.is_ajax()" method.
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            self.label_metric(self.metrics.requests_ajax, request).inc()

        content_length = int(request.META.get("CONTENT_LENGTH") or 0)
        self.label_metric(self.metrics.requests_body_bytes, request).observe(
            content_length
        )
        request.prometheus_after_middleware_event = Time()

    def _get_view_name(self, request):
        view_name = "<unnamed view>"
        if hasattr(request, "resolver_match"):
            if request.resolver_match is not None:
                if request.resolver_match.view_name is not None:
                    view_name = request.resolver_match.view_name
        return view_name

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        transport = self._transport(request)
        method = self._method(request)
        if hasattr(request, "resolver_match"):
            name = request.resolver_match.view_name or "<unnamed view>"
            self.label_metric(
                self.metrics.requests_by_view_transport_method,
                request,
                view=name,
                transport=transport,
                method=method,
            ).inc()

    def process_template_response(self, request, response):
        if hasattr(response, "template_name"):
            self.label_metric(
                self.metrics.responses_by_templatename,
                request,
                response=response,
                templatename=str(response.template_name),
            ).inc()
        return response

    def process_response(self, request, response):
        method = self._method(request)
        name = self._get_view_name(request)
        status = str(response.status_code)
        self.label_metric(
            self.metrics.responses_by_status, request, response, status=status
        ).inc()
        self.label_metric(
            self.metrics.responses_by_status_view_method,
            request,
            response,
            status=status,
            view=name,
            method=method,
        ).inc()
        if hasattr(response, "charset"):
            self.label_metric(
                self.metrics.responses_by_charset,
                request,
                response,
                charset=str(response.charset),
            ).inc()
        if hasattr(response, "streaming") and response.streaming:
            self.label_metric(self.metrics.responses_streaming, request, response).inc()
        if hasattr(response, "content"):
            self.label_metric(
                self.metrics.responses_body_bytes, request, response
            ).observe(len(response.content))
        if hasattr(request, "prometheus_after_middleware_event"):
            self.label_metric(
                self.metrics.requests_latency_by_view_method,
                request,
                response,
                view=self._get_view_name(request),
                method=request.method,
            ).observe(TimeSince(request.prometheus_after_middleware_event))
        else:
            self.label_metric(
                self.metrics.requests_unknown_latency, request, response
            ).inc()
        return response

    def process_exception(self, request, exception):
        self.label_metric(
            self.metrics.exceptions_by_type, request, type=type(exception).__name__
        ).inc()
        if hasattr(request, "resolver_match"):
            name = request.resolver_match.view_name or "<unnamed view>"
            self.label_metric(self.metrics.exceptions_by_view, request, view=name).inc()
        if hasattr(request, "prometheus_after_middleware_event"):
            self.label_metric(
                self.metrics.requests_latency_by_view_method,
                request,
                view=self._get_view_name(request),
                method=request.method,
            ).observe(TimeSince(request.prometheus_after_middleware_event))
        else:
            self.label_metric(self.metrics.requests_unknown_latency, request).inc()

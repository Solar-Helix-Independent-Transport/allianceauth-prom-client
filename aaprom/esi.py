import logging
import json
from .collectors.esi import esi_bucket, esi_rate_bucket, esi_latency_by_endpoint, esi_error_bucket

from django.dispatch import receiver
from esi.signals import esi_request_statistics

logger = logging.getLogger(__name__)

@receiver(esi_request_statistics)
def esi_callback(sender, operation, status_code, headers, latency, bucket, **kwargs):
    # do stuff
    logger.debug(
        f"AA-Prom-Exporter - {operation} - Status Code: {status_code} in {latency}s (headers: {len(headers)})"
    )
    logger.debug(
        f"Headers: {json.dumps(dict(headers), indent=2)})"
    )
    ## Total Counts
    try:
        esi_bucket.labels(
        endpoint=operation,
        status_code=status_code
        ).inc()
    except Exception as e:
        logger.error(e)

    try:
        ## Latency
        esi_latency_by_endpoint.labels(
            endpoint=operation,
            status_code=status_code
        ).observe(latency)
    except Exception as e:
        logger.error(e)
    
    try:
        ## Global Error Rate
        if "x-esi-error-limit-remain" in headers:
            logger.debug(
                f"Global Limit - remain {headers.get('x-esi-error-limit-remain')}"
            )

            esi_error_bucket.set(int(headers.get('x-esi-error-limit-remain')))
    except Exception as e:
        logger.error(e)

    try:
        if bucket != "" and status_code > 0:
            logger.debug(
                f"Bucket: `{bucket}` - Remain: {headers.get('x-ratelimit-remaining')}"
            )
            esi_rate_bucket.labels(
                bucket=bucket,
            ).set(
                headers.get('x-ratelimit-remaining')
            )
    except Exception as e:
        logger.error(e)

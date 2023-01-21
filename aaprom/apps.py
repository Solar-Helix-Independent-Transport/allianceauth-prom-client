import redis
from django.apps import AppConfig
from django.conf import settings

from prometheus_redis_client import REGISTRY

# Load all the prom models
import aaprom

class AllianceAuthPrometheusConfig(AppConfig):
    name = aaprom.__name__
    verbose_name = f"Auth-Prometheus {aaprom.__version__}"

    def ready(self):
        """Initializes the Prometheus exports if they are enabled in the config.

        Note that this is called even for other management commands
        than `runserver`. As such, it is possible to scrape the
        metrics of a running `manage.py test` or of another command,
        which shouldn't be done for real monitoring (since these jobs
        are usually short-lived), but can be useful for debugging.
        """
        # Setup the redis link when everything is alive!
        REGISTRY.set_redis(redis.from_url(settings.PROMETHEUS_REDIS_URI))
        #load the celery tasks if we can
        try:
            import aaprom.celery
        except Exception as e:
            pass

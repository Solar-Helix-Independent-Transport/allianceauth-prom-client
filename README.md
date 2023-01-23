# Prom Exporter and Web Server for and Auth Instance with redis as a backend

```python
pip install prometheus-redis-client flask
pip install -U git+https://gitlab.com/aaronkable/django-esi.git@prom
wget https://raw.githubusercontent.com/Solar-Helix-Independent-Transport/allianceauth-prom-client/master/prom_exporter.py
```

local.py add:
```
PROMETHEUS_REDIS_URI = os.environ.get("PROMETHEUS_REDIS_URI", "redis://localhost:6379/3")
```

Update your middleware either override in local.py or base.py
```MIDDLEWARE = [
    'aaprom.middleware.PrometheusBeforeMiddleware',  # First
......... existing middlewears
    'aaprom.middleware.PrometheusAfterMiddleware',   # Last
]
```

use this command to run the metric endpoint. ( can be added as a new supervisor program )
```bash
gunicorn --bind localhost:8099 prom_exporter:app
```

add prometheus scrape config
```yaml
  - job_name: "auth"
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      - targets: ["localhost:8099"]
```

This module is a modified copy of
https://github.com/korfuri/django-prometheus
with parts taken from
https://github.com/prezi/django-exporter

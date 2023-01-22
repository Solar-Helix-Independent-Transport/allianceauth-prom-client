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
update your middleware either override in local.py or base.py
```MIDDLEWARE = [
    'aaprom.middleware.PrometheusBeforeMiddleware',  # First
......... existing middlewears
    'aaprom.middleware.PrometheusAfterMiddleware',   # Last
]
```
```bash
gunicorn --bind localhost:8099 prom_exporter:app
```

This module is a modified copy of
https://github.com/korfuri/django-prometheus
with parts taken from
https://github.com/prezi/django-exporter

# Prom Exporter and Web Server for and Auth Instance

```python
pip install prometheus-redis-client flask
pip install -U git+https://gitlab.com/aaronkable/django-esi.git@prom
wget https://raw.githubusercontent.com/Solar-Helix-Independent-Transport/allianceauth-prom-client/master/prom_exporter.py

PROMETHEUS_REDIS_URI = os.environ.get("PROMETHEUS_REDIS_URI", "redis://redis:6379/3")

```

```bash
gunicorn --bind localhost:8099 prom_exporter:app
```
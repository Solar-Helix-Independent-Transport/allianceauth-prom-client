# Auth Prom Exporter

Prom Exporter and Web Server for and Auth Instance with redis as a backend

## Why? 
Because metrics are sometimes very helpful!
## How?
- All esi requests throw a [signal](https://gitlab.com/allianceauth/django-esi/-/blob/master/esi/signals.py?ref_type=heads#L13) that this app catches and then the important data is stored in redis for export to the prometheus scraper.
- All Celery task stats (failed/success, time etc) are exported to metrics for the prometheus scraper.
- All Auth webpage metrics are are exported for the prometheus exporter.

### Install 
1. From your venv and in my auth
```
wget https://raw.githubusercontent.com/Solar-Helix-Independent-Transport/allianceauth-prom-client/master/prom_exporter.py
```

#### Baremetal 
```python
pip install prometheus-redis-client flask
pip install git+https://github.com/Solar-Helix-Independent-Transport/allianceauth-prom-client.git
```
#### Docker 
add to requirements.txt
```
prometheus-redis-client
flask
allianceauth-prometheus-exporter @ git+https://github.com/Solar-Helix-Independent-Transport/allianceauth-prom-client.git
```

2. in your `local.py` add:
```
PROMETHEUS_REDIS_URI = os.environ.get("PROMETHEUS_REDIS_URI", "redis://localhost:6379/3")
```
** Note the `/3` we are going to ue the 3rd database in redis for storage. **

3. in your `local.py`'s `INSTALLED_APPS` add:
```
    'aaprom',
```

4. add the following middleware override in `local.py`
```python
MIDDLEWARE = [
    'aaprom.middleware.PrometheusBeforeMiddleware', # run first
] + MIDDLEWARE + [
    'aaprom.middleware.PrometheusAfterMiddleware', # run last
]
```

5. use this command to run the metric endpoint. ( can be added as a new supervisor program, or docker compose container )
```bash
gunicorn --bind localhost:8099 prom_exporter:app
```

#### Example supervisor config
```conf
[program:prom_exporter]
user = allianceserver
directory=/home/allianceserver/myauth
command=/home/allianceserver/venv/bin/gunicorn --bind localhost:8099 prom_exporter:app
stdout_logfile=/home/allianceserver/myauth/log/prom_exporter.log
stderr_logfile=/home/allianceserver/myauth/log/prom_exporter.log
autostart=true
autorestart=true
stopsignal=INT
```

#### Example docker compose blocks
add this file to the volumes in the x-common for auth build
```yaml
  volumes:
...
    - ./conf/prom_exporter.py:/home/allianceauth/myauth/prom_exporter.py
...
```
add your app block to docker compose
```yaml
  auth_prom_exporter:
    ports:
      - 127.0.0.1:8099:8099
    container_name: auth_prom_exporter
    <<: *common-auth-build
    entrypoint: ["gunicorn","--bind=0.0.0.0:8099","--max-requests=10000","--workers=1","--log-level=debug","prom_exporter:app"]
```


## Setup Prom using the online guides.
add prometheus scrape config
```yaml
  - job_name: "auth"
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      - targets: ["localhost:8099"]
```


## Credits
This module is a modified copy of
https://github.com/korfuri/django-prometheus
with parts taken from
https://github.com/prezi/django-exporter

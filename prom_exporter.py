from flask import Flask
import redis
from prometheus_redis_client import REGISTRY, Counter

REGISTRY.set_redis(redis.from_url("redis://localhost:6379/3"))
ESI_BUCKET = Counter('esi_request', 'Esi Requests and response codes',
                     labelnames=["endpoint", "status_code"])

app = Flask(__name__)

@app.route("/metrics")
@app.route("/")
def prom_export():
    return REGISTRY.output()

if __name__ == "__main__":
    app.run()

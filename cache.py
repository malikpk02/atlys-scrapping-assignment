import json
import redis
from config import REDIS_HOST, REDIS_PORT


class RedisCache:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def write_to_cache(self, key, value, expiration=None):
        self.redis_client.set(key, json.dumps(value), ex=expiration)

    def read_from_cache(self, key):
        value = self.redis_client.get(key)
        return value and json.loads(value)

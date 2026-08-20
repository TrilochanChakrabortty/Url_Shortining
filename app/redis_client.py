import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
)


def get_redis():
    return redis_client
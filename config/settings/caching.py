import logging
import os

logger = logging.getLogger(__name__)


REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_DB = os.getenv("REDIS_DB", 1)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

if all([REDIS_PORT, REDIS_HOST, REDIS_DB, REDIS_PASSWORD]):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": REDIS_PASSWORD,
            },
        },
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        },
    }
    logger.warning("Redis cache is not configured.")

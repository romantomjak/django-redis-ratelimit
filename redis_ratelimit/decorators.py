from functools import wraps

import redis
from django.conf import settings
from django.http import HttpRequest

from redis_ratelimit.exceptions import RateLimited
from redis_ratelimit.utils import parse_rate, build_redis_key


def is_rate_limited(request, rate=None):
    if not rate:
        return False

    count, seconds = parse_rate(rate)
    redis_key = build_redis_key(request, count, seconds)

    db_url = getattr(settings, 'REDIS_RATELIMIT_DB_URL', "redis://localhost:6379/0")
    r = redis.from_url(db_url)

    current = r.get(redis_key)
    if current:
        current = int(current.decode('utf-8'))
        if current >= count:
            return True

    value = r.incr(redis_key)
    if value == 1:
        r.expire(redis_key, seconds)

    return False


def ratelimit(rate=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # CBV support
            if isinstance(args[0], HttpRequest):
                request = args[0]
            else:
                request = args[1]
            if is_rate_limited(request, rate=rate):
                raise RateLimited("Too Many Requests")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

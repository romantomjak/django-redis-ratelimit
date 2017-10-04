from functools import wraps

from redis_ratelimit.exceptions import RateLimited


def is_rate_limited():
    return True


def ratelimit():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if is_rate_limited():
                raise RateLimited("Too Many Requests")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

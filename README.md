# django-redis-ratelimit

[![Build Status](https://travis-ci.org/r00m/django-redis-ratelimit.svg?branch=master)](https://travis-ci.org/r00m/django-redis-ratelimit)

A fixed window rate limiting based on Redis

---

## Requirements

- Python >= 3.6
- Django >= 1.11
- Redis

## Installation

To install django-redis-ratelimit, simply:

```console
$ pip install django-redis-ratelimit
```

**NB!** django-redis-ratelimit requires a running Redis server. See [Redis's quickstart](http://redis.io/topics/quickstart)
 for installation instructions.

## Getting started

First, add the middleware to your `settings.py`:

```django
MIDDLEWARE = [
    # ...
    
    'redis_ratelimit.middleware.RateLimitMiddleware',
]
```

this will make sure that end user sees the HTTP 429 response.

Next, apply the `ratelimit` decorator to the view:

```django
from django.http import HttpResponse
from redis_ratelimit import ratelimit

@ratelimit(rate='5/m')
def index(request):
    return HttpResponse("Hello World!")
```

## Memory requirements

For this example we will assume that each key takes up roughly 250 bytes and each value is 4 bytes:

```
250 + 4 * 1 million unique hits = ~254 Megabytes
```

## Notes

- [Redis Rate Limiting Pattern #2](https://redis.io/commands/INCR#pattern-rate-limiter-2)

## License

MIT
# django-redis-ratelimit

[![Build Status](https://travis-ci.org/r00m/django-redis-ratelimit.svg?branch=master)](https://travis-ci.org/r00m/django-redis-ratelimit)

A sliding window rate limiting based on Redis

---

## Installation

To install django-redis-ratelimit, simply:

```
$ pip install django-redis-ratelimit
```

**NB!** django-redis-ratelimit requires a running Redis server. See [Redis's quickstart](http://redis.io/topics/quickstart)
 for installation instructions.

## Getting started

```
from django.http import HttpResponse
from redis_ratelimit import ratelimit


@ratelimit()
def index(request):
    return HttpResponse("Hello World!")

```

import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import resolve

rate_re = re.compile('([\d]+)/([\d]*)([smhd])')

UNITS = {
    's': 1,
    'm': 60,
    'h': 60 * 60,
    'd': 24 * 60 * 60
}


def parse_rate(rate):
    try:
        count, factor, unit = rate_re.match(rate).groups()
        count = int(count)
        seconds = UNITS[unit.lower()]
        if factor:
            seconds *= int(factor)
        return count, seconds
    except ValueError:
        raise ImproperlyConfigured("Invalid rate value")


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def build_redis_key(request, count, seconds):
    view_path = resolve(request.path).view_name
    ip = get_ip(request)
    prefix = getattr(settings, 'REDIS_RATELIMIT_PREFIX', "REDIS_RATELIMIT")
    return "{}/{}/{}/{}/{}".format(prefix, ip, view_path, count, seconds)

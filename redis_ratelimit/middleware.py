from django.http import HttpResponse

from redis_ratelimit.exceptions import RateLimited


class RateLimitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if not isinstance(exception, RateLimited):
            return None
        return HttpResponse("Too Many Requests", status=429)

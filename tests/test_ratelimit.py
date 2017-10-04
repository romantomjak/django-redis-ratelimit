from django.test import RequestFactory, TestCase

from redis_ratelimit import ratelimit
from redis_ratelimit.exceptions import RateLimited

factory = RequestFactory()


class RateLimitTests(TestCase):

    def test_method_decorator(self):
        @ratelimit()
        def view(request):
            return True

        req = factory.get('/')
        with self.assertRaises(RateLimited):
            view(req)

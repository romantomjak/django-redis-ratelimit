from django.conf.urls import url
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from django.views import View

from redis_ratelimit import ratelimit
from redis_ratelimit.exceptions import RateLimited
from redis_ratelimit.utils import parse_rate

factory = RequestFactory()


class RateParsingTests(TestCase):
    def test_rate_parsing(self):
        tests = (
            ('100/s', (100, 1)),
            ('100/10s', (100, 10)),
            ('100/m', (100, 60)),
            ('400/10m', (400, 10 * 60)),
            ('600/h', (600, 60 * 60)),
            ('800/d', (800, 24 * 60 * 60)),
        )

        for input, output in tests:
            assert output == parse_rate(input)


class DecoratorTests(TestCase):
    def test_no_rate(self):
        @ratelimit()
        def view(request):
            return True

        req = factory.get('/')
        assert view(req)


class RateLimitTests(TestCase):
    def test_method_decorator(self):
        @ratelimit(rate='5/s')
        def view(request):
            return True

        class DynamicUrlPattern:
            urlpatterns = [url(r'', view)]

        with override_settings(ROOT_URLCONF=DynamicUrlPattern):
            for _ in range(5):
                req = factory.get('/')
                view(req)

            with self.assertRaises(RateLimited):
                req = factory.get('/')
                view(req)

    def test_cbv_decorator(self):
        class Cbv(View):
            @ratelimit(rate='5/s')
            def get(self, request):
                return True

        class DynamicUrlPattern:
            urlpatterns = [url(r'', Cbv.as_view())]

        with override_settings(ROOT_URLCONF=DynamicUrlPattern):
            for _ in range(5):
                req = factory.get('/')
                Cbv.as_view()(req)

            with self.assertRaises(RateLimited):
                req = factory.get('/')
                Cbv.as_view()(req)

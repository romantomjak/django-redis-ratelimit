SECRET_KEY = "redis_ratelimit"

INSTALLED_APPS = (
    'redis_ratelimit',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Configuration of project ovveride here
ALLOWED_HOSTS = ["*"]
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "Blog_App",
        "USER": "postgres",
        "PASSWORD": "postgres_db",
        "HOST": "localhost",
        "PORT": "5432",
        "ATOMIC_REQUESTS": True,
    }
}


HOST = "http://localhost:8000"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "blog"
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

import mimetypes

mimetypes.add_type("application/javascript", ".js", True)
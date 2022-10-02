import ast
import os
import secrets
from pathlib import Path

import dj_database_url
import dotenv
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# from .django_logging import LOGGING

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_urlsafe(20)

if not os.path.exists(BASE_DIR / "logs"):
    os.makedirs(BASE_DIR / "logs")

dotenv_file = BASE_DIR / ".env"
ENV_EXISTS = os.path.isfile(dotenv_file)
if ENV_EXISTS:

    dotenv.load_dotenv(dotenv_file)

    if not os.path.exists(BASE_DIR / "media"):
        os.makedirs(BASE_DIR / "media")

    PRODUCTION_SERVER = False
    ALLOWED_HOSTS = ["*"]
    DATABASES = {
        "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
    }

else:
    PRODUCTION_SERVER = True

    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    DATABASES = {
        "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
    }
    ALLOWED_HOSTS = ["*"]

SENTRY_URL = os.environ["SENTRY_URL"]

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    integrations=[DjangoIntegration(), RedisIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

# Application definition

INSTALLED_APPS = [
    "main.apps.MainConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "django_admin_listfilter_dropdown",
    "colorfield",
    "compressor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]

ROOT_URLCONF = "puja.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "puja.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DEBUG = ast.literal_eval(
    os.environ.get("DEBUG", "False").strip("\n").capitalize())
if not DEBUG:
    MIDDLEWARE = ([MIDDLEWARE[0]] +
                  ["whitenoise.middleware.WhiteNoiseMiddleware"] +
                  MIDDLEWARE[1:])
    INSTALLED_APPS = (INSTALLED_APPS[0:-1] +
                      ["whitenoise.runserver_nostatic"] + [INSTALLED_APPS[-1]])
elif ast.literal_eval(
        os.environ.get("WHITENOISE", "True").strip("\n").capitalize()):
    MIDDLEWARE = ([MIDDLEWARE[0]] +
                  ["whitenoise.middleware.WhiteNoiseMiddleware"] +
                  MIDDLEWARE[1:])
    INSTALLED_APPS = (INSTALLED_APPS[0:-1] +
                      ["whitenoise.runserver_nostatic"] + [INSTALLED_APPS[-1]])

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

CELERY_TIMEZONE = TIME_ZONE = "Asia/Calcutta"

USE_TZ = True

USE_L10N = True

USE_I18N = True

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = os.environ.get("CLOUDAMQP_URL", "amqp://localhost")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

WHITENOISE_MAX_AGE = 9000
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = []

if os.path.isdir(MEDIA_ROOT):
    pass
else:
    os.mkdir(MEDIA_ROOT)

# # Deployment check
if PRODUCTION_SERVER:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION":
        os.environ.get("REDIS_URL", "redis://127.0.0.1:6379"
                       ),  # expected port, otherwise you can alter it
    }
}

if os.getenv("DATABASE_URL")[0] == "m":
    DATABASES["default"]["OPTIONS"] = {
        "init_command": "SET default_storage_engine=InnoDB",
    }

LANGUAGES = (
    ("bn", _("Bengali")),
    ("en", _("English")),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"), )

HOMECOMING = os.environ.get("HOMECOMING")
SHASHTI = os.environ.get("SHASHTI")
SAPTAMI = os.environ.get("SAPTAMI")
ASHTAMI = os.environ.get("ASHTAMI")
NAVAMI = os.environ.get("NAVAMI")
DASHAMI = os.environ.get("DASHAMI")
TEST = os.environ.get("TEST")
TOKEN = os.environ.get("TOKEN")

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_PRECOMPILERS = (
    ("text/x-sass", "django_libsass.SassCompiler"),
    ("text/x-scss", "django_libsass.SassCompiler"),
)
COMPRESS_CSS_HASHING_METHOD = "content"
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": [
        "compressor.filters.jsmin.JSMinFilter",
    ],
}
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False
DJANGO_ALLOW_ASYNC_UNSAFE = True

SESSION_COOKIE_AGE = 1 * 60 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# LOGGING = LOGGING

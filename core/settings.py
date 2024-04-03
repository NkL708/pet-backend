import os
from datetime import timedelta
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

# Environment
load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("PRODUCTION") == "False"

# Django
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
ROOT_URLCONF = "core.urls"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
WSGI_APPLICATION = "core.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# REST
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# Database
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": "5432",
    }
}

# Auth
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        )
    },
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
}

# Outer requests
ALLOWED_HOSTS = ["localhost", os.getenv("SERVER_IP")]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost",
    f"http://{os.getenv('SERVER_IP')}",
]

# Sentry
if not DEBUG:
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        send_default_pii=True,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

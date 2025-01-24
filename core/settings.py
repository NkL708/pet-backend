import os
from pathlib import Path

import sentry_sdk
import yaml
from celery.schedules import crontab
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

# ================================== ENVIRONMENT =================================
load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("PRODUCTION") == "False"

BASE_DIR = Path(__file__).resolve().parent.parent

# ================================== DJANGO CORE SETTINGS ========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Novosibirsk"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
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

# ================================== LOGGING =====================================
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

# ================================== DATABASE ====================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": "5432",
    }
}

# ================================== AUTH ========================================
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

# ========================== EXTERNAL (CORS / ALLOWED_HOSTS) ======================
ALLOWED_HOSTS = ["localhost", os.getenv("SERVER_HOST")]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost",
    f"http://{os.getenv('SERVER_HOST')}",
]

# ================================== SENTRY ======================================
if not DEBUG:
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN_BACKEND"),
        integrations=[DjangoIntegration()],
        send_default_pii=True,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

# ================================== CELERY ======================================
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

CELERY_BROKER_TRANSPORT_OPTIONS = {
    "visibility_timeout": 600,
    "retry_policy": {"timeout": 30.0},
}

schedule_path = os.path.join(BASE_DIR, "core", "schedule.yml")


def parse_cron_expr(cron_expr: str):
    fields = cron_expr.split()
    return crontab(
        minute=fields[0],
        hour=fields[1],
        day_of_month=fields[2],
        month_of_year=fields[3],
        day_of_week=fields[4],
    )


with open(schedule_path) as f:
    raw_schedule = yaml.safe_load(f)
    for key, value in raw_schedule.items():
        if "schedule" in value:
            value["schedule"] = parse_cron_expr(value["schedule"])
    CELERY_BEAT_SCHEDULE = raw_schedule

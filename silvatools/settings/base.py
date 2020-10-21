"""
Django settings for silvatools project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import django_heroku
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "q3__boklai^nrseqwoxswt^#d9d^z^08egwm9kcqw0^o#xo0dh"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "silvatools",
    "prac.apps.PracConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silvatools.middlewares.RequestLoggerMiddleware",
]

ROOT_URLCONF = "silvatools.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "silvatools.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# DATABASES = {'default': None}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "NAME": "silvatools",
        "USER": "silva",
        "PASSWORD": "silva",
        "CONN_MAX_AGE": 0,
        "PORT": "3310",
        "ATOMIC_REQUEST": True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = ()

LOGGING = {
    "disable_existing_loggers": False,
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "[%(levelname)s]\t(%(asctime)s) %(message)s"},
        "custom": {
            "format": "[%(levelname)s] (%(asctime)s) %(filename)s(%(lineno)d): %(message)s"
        },
    },
    "handlers": {
        "base": {  # 기본 로깅
            "level": "DEBUG",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "logs/daily.log",
            "formatter": "custom",
            "encoding": "utf-8",
        },
        "console": {  # log messages to terminal
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "script": {  # 모든 스크립트 로그 by "runscript" command
            "level": "DEBUG",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "logs/scripts.log",
            "formatter": "custom",
            "encoding": "utf-8",
        },
        "request": {  # 모든 요청 URL 과 입력 Param 을 남긴다
            "level": "DEBUG",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "logs/requests.log",
            "formatter": "simple",
            "encoding": "utf-8",
        },
        "redis": {  # 모든 Redis 관련 Read & Write 기록
            "level": "DEBUG",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "logs/redis.log",
            "formatter": "simple",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            "level": "DEBUG",
            "handlers": ["console", "base"],
            "propagate": False,  # this tells logger to send logging message
            # to its parent (will send if set to True)
        },
        "django.template": {"level": "INFO", "handlers": ["console"]},
        "django.utils.autoreload": {"level": "INFO", "handlers": ["console"]},
        "django": {
            "level": "DEBUG",
            "handlers": ["console", "base"],
            "propagate": False,
        },
        "scripts": {"level": "DEBUG", "handlers": ["script"], "propagate": False},
        "request": {"level": "DEBUG", "handlers": ["request"], "propagate": False},
        "redis": {"level": "DEBUG", "handlers": ["redis"], "propagate": False},
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

django_heroku.settings(locals())

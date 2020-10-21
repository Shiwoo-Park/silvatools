from silvatools.settings.local import *  # noqa (block erase)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "NAME": "silvatools",
        "USER": "root",
        "PASSWORD": "root",
        "CONN_MAX_AGE": 0,
        "PORT": "3401",
        "ATOMIC_REQUEST": True,
    }
}

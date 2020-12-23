from silvatools.settings.local import *  # noqa (block erase)

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

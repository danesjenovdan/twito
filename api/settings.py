import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'twito.sqlite3',
    }
}

INSTALLED_APPS = (
    'stats',
)

SECRET_KEY = os.getenv('SECRET_KEY', 'THIS_SHOULD_BE_SECRET')

import os
from logging.config import dictConfig

DMI_TCAT_USERNAME = os.getenv('DMI_TCAT_USERNAME')
DMI_TCAT_PASSWORD = os.getenv('DMI_TCAT_PASSWORD')

CACHE_CONFIG = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 30 * 24 * 60 * 60,  # 30 days
}

DATABASES = {
    'default': ({
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('SECRET_DB_NAME', ''),
        'USER': os.getenv('SECRET_DB_USERNAME', ''),
        'PASSWORD': os.getenv('SECRET_DB_PASSWORD', ''),
        'HOST': os.getenv('POSTGRESQL_SERVICE_HOST', ''), # this relies on postgresql being names properly on the cluster
        'PORT': '5432',
    } if os.getenv('APP_ENV', 'development') == 'production' else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('DB_URL', 'twito.sqlite3'),
    })
}

USE_TZ=True

INSTALLED_APPS = (
    'tweets',
)

redis_password = os.getenv('REDIS_PASSWORD', '')
redis_host = os.getenv('REDIS_MASTER_SERVICE_HOST', 'redis')

CELERY_CONFIG = {
    'BROKER_URL': f"redis://default:{redis_password}@{redis_host}",
    'RESULT_BACKEND': f"redis://default:{redis_password}@{redis_host}",
}

SECRET_KEY = os.getenv('SECRET_KEY', 'THIS_SHOULD_BE_SECRET')

# set logging configuration
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

import os
from logging.config import dictConfig

DMI_TCAT_USERNAME = os.getenv('DMI_TCAT_USERNAME')
DMI_TCAT_PASSWORD = os.getenv('DMI_TCAT_PASSWORD')

CACHE_CONFIG = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 30 * 24 * 60 * 60, # 30 days
}

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

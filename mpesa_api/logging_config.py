import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} - {message}',
            'style': '{',
        },
    },

    'handlers': {
        'mpesa_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'mpesa.log'),
            'formatter': 'verbose',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'mpesa': {
            'handlers': ['console', 'mpesa_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

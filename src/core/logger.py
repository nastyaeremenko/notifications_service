from core.settings import LOG_LEVEL

LOG_DEFAULT_HANDLERS = [
    'console',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(funcName)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'default': {
            '()': 'uvicorn._logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn._logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'services': {
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {'handlers': LOG_DEFAULT_HANDLERS, 'level': LOG_LEVEL},
        'uvicorn.error': {'level': 'WARNING'},
        'uvicorn.access': {'handlers': ['access'], 'level': 'INFO', 'propagate': False},
    },
    'root': {
        'level': LOG_LEVEL,
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}

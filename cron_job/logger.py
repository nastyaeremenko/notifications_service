LEVEL_LOG = 'INFO'

LOG_CONFIG = {
    'version': 1,
    'root': {
        'handlers': ['console'],
        'level': LEVEL_LOG,
    },
    'handlers': {
        'console': {
            'formatter': 'std_out',
            'class': 'logging.StreamHandler',
            'level': LEVEL_LOG,
        },
    },
    'formatters': {
        'std_out': {
            'format': '%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(message)s',
            'datefmt': '%d-%m-%Y %I:%M:%S',
        },
    },
}

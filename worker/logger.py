import logging
import sys


def configure_logger():
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        stream=sys.stdout)

import argparse
import os
import re
from logging import getLogger

import core.settings as s

MIGRATION_RE = re.compile(r'V(?P<num>\d{4})__[^.]+\.sql')

LOGGER = getLogger('manage.py')

COMMANDS = ('migrate', 'create_migration', 'run_server')


def migrate(_):
    conn_str = ' '.join([f"host={s.POSTGRES_DB_HOST}",
                         f"port={s.POSTGRES_DB_PORT}",
                         f"dbname={s.POSTGRES_DB_NAME}",
                         f"user={s.POSTGRES_DB_USER}",
                         f"password={s.POSTGRES_DB_PASSWORD}"])
    os.system(f'pgmigrate -d db/ -c "{conn_str}" -t latest migrate')


def create_migration(args):
    if not args.migration_name:
        LOGGER.exception("Error: no migrations name supplied")
        exit(1)
    migrations = sorted(f for f in os.listdir("db/migrations/") if f.endswith('.sql'))
    last_migration_num = int(MIGRATION_RE.search(migrations[-1])['num']) if migrations else 0
    migration_n = str(last_migration_num + 1).zfill(4)
    migration = f'V{migration_n}__{args.migration_name}.sql'
    try:
        with open(f'db/migrations/{migration}', 'w'):
            LOGGER.debug(msg=f'CREATED: {migration} in conf/db_schema/migrations/')
    except Exception as ex:
        LOGGER.exception(msg=f"Error: cant create migrations.\n ERROR: {ex}")
        exit()


def run_server(_):
    os.system('python main.py')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Management CLI for notification-service")
    parser.add_argument('command', metavar='CMD', type=str, nargs='?',
                        help='Command', choices=COMMANDS)
    parser.add_argument('-m', dest='migration_name', action='store',
                        help='Migration name (for create_migration command)', default='')

    args = parser.parse_args()
    if not args.command:
        LOGGER.exception("Error: no command supplied")
        exit(1)
    globals()[args.command](args)

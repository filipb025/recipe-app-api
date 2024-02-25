"""
Django command to wait for DB connection
"""
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.db import connections


# class Command(BaseCommand):
#     """ Django command to wait for database connection """
#
#     def handle(self, *args, **options):
#         """ Entry point to command. """
#         self.stdout.write('Waiting for database...')
#         db_up = False
#         while db_up is False:
#             try:
#                 self.check(databases=['default'])
#                 db_up = True
#             except (Psycopg2OpError, OperationalError):
#                 self.stdout.write('Database unavailable, waiting 1 second...')
#                 time.sleep(2)
#         self.stdout.write(self.style.SUCCESS('Database available!'))


class Command(BaseCommand):
    """Django command to wait for the database to be available."""

    def add_arguments(self, parser):
        parser.add_argument('--timeout', type=int, default=30, help='Seconds to wait for the database.')

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        start_time = time.time()
        timeout = options['timeout']
        db_conn = None
        while not db_conn:
            try:
                connection = connections['default']
                connection.ensure_connection()
                db_conn = True
                self.stdout.write(self.style.SUCCESS('Database available!'))
            except OperationalError as e:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
                if time.time() - start_time > timeout:
                    self.stdout.write(self.style.ERROR('Database was not available within the timeout period.'))
                    break
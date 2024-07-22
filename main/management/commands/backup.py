"""
 Command for backup database
"""

import os
import time

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Backup database. Only Mysql and Postgresql engines are implemented"
    requires_system_checks = output_transaction = requires_migrations_checks = True

    def handle(self, *args, **options):
        from django.conf import settings

        self.engine = settings.DATABASES["default"]["ENGINE"]
        self.db = settings.DATABASES["default"]["NAME"]
        self.user = settings.DATABASES["default"]["USER"]
        self.passwd = settings.DATABASES["default"]["PASSWORD"]
        self.host = settings.DATABASES["default"]["HOST"]
        self.port = settings.DATABASES["default"]["PORT"]

        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        outfile = os.path.join(backup_dir,
                               "backup_%s.sql" % time.strftime("%y%m%d%S"))

        if self.engine in ("mysql", "django.db.backends.mysql"):
            print(f"Doing Mysql backup to database {self.db} into {outfile}")
            self.do_mysql_backup(outfile)
        elif self.engine in (
                "postgresql_psycopg2",
                "postgresql",
                "django.db.backends.postgresql_psycopg2",
                "django.db.backends.postgresql",
        ):
            print(
                f"Doing Postgresql backup to database {self.db} into {outfile}"
            )
            self.do_postgresql_backup(outfile)
        else:
            print(f"Backup in {self.engine} engine not implemented")

    def do_mysql_backup(self, outfile):
        args = []
        if self.user:
            args += ["--user=%s" % self.user]
        if self.passwd:
            args += ["--password=%s" % self.passwd]
        if self.host:
            args += ["--host=%s" % self.host]
        if self.port:
            args += ["--port=%s" % self.port]
        args += [self.db]

        os.system("mysqldump %s > %s" % (" ".join(args), outfile))

    def do_postgresql_backup(self, outfile):
        os.popen(
            f"pg_dump --dbname=postgres://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.db} > {outfile}"
        )
        print("Database backed up succesfully")

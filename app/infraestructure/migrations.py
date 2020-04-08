import logging
from infraestructure import config
from yoyo import read_migrations  # type: ignore
from yoyo import get_backend  # type: ignore

DB_CONF = config.Database()


class Migrations():
    def __init__(self):
        self.log = logging.getLogger('database')
        date_format = """%(asctime)s,%(msecs)d %(levelname)-2s """
        info_format = """[%(filename)s:%(lineno)d] %(message)s"""
        log_format = date_format + info_format
        logging.basicConfig(format=log_format, level=logging.INFO)

    # migrate process migrations scripts and update db
    def migrate(self):
        self.log.info("Setting up Migrations")
        backend = get_backend(self._getConnection())
        migrations = read_migrations(DB_CONF.migrations)
        with backend.lock():
            try:
                new_migrations = backend.to_apply(migrations)
                if len(new_migrations) <= 0:
                    self.log.info('Migrations are up to date')
                    return
                # Apply any new migrations
                backend.apply_migrations(backend.to_apply(new_migrations))
                for migration in new_migrations:
                    if backend.is_applied(migration):
                        self.log.info(
                            'Migrations upgraded to version %s',
                            str(migration.id)
                        )
            except Exception as error:
                self.log.error('Migrate error: %s', error)
                rollback = backend.to_rollback(migrations)
                self.log.error('Migrate rollback: %s', str(rollback))
                backend.rollback_migrations(rollback)

    # _getConnection return connection string to db
    def _getConnection(self):
        return '{driver}://{user}:{password}@{host}:{port}/{database}'.format(
            driver=DB_CONF.driver,
            user=DB_CONF.user,
            password=DB_CONF.password,
            host=DB_CONF.host,
            port=DB_CONF.port,
            database=DB_CONF.dbname
        )
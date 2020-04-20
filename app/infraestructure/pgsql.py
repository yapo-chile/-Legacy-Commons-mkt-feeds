from typing import Iterator, Dict, Any
import logging
import time
import re
import unicodedata
import pandas as pd  # type: ignore
import psycopg2  # type: ignore
from contextlib import contextmanager
from psycopg2 import pool
from infraestructure.stringIteratorIO import StringIteratorIO,\
    cleanCsvValue, cleanStrValue
from urllib import parse
from infraestructure import config


@contextmanager
def db(conf):
    conn = psycopg2.connect(
        user=conf.user,
        password=conf.password,
        host=conf.host,
        port=conf.port,
        database=conf.dbname)
    conn.set_client_encoding('UTF-8')
    cur = conn.cursor()
    try:
        yield conn, cur
    finally:
        cur.close()
        conn.close()


class Datasource:
    def __init__(self, dbconfig):
        self.config = dbconfig

    def rawSqlToDict(self, query, params):
        """
        Method for convert a raw query into a dict
        Parameters
        ----------
        query:
            Raw query to use
        param:
            In case from need aditional parameters can be added by here
        Returns
        -------
        Dict
            format [{u'nombre:'valor',N..}]
        """
        conn = psycopg2.connect(user=self.config.user,
                                password=self.config.password,
                                host=self.config.host,
                                port=self.config.port,
                                database=self.config.dbname)
        cursor = conn.cursor()
        conn.set_client_encoding('UTF-8')
        cursor.execute(query)
        fieldnames = [name[0] for name in cursor.description]
        result = []
        for row in cursor.fetchall():
            rowset = []
            for field in zip(fieldnames, row):
                if len(field) == 2 and field[0] in params:
                    value = self._normalizeFields(field[0], field[1])
                    field = (field[0], value)
                rowset.append(field)
            result.append(dict(rowset))
        # Closes connection
        cursor.close()
        conn.close()
        # Return results
        return result

    # _normalizeFields returns a normalized str
    def _normalizeFields(self, field, value) -> str:
        rep = {'|': '', '\r': ' ', '\n': '--'}
        if 'url' in field:
            rep.update({'&#8230;': '_',
                        ';': '_', '!': '_', '?': '_',
                        ':': '_', '¨': '_', 'º': '_',
                        'ª': '_', '$': '_', '#': '_',
                        '&': '_', '"': '_', '%': '_',
                        ',': '_'})
            return self._urlParse(self._replaceCharacters(rep, value))
        return self._replaceCharacters(rep, value)

    def _replaceCharacters(self, rep, value) -> str:
        # do the replacement
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        return pattern.sub(
            lambda m: rep[re.escape(m.group(0))],
            self._strip_accents(value)
        )

    # _urlParse returns url safe string
    def _urlParse(self, url) -> str:
        url = "_".join(url.split())
        return "https://" + url if not url.startswith('https://') else url

    # _strip_accents remove accents on a str
    def _strip_accents(self, text) -> str:
        text = unicodedata.normalize('NFD', text)\
            .encode('ascii', 'ignore')\
            .decode("utf-8")
        return str(text)


class Pgsql:
    def __init__(self, dbconfig):
        self.dbconf = dbconfig
        self.dbpool = None
        self.log = logging.getLogger('database')
        date_format = """%(asctime)s,%(msecs)d %(levelname)-2s """
        info_format = """[%(filename)s:%(lineno)d] %(message)s"""
        log_format = date_format + info_format
        logging.basicConfig(format=log_format, level=logging.INFO)

    # start tries to get a connection pool with database
    # and retries maxretries times if connections fails
    # returns True if connection is done successfully otherwise False
    def start(self) -> bool:
        for retry in range(self.dbconf.maxretries):
            self._poolConnect()
            if self.dbpool is not None:
                return True
            self.log.info(
                "waiting %d sec to retry db connection ...",
                self.dbconf.retryTimeout
            )
            time.sleep(self.dbconf.retryTimeout)
        self.log.info("Max retries")
        return False

    # _poolConnect tries to create a threaded connection pool with db
    # if anything goes wrong logs error
    def _poolConnect(self):
        try:
            self.dbpool = psycopg2.pool.ThreadedConnectionPool(
                1, 10,
                user=self.dbconf.user,
                password=self.dbconf.password,
                host=self.dbconf.host,
                port=self.dbconf.port,
                database=self.dbconf.dbname)
        except psycopg2.pool.PoolError as error:
            self.log.error('Connection pool error: %s', error)
        except psycopg2.OperationalError as error:
            self.log.error('Operational connection error: %s', error)

    def select(self, query: str) -> pd.DataFrame:
        with db(self.dbconf) as (conn, cursor):
            cursor.execute(query)
            conn.commit()
            data = pd.DataFrame(cursor.fetchall())
            data.columns = [name[0] for name in cursor.description]
            return data

    def truncate(self) -> pd.DataFrame:
        with db(self.dbconf) as (conn, cursor):
            cursor.execute("TRUNCATE {};".format(self.dbconf.tableName))
            conn.commit()
            return True
        return False

    def makeconnection(self):
        self.log = logging.getLogger('database')
        date_format = """%(asctime)s,%(msecs)d %(levelname)-2s """
        info_format = """[%(filename)s:%(lineno)d] %(message)s"""
        log_format = date_format + info_format
        logging.basicConfig(format=log_format, level=logging.INFO)
        return self.getConnection()

    def getConnection(self):
        dbw = config.Database()
        self.log.info('getConnection DB %s/%s', dbw.host, dbw.dbname)
        return psycopg2.connect(user=dbw.user,
                                password=dbw.password,
                                host=dbw.host,
                                port=dbw.port,
                                database=dbw.dbname)

    def executeCommand(self, connection, command):
        self.log.info('executeCommand : %s', command)
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()
        cursor.close()

    def copyStringIter(self,
                       connection,
                       tableName,
                       dataDict: Iterator[Dict[str, Any]]):
        self.log.info('copyStringIterator init CURSOR %s.', tableName)
        with connection.cursor() as cursor:
            stringData = StringIteratorIO((
                '|'.join(map(cleanCsvValue, (
                    rowDict['ad_id'],
                    rowDict['ad_insertion'],
                    cleanStrValue(rowDict['name']),
                    rowDict['image_url'],
                    rowDict['main_category'],
                    rowDict['category'],
                    cleanStrValue(rowDict['description']),
                    rowDict['price'],
                    rowDict['region'],
                    rowDict['url'],
                    rowDict['condition'],
                    rowDict['ios_url'],
                    rowDict['ios_app_store_id'],
                    rowDict['ios_app_name'],
                    rowDict['android_url'],
                    rowDict['android_package'],
                    rowDict['android_app_name'],
                    rowDict['num_ad_replies'],
                ))) + '\n'
                for rowDict in dataDict
                if len(cleanStrValue(rowDict['url'])) == len(rowDict['url'])
            ))

            self.log.info('Preparing data for insert.')
            cursor.copy_from(stringData, tableName, sep='|')
            self.log.info('copyStringIterator COMMIT.')
            connection.commit()
            self.log.info('Close cursor %s', tableName)
            cursor.close()

    def closeConnection(self, connection):
        connection.close()

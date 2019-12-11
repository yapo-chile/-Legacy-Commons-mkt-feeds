from typing import Iterator, Dict, Any, Optional
from infraestructure.stringIteratorIO import StringIteratorIO
from infraestructure.stringIteratorIO import cleanCsvValue
from infraestructure.stringIteratorIO import cleanStrValue
import pandas as pd
import psycopg2
import logging
from infraestructure.config import Database, DatabaseSource



class Pgsql():
    def execute(self, params: str) -> pd.DataFrame:
        data = pd.DataFrame({'year': [2017, 2014, 2018, 2019],
                             'category': [2, 5, 3, 2],
                             'region': [10, 2, 1, 8]})
        return data.query(params)


def rawSqlToDict(query, param=None):
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
    dbs = DatabaseSource()
    conn = psycopg2.connect(user=dbs.user,
                            password=dbs.password,
                            host=dbs.host,
                            port=dbs.port,
                            database=dbs.dbname)
    cursor = conn.cursor()
    conn.set_client_encoding('UTF-8')
    cursor.execute(query, param)
    fieldnames = [name[0] for name in cursor.description]
    result = []
    for row in cursor.fetchall():
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    # Closes connection
    cursor.close()
    conn.close()
    # Return results
    return result


class writeDatabase(object):
    def __init__(self):
        self.log = logging.getLogger('database')
        date_format = """%(asctime)s,%(msecs)d %(levelname)-2s """
        info_format = """[%(filename)s:%(lineno)d] %(message)s"""
        log_format = date_format + info_format
        logging.basicConfig(format=log_format, level=logging.INFO)
        self.connection = None
        self.getConnection()

    def getConnection(self):
        dbw = Database()
        self.log.info('getConnection DB %s/%s', dbw.host, dbw.dbname)
        self.connection = psycopg2.connect(user=dbw.user,
                                           password=dbw.password,
                                           host=dbw.host,
                                           port=dbw.port,
                                           database=dbw.dbname)

    def executeCommand(self, command):
        self.log.info('executeCommand : %s', command)
        Database()
        cursor = self.connection.cursor()
        cursor.execute(command)
        self.connection.commit()
        cursor.close()

    def copyStringIterator(self, tableName, dataDict: Iterator[Dict[str, Any]]) -> None:
        self.log.info('copyStringIterator init CURSOR %s.', tableName)
        with self.connection.cursor() as cursor:
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
            ))

            self.log.info('Preparing data for insert.')
            cursor.copy_from(stringData, tableName, sep='|')
            self.log.info('copyStringIterator COMMIT.')
            self.connection.commit()
            self.log.info('Close cursor %s', tableName)
            cursor.close()

    def closeConnection(self):
        self.connection.close()

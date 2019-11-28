import pandas as pd
import psycopg2
from config import DatabaseConf


class Pgsql():
    def execute(self, params: str) -> pd.DataFrame:
        data = pd.DataFrame({'year': [2017, 2014, 2018, 2019],
                             'category': [2, 5, 3, 2],
                             'region': [10, 2, 1, 8]})
        return data.query(params)


def RawSqlToDict(query, param=None):
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
    try:
        conn = psycopg2.connect(**DatabaseConf())
    except Exception as e:
        exit(e)
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

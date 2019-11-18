import psycopg2
from config import DatabaseConf

def RawSqlToDict(query, param=None):
    """
    Funcion para convertir un query raw en un dict
    Parameters
    ----------
    query:
        Query Raw a utilizar
    param:
        En caso de necesitar parametros adicionales pueden ser pasados por aca
    Returns
    -------
    Dict
        formato [{u'nombre:'valor',N..}]
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

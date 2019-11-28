import os


def DatabaseConf(dbname='DATABASE'):
    if(dbname == 'DATABASE'):
        return {"host": os.environ.get("DATABASE_HOST", "0.0.0.0"),
                "port": os.environ.get("DATABASE_PORT", "5432"),
                "user": os.environ.get("DATABASE_USER", "docker"),
                "password": os.environ.get("DATABASE_PASSWORD", "docker"),
                "dbname": os.environ.get("DATABASE_NAME", "feeds-db")}
    elif(dbname == 'BLOCKET'):
        return {"host": os.environ.get("BLOCKETDB_HOST", "10.55.10.95"),
                "port": os.environ.get("BLOCKETDB_PORT", "5432"),
                "user": os.environ.get("BLOCKETDB_USER", "bnbiuser"),
                "password": os.environ.get("BLOCKETDB_PASSWORD", "VE1bi@BN112AzLkOP"),
                "dbname": os.environ.get("BLOCKETDB_NAME", "blocketdb")}

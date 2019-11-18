import os

def DatabaseConf():
    return {"host": os.environ.get("DATABASE_HOST", "0.0.0.0"),
            "port": os.environ.get("DATABASE_PORT", "5432"),
            "user": os.environ.get("DATABASE_USER", "docker"),
            "password": os.environ.get("DATABASE_PASSWORD", "docker"),
            "dbname": os.environ.get("DATABASE_NAME", "feeds-db")}
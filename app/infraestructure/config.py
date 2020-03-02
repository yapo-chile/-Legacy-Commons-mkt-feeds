import json
from os import environ
from typing import NamedTuple


def getValueFromFile(env, default=""):
    try:
        file = environ.get(env)
        if file != None:
            f = open(file)
            return f.readline()
        return default
    except IOError:
        return default


# Logger tuple that contain all definitions for logging usage
class Logger(NamedTuple):
    LogLevel: str = environ.get("LOGGER_LOG_LEVEL", "gunicorn.error")


# Server tuple that contains all definitions for server init
class Server(NamedTuple):
    Host: str = environ.get("SERVER_HOST", "0.0.0.0")
    Port: int = int(environ.get("SERVER_PORT", 5000))
    tmpLocation: str = environ.get("SERVER_TMP_LOCATION", "tmp")
    Debug: bool = json.loads(environ.get("SERVER_DEBUG", 'true'))
    configFile: str = environ.get("SERVER_CONFIG_FILE", "catalog.json")


# Database tuple that contains all definitions for its conection
class Database(NamedTuple):
    host: str = environ.get("DATABASE_HOST", "0.0.0.0")
    port: int = int(environ.get("DATABASE_PORT", 5432))
    dbname: str = environ.get("DATABASE_NAME", "feeds-db")
    user: str = environ.get("DATABASE_USER", "docker")
    password: str = getValueFromFile("DATABASE_PASSWORD_FILE", "docker")
    tableName: str = "public.data_feed"


class DatabaseSource(NamedTuple):
    host: str = environ.get("SOURCEDATA_HOST", "0.0.0.0")
    port: int = int(environ.get("SOURCEDATA_PORT", 5432))
    dbname: str = environ.get("SOURCEDATA_NAME", "feeds-db")
    user: str = environ.get("SOURCEDATA_USER", "docker")
    password: str = getValueFromFile("SOURCEDATA_PASSWORD_FILE")


class AWS(NamedTuple):
    accessKey: str = getValueFromFile("AWS_ACCESS_KEY_ID_FILE")
    secretKey: str = getValueFromFile("AWS_SECRET_ACCESS_KEY_FILE")
    bucketName: str = environ.get("AWS_STORAGE_BUCKET_NAME", "")
    bucketFolder: str = environ.get("AWS_STORAGE_BUCKET_FOLDER", "config")
    region: str = environ.get("AWS_REGION_NAME", "us-west-2")


# Config type to contain all definitions of configs
class Config(NamedTuple):
    logger: Logger = Logger()
    server: Server = Server()
    database: Database = Database()
    aws: AWS = AWS()

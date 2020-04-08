import json
from os import environ
from typing import NamedTuple


def getValue(env, default=""):
    if env.endswith("FILE"):
        val = getValueFromFile(env, default)
        return val if val.strip() else environ.get(env[:-5], default)
    return environ.get(env, default)


def getValueFromFile(env, default):
    try:
        file = environ.get(env)
        if file is not None:
            fileData = open(file)
            return fileData.readline()
        return default
    except IOError:
        return default


# Logger tuple that contain all definitions for logging usage
class Logger(NamedTuple):
    LogLevel: str = getValue("LOGGER_LOG_LEVEL", "gunicorn.error")


# Server tuple that contains all definitions for server init
class Server(NamedTuple):
    Host: str = getValue("SERVER_HOST", "0.0.0.0")
    Port: int = int(getValue("SERVER_PORT", "5000"))
    tmpLocation: str = getValue("SERVER_TMP_LOCATION", "tmp")
    Debug: bool = json.loads(getValue("SERVER_DEBUG", 'true'))
    configFile: str = getValue("SERVER_CONFIG_FILE", "catalog.json")


# Database tuple that contains all definitions for its conection
class Database(NamedTuple):
    host: str = getValue("DATABASE_HOST", "0.0.0.0")
    port: int = int(getValue("DATABASE_PORT", "5432"))
    dbname: str = getValue("DATABASE_NAME", "feeds-db")
    user: str = getValue("DATABASE_USER", "docker")
    password: str = getValue("DATABASE_PASSWORD_FILE", "docker")
    tableName: str = getValue("DATABASE_TABLE_NAME", "data_feed")
    migrations: str = getValue("DATABASE_MIGRATIONS_FOLDER", "migrations")


class DatabaseSource(NamedTuple):
    host: str = getValue("SOURCEDATA_HOST", "0.0.0.0")
    port: int = int(getValue("SOURCEDATA_PORT", "5432"))
    dbname: str = getValue("SOURCEDATA_NAME", "feeds-db")
    user: str = getValue("SOURCEDATA_USER", "docker")
    password: str = getValue("SOURCEDATA_PASSWORD_FILE")


class AWS(NamedTuple):
    accessKey: str = getValue("AWS_ACCESS_KEY_ID_FILE")
    secretKey: str = getValue("AWS_SECRET_ACCESS_KEY_FILE")
    bucketName: str = getValue("AWS_STORAGE_BUCKET_NAME", "mkt-feeds")
    bucketFolder: str = getValue("AWS_STORAGE_BUCKET_FOLDER", "config")
    region: str = getValue("AWS_REGION_NAME", "us-east-1")


# Config type to contain all definitions of configs
class Config(NamedTuple):
    logger: Logger = Logger()
    server: Server = Server()
    database: Database = Database()
    databaseSource: DatabaseSource = DatabaseSource()
    aws: AWS = AWS()

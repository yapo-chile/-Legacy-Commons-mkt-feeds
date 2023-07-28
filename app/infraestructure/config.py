import json
from os import environ
from typing import NamedTuple

def getValue(env, default=""):
    if env.endswith("FILE"):
        val = getValueFromFile(env)
        return val if val.strip() else environ.get(env[:-5], default)
    return environ.get(env, default)


"""
def getValueFromFile(env):
    try:
        file = environ.get(env)
        if file is not None:
            fileData = open(file)
            return fileData.readline()
        return ""
    except IOError:
        return ""

"""
    
def getValueFromFile(env):
    try:
        file = environ.get(env)
        if file is not None:
            return file
        return ""
    except IOError:
        return ""



# Logger tuple that contain all definitions for logging usage
class Logger(NamedTuple):
    LogLevel: str = getValue("LOGGER_LOG_LEVEL", "gunicorn.error")


# Server tuple that contains all definitions for server init
class Server(NamedTuple):
    Host: str = getValue("SERVER_HOST", "0.0.0.0")
    Port: int = int(getValue("SERVER_PORT", "5000"))
    tmpLocation: str = getValue("SERVER_TMP_LOCATION", "tmp")
    Debug: bool = json.loads(getValue("SERVER_DEBUG", 'true'))


# Database tuple that contains all definitions for its conection
class Database(NamedTuple):
    driver: str = getValue("DATABASE_DRIVER", "postgres")
    host: str = getValue("DATABASE_HOST", "0.0.0.0")
    port: int = int(getValue("DATABASE_PORT", "5432"))
    dbname: str = getValue("DATABASE_NAME", "feeds-db")
    user: str = getValue("DATABASE_USER", "docker")
    password: str = getValue("DATABASE_PASSWORD", "docker")
    tableName: str = getValue("DATABASE_TABLE_NAME", "data_feed")
    migrations: str = getValue("DATABASE_MIGRATIONS_FOLDER", "migrations")
    maxretries: int = int(getValue("DATABASE_MAX_RETRIES", "10"))
    retryTimeout: int = int(getValue("DATABASE_RETRY_TIMEOUT", "10"))


class DatabaseSource(NamedTuple):
    host: str = getValue("SOURCEDATA_HOST", "0.0.0.0")
    port: int = int(getValue("SOURCEDATA_PORT", "5432"))
    dbname: str = getValue("SOURCEDATA_NAME", "feeds-db")
    user: str = getValue("SOURCEDATA_USER", "docker")
    password: str = getValue("SOURCEDATA_PASSWORD")


class AWS(NamedTuple):
    accessKey: str = getValue("AWS_ACCESS_KEY_ID_FILE")
    secretKey: str = getValue("AWS_SECRET_ACCESS_KEY_FILE")
    bucketName: str = getValue("AWS_STORAGE_BUCKET_NAME", "mkt-feeds")
    bucketFolder: str = getValue("AWS_STORAGE_BUCKET_FOLDER", "config")
    region: str = getValue("AWS_REGION_NAME", "us-east-1")
    configFile: str = getValue("SERVER_CONFIG_FILE", "catalog.json")


class UFConf(NamedTuple):
    externalApi: str = getValue("UF_EXTERNAL_API", "")
    defaultValue: int = int(getValue("UF_DEFAULT_VALUE", "29517"))
    normalizeFactor: float = float(getValue("UF_DEFAULT_FACTOR", "0.01"))
    roundFactor: int = int(getValue("UF_ROUND_FACTOR", "6"))
    locationFolder: str = getValue("UF_LOCATION", "tmp")
    latestFile: str = getValue("UF_latest_file", "latest.txt")


# Config type to contain all definitions of configs
class Config(NamedTuple):
    logger: Logger = Logger()
    server: Server = Server()
    database: Database = Database()
    databaseSource: DatabaseSource = DatabaseSource()
    aws: AWS = AWS()
    ufConf: UFConf = UFConf()

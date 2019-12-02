import domain as d
import json
from os import environ
from typing import NamedTuple


class Logger(NamedTuple):
    LogLevel: str = environ.get("LOGGER_LOG_LEVEL", "gunicorn.error") 


class Server(NamedTuple):
    Host: str = environ.get("SERVER_HOST", "0.0.0.0")
    Port: int = environ.get("SERVER_PORT", 5000)
    Debug: bool = json.loads(environ.get("SERVER_DEBUG", 'true'))


class Database(NamedTuple):
    Host: str = environ.get("DATABASE_HOST", "0.0.0.0")
    Port: int = environ.get("DATABASE_PORT", 5432)
    Name: str = environ.get("DATABASE_NAME", "feeds-db")
    User: str = environ.get("DATABASE_USER", "docker")
    Pass: str = environ.get("DATABASE_PASSWORD", "docker")


"""Config type to contain al definition of config
    use prefix for the sub structs"""
class Config(NamedTuple):
    logger: Logger = Logger()
    server: Server = Server()
    database: Database = Database()

from domain import JSONType, HTTPStatus
from .logger import Response, LOGGER

def healthCheckHandler() -> JSONType:
    LOGGER.info("Ok returned")
    LOGGER.debug("this is a DEBUG message")
    LOGGER.warning("this is a WARNING message")
    LOGGER.error("this is an ERROR message")
    LOGGER.critical("this is a CRITICAL message")
    return Response(HTTPStatus(200)).Success('OK')

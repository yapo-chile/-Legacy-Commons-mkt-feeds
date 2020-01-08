import logging
from flask import Flask
import domain as d
import interfaces.handlers as h
from infraestructure.config import Config

APP = Flask(__name__)
CONFIG: Config = Config()

# Logger initial conf
LOGGER = logging.getLogger(CONFIG.logger.LogLevel)
LOGGER.handlers.extend(LOGGER.handlers)
LOGGER.setLevel(LOGGER.level)
LOGGER.info(CONFIG)


@APP.route("/healthcheck", methods=['GET'])
def healthcheck() -> d.JSONType:
    '''healthCheck route'''
    return h.healthcheckHandler()


@APP.route('/catalog/create/<int:catalog_id>', methods=['GET'])
def catalogCreate(catalog_id) -> d.JSONType:
    '''Catalog route'''
    return h.CatalogHandler(d.CatalogId(catalog_id),
                            config=CONFIG,
                            logger=LOGGER).create()


@APP.route('/catalog/get/<int:catalog_id>', methods=['GET'])
def catalogGet(catalog_id) -> d.JSONType:
    '''Catalog route'''
    return h.CatalogHandler(d.CatalogId(catalog_id),
                            config=CONFIG,
                            logger=LOGGER).get()


@APP.route('/refresh', methods=['GET'])
def dataExtractor() -> d.JSONType:
    return h.dataExtractor.runExtractData()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    APP.run(host=CONFIG.server.Host,
            port=CONFIG.server.Port,
            debug=CONFIG.server.Debug,
            threaded=True)

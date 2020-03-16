import logging
from flask import Flask, request
import domain as d
import interfaces.handlers as h
from infraestructure.config import Config

APP = Flask(__name__)
CONFIG: Config = Config()

# Logger initial conf
LOGGER = logging.getLogger(CONFIG.logger.LogLevel)
LOGGER.setLevel(LOGGER.level)
LOGGER.info(CONFIG)

# /healthcheck returns service status
@APP.route("/healthcheck", methods=['GET'])
def healthcheck() -> d.JSONType:
    '''healthCheck route'''
    return h.healthcheckHandler()

# /catalog/create trigger process to re-create all
# files configured on config file
@APP.route('/catalog/create', methods=['GET'])
def catalogCreateAll() -> d.JSONType:
    '''Catalog route'''
    return h.CatalogHandler(config=CONFIG,
                            logger=LOGGER).createAll()

# /catalog/create trigger process to re-create a
# file configured on config file
@APP.route('/catalog/create/<catalog_id>', methods=['GET'])
def catalogCreate(catalog_id) -> d.JSONType:
    '''Catalog route'''
    return h.CatalogHandler(config=CONFIG,
                            logger=LOGGER).create(d.CatalogId(catalog_id))

# /catalog/get/<catalog_id> returns a file using a catalog_id value
@APP.route('/catalog/get/<catalog_id>', methods=['GET'])
def catalogGet(catalog_id) -> d.JSONType:
    '''Catalog route'''
    appendList = request.args.getlist("file", type=str)
    return h.CatalogHandler(config=CONFIG,
                            logger=LOGGER).get(
                                d.CatalogId(catalog_id),
                                appendList)

# /refresh trigger process to delete db data and recreate it
@APP.route('/refresh', methods=['GET'])
def dataExtractor() -> d.JSONType:
    return h.dataExtractor.runExtractData()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    APP.run(host=CONFIG.server.Host,
            port=CONFIG.server.Port,
            debug=CONFIG.server.Debug,
            threaded=True)

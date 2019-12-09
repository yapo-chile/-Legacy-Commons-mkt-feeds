import logging
from flask import Flask
import domain as d
import interfaces.handlers as h
import interfaces.repository.extractData as e
from infraestructure.config import Config

APP = Flask(__name__)

CONFIG: Config = Config()

# Logger initial conf
LOGGER = logging.getLogger(CONFIG.logger.LogLevel)
LOGGER.handlers.extend(LOGGER.handlers)
LOGGER.setLevel(LOGGER.level)
LOGGER.info(CONFIG)


@APP.route("/healthcheck", methods=['GET'])
def healthCheck() -> d.JSONType:
    '''healthCheck route'''
    return h.healthCheckHandler()


@APP.route('/catalog/<int:catalog_id>', methods=['GET'])
def catalog(catalog_id) -> d.JSONType:
    '''Catalog route'''
    return h.CatalogHandler(d.CatalogId(catalog_id),
                            config=CONFIG,
                            logger=LOGGER).Run()

@app.route('/dataExtractor', methods=['GET'])
def dataExtractor() -> d.JSONType:
    return h.dataExtractor.RunExtractData()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    APP.run(*CONFIG.server, threaded=True)

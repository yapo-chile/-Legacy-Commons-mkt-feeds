from flask import Flask
from flask import request

import json
import logging
import os

import domain as d
import interfaces.handlers as h
from infraestructure.config import Config

app = Flask(__name__)

CONFIG = Config()
LOGGER = logging.getLogger(CONFIG.logger.LogLevel)
LOGGER.info(CONFIG)

@app.route("/healthcheck", methods=['GET'])
def healthCheck() -> d.JSONType:
    return h.healthCheckHandler()

@app.route('/catalog/<int:catalog_id>', methods=['GET'])
def catalog(catalog_id) -> d.JSONType:
    return h.CatalogHandler(d.CatalogId(catalog_id),
                            config=CONFIG,
                            logger=LOGGER).Run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(*CONFIG.server, threaded=True)
else:
    app.logger.handlers.extend(LOGGER.handlers)
    app.logger.setLevel(LOGGER.level)



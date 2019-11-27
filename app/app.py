from flask import Flask
from flask import request

import json
import logging
import os
import typing as t

import domain as d
import interfaces.handlers as h

app = Flask(__name__)

@app.route("/healthcheck")
def healthCheck() -> d.JSONType:
    return h.healthCheckHandler()

@app.route('/catalog/<int:catalog_id>', methods=['GET'])
def catalog(catalog_id) -> d.JSONType:
    return h.CatalogHandler(d.CatalogId(catalog_id)).Run()

if __name__ == "__main__":
    debug = os.getenv('SERVER_DEBUG') or 'true'
    logging.basicConfig(level=logging.DEBUG)
    port = os.getenv('SERVER_PORT') or 5000
    app.run(host="0.0.0.0", port=int(port), threaded=True, debug=json.loads(debug))
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.setLevel(gunicorn_logger.level)
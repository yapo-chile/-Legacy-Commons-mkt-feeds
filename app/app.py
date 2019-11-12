from flask import Flask
from flask import request

import json
import logging
import os

from handlers import healthcheck
from utils.logger import Response

app = Flask(__name__)

@app.route("/v1/healthcheck")
def healthCheck():
    return healthcheck.handler()


if __name__ == "__main__":
    debug = os.getenv('SERVER_DEBUG') or 'true'
    port = os.getenv('SERVER_PORT') or 5000
    app.run(host="0.0.0.0", port=int(port), threaded=True, debug=json.loads(debug))
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
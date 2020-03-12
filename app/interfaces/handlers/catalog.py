from pathlib import Path
import domain as d
import logging
import numpy as np  # type: ignore
from usecases.catalog import CatalogUsecases
from .handler import Response


class CatalogHandler(CatalogUsecases):
    # CatalogHandler implements the handler interface
    # and responds to [GET] /catalog/{id}
    # requests, then executes the Get catalog usecase and returns the response
    # with a io string with a csv header response.
    def __init__(
            self,
            config,
            logger) -> None:
        self.config = config
        self.logger = logger

    # create trigger process to re-create a file using catalogId
    def create(self, catalogId):
        resp = self.createCsv(catalogId)
        if resp:
            r = Response(202)
            return r.toJson(msg=d.JSONType({"status": "Creating"}))
        r = Response(400)
        return r.toJson(msg=d.JSONType({"status": "Failed to create csv"}))

    # createAll trigger process to re-create all files configured
    def createAll(self):
        resp = self.createAllCsv()
        if resp:
            r = Response(202)
            return r.toJson(msg=d.JSONType({"status": "Creating All"}))
        r = Response(400)
        return r.toJson(msg=d.JSONType({"status": "Failed to create all csv"}))

    # get func finds a file if exists and download it
    def get(self, catalogId):
        file = Path(self.filepath(catalogId)).absolute()
        if file.is_file():
            self.logger.info('catalog id {} downloaded'.format(catalogId))
            r = Response(200)
            return r.toCsv(file=file,
                           filename=self.filename(
                               catalogId,
                               include_time=True))
        r = Response(404)
        return r.toJson(msg=d.JSONType({"status": "File doesnt exists"}))

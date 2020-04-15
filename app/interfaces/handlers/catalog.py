from pathlib import Path
import domain as d
import logging
import numpy as np  # type: ignore
from .handler import Response


class CatalogHandler():
    # CatalogHandler implements the handler interface
    # and responds to [GET] /catalog/{id}
    # requests, then executes the Get catalog usecase and returns the response
    # with a io string with a csv header response.
    def __init__(
            self,
            config,
            catalog,
            logger) -> None:
        self.config = config
        self.catalog = catalog
        self.logger = logger

    # create trigger process to re-create a file using catalogId
    def create(self, catalogId):
        resp = self.catalog.createCsv(catalogId)
        if resp:
            r = Response(202)
            return r.toJson(msg=d.JSONType({"status": "Creating"}))
        r = Response(400)
        return r.toJson(msg=d.JSONType({"status": "Failed to create csv"}))

    # createAll trigger process to re-create all files configured
    def createAll(self):
        resp = self.catalog.createAllCsv()
        if resp:
            r = Response(202)
            return r.toJson(msg=d.JSONType({"status": "Creating All"}))
        r = Response(400)
        return r.toJson(msg=d.JSONType({"status": "Failed to create all csv"}))

    # get func finds a file if exists and download it
    def get(self, catalogId, fileList):
        filename = self.catalog.getCsvName(catalogId, fileList)
        file = Path(self.catalog.filepath(filename)).absolute()
        if file.is_file():
            self.logger.info('catalog id {} downloaded'.format(filename))
            r = Response(200)
            return r.toCsv(file=file,
                           filename=self.catalog.filename(
                               filename,
                               include_time=True))
        r = Response(404)
        return r.toJson(msg=d.JSONType({"status": "File doesnt exists"}))

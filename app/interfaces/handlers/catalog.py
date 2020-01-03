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
            catalogId: d.CatalogId,
            config,
            logger) -> None:
        self.config = config
        self.logger = logger
        self.id = catalogId

    def create(self):
        resp = self.create()
        if resp:
            r = Response(202)
            return r.toJson(msg=d.JSONType({"status": "Creating"}))
        r = Response(400)
        return r.toJson(msg=d.JSONType({"status": "Failed to create csv"}))

    # get func finds a file if exists and download it
    def get(self):
        filename = self.filename()
        file = Path("app/tmp/{}".format(filename)).absolute()
        if file.is_file():
            self.logger.info('catalog id {} downloaded'.format(self.id))
            r = Response(200)
            return r.toCsv(file=file,
                           filename=filename)
        r = Response(404)
        return r.toJson(msg=d.JSONType({"status": "File doesnt exists"}))

    @property
    def id(self) -> d.CatalogId:
        return self.__id

    @id.setter
    def id(self, catalogId: d.CatalogId) -> None:
        # Validates that catalogId is not negative
        if catalogId <= 0:
            raise ValueError("Catalog id is not a valid value")
        self.__id = catalogId

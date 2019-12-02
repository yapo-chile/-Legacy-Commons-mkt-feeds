import io
import domain as d
import pandas as pd
import datetime
import logging
from flask import make_response
from usecases.catalog import CatalogUsecases
from .handler import Response

class CatalogHandler(CatalogUsecases):

    def __init__(self, catalogId:d.CatalogId, config:d.Config, logger:logging) -> None:
        self.config = config
        self.logger = logger
        self.id = catalogId

    def Run(self):
        data = self.get()
        stream = io.StringIO()
        data.to_csv(stream, sep=";")
        output = make_response(stream.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export{}.csv".format(datetime.datetime.now())
        output.headers["Content-type"] = "text/csv"
        if len(data) > 0:
            self.logger.info('{} rows downloaded from catalog id {}'.format(len(data), self.id))
        else:
            self.logger.info('No rows found for catalog id {}, returning empty file'.format(self.id))
        return output

    @property
    def id(self) -> d.CatalogId:
        return self.__id
    
    @id.setter
    def id(self, catalogId:d.CatalogId) -> None:
        if catalogId <= 0:
            raise ValueError("Catalog id is not a valid value")
        self.__id = catalogId



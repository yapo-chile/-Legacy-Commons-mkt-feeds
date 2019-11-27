import io
import domain as d
import pandas as pd
import datetime
import logging
from flask import make_response
from .logger import Response
from usecases.catalog import CatalogUsecases

class CatalogHandler(CatalogUsecases):

    def __init__(self, catalogId:d.CatalogId) -> None:
        self.id = catalogId

    def Run(self):
        data = self.get()
        stream = io.StringIO()
        data.to_csv(stream, sep=";")
        output = make_response(stream.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export{}.csv".format(datetime.datetime.now())
        output.headers["Content-type"] = "text/csv"
        if len(data) > 0:
            logging.info('{} rows downloaded from catalog id {}'.format(self.id, len(data)))
        else:
            logging.info('No rows found for catalog id {}, returning empty file'.format(self.id))
        return output

    @property
    def id(self) -> d.CatalogId:
        return self.__id
    
    @id.setter
    def id(self, catalogId:d.CatalogId) -> None:
        if catalogId <= 0:
            raise ValueError("Catalog id is not a valid value")
        self.__id = catalogId



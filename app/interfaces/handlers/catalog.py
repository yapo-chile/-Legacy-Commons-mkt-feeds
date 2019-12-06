import io
import domain as d
import logging
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

    def Run(self):
        data = self.get()
        stream = io.StringIO()
        data.to_csv(stream, sep=";")
        if len(data) > 0:
            self.logger.info(
                '{} rows downloaded from catalog id {}'.format(
                    len(data), self.id))
        else:
            self.logger.info(
                'No rows found for catalog id {}, returning empty file'.format(
                    self.id))

        r = Response(200)
        return r.toCsv(stream=stream)

    @property
    def id(self) -> d.CatalogId:
        return self.__id

    @id.setter
    def id(self, catalogId: d.CatalogId) -> None:
        # Validates that catalogId is not negative
        if catalogId <= 0:
            raise ValueError("Catalog id is not a valid value")
        self.__id = catalogId

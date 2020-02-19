import numpy as np  # type: ignore
import threading
import datetime
from interfaces.repository.catalogRepo import CatalogRepo


# CatalogUsecases receives a catalog id and if valid returns a size-fixed
# data matrix.
class CatalogUsecases(CatalogRepo):

    def generate(self):
        catalog = self.getCatalog()
        columns = self.getOutputFields()
        delimiter = self.getOutputDelimiter()

        # Leaving this commented so would be used to check
        # repeated rows in the future
        # duplicateRowsDF = catalog[catalog.duplicated(keep='last')]
        # print(duplicateRowsDF.head())
        catalog.drop_duplicates(inplace=True)
        catalog.to_csv(self.filepath(),
                       sep=delimiter,
                       header=True,
                       index=False,
                       columns=columns)
        if len(catalog) > 0:
            self.logger.info(
                '{} rows created for catalog id {} file'.format(
                    len(catalog), self.id))
        else:
            self.logger.info(
                'No rows found for catalog id {}, returning empty file'.format(
                    self.id))
        return True

    def createCsv(self) -> bool:
        t = threading.Thread(target=self.generate)
        t.start()
        return True

    def filepath(self):  # type: ignore
        return "{}/{}".format(self.config.server.tmpLocation,
                              self.filename())

    def filename(self, include_time=False):  # type: ignore
        return "catalog_{}{}.csv".format(self.id,
                                         datetime.datetime.now()
                                         .strftime("%m%d%Y%H%M%S")
                                         if include_time else "")

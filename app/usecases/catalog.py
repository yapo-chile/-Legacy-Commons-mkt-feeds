import numpy as np  # type: ignore
import threading
from interfaces.repository.catalogRepo import CatalogRepo


# CatalogUsecases receives a catalog id and if valid returns a size-fixed
# data matrix.
class CatalogUsecases(CatalogRepo):

    def generate(self):
        catalog = self.getCatalog()
        catalog.to_csv("app/tmp/catalog_{}.csv".format(self.id),
                       sep=";",
                       header=True,
                       index=False)
        if len(catalog) > 0:
            self.logger.info(
                '{} rows downloaded from catalog id {}'.format(
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

    def filename(self):  # type: ignore
        filename = "catalog_{}.csv".format(self.id)
        return filename

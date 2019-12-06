import pandas as pd  # type: ignore
from interfaces.repository.catalogRepo import CatalogRepo


# CatalogUsecases receives a catalog id and if valid returns a size-fixed
# data matrix.
class CatalogUsecases(CatalogRepo):

    def get(self) -> pd.DataFrame():  # type: ignore
        return self.getCatalog()

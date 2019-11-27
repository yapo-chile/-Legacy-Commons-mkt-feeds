import domain as d
import pandas as pd
from interfaces.repository.catalogRepo import CatalogRepo

class CatalogUsecases(CatalogRepo):
    """
    Receives a catalog id and if valid returns a size-fixed data matrix.

    Parameters
    ----------
    id : domain type CatalogId

    """
    def get(self) -> pd.DataFrame():
        return self.getCatalog()



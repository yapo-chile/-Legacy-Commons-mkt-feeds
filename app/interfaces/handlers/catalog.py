import domain as d
from .logger import Response
from usecases.catalog import CatalogUsecases

class CatalogHandler:

    def __init__(self, catalog_id:d.CatalogId) -> None:
        self.catalog = catalog_id

    def Run(self) -> d.JSONType:
        return CatalogUsecases(self.catalog).Execute()


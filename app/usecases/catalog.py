import domain as d

class CatalogUsecases:

    def __init__(self, catalog_id:d.CatalogId) -> None:
        self.catalog = catalog_id

    def findCatalog(self) -> None:
        if self.catalog == 1:
            self.params = d.JSONType({"test": "ok"})
        else:
            raise Exception("Catalog Not Found")
    
    def Execute(self) -> d.JSONType:
        self.findCatalog()
        return self.params



import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import threading
import datetime
from pathlib import Path
from interfaces.repository.catalogRepo import CatalogRepo


# CatalogUsecases receives a catalog id and if valid returns a size-fixed
# data matrix.
class CatalogUsecases(CatalogRepo):
    # generate gets catalog data and generates a new file using catalogId
    def generate(self, catalogId) -> bool:
        catalogRaw = self.getRawCatalog()
        catalogConfig = self.getCatalogConfig(catalogId)
        return self.generateFromCatalog(catalogRaw, catalogConfig, catalogId)

    # generateFromCatalog generates a catalog filtered by catalogConfig
    # and creates a new csv file using a specifi catalogId.
    # Returns false if process fails, otherwise returns true
    def generateFromCatalog(self, catalogRaw, catalogConfig, catalogId):
        catalog = self.getCatalog(catalogRaw, catalogConfig)
        if catalog.empty:
            self.logger.info(
                'No rows found for catalog id {}, returning empty file'.format(
                    catalogId))
            del catalog
            del catalogRaw
            del catalogConfig
            return False
        columns = self.getOutputFields(catalogConfig)
        delimiter = self.getOutputDelimiter(catalogConfig)

        # Leaving this commented so would be used to check
        # repeated rows in the future
        # duplicateRowsDF = catalog[catalog.duplicated(keep='last')]
        # print(duplicateRowsDF.head())
        catalog.drop_duplicates(inplace=True)
        catalog.to_csv(self.filepath(catalogId),
                       sep=delimiter,
                       header=True,
                       index=False,
                       columns=columns)
        if len(catalog) > 0:
            self.logger.info(
                '{} rows created for catalog id {} file'.format(
                    len(catalog), catalogId))
        del catalog
        del catalogRaw
        del catalogConfig
        return True

    # generateAll gets all catalogConfig configured on config file
    # and iterate over them to re-create all files.
    # Returns true when process is done
    def generateAll(self):
        catalogAllConfig = self.getAllCatalogConfig()
        catalogRaw = self.getRawCatalog()
        for key, catalogConfig in catalogAllConfig.items():
            self.generateFromCatalog(catalogRaw, catalogConfig, key)
        del catalogRaw
        return True

    # createCsv trigger process to create a file using catalogId
    def createCsv(self, catalogId) -> bool:
        t = threading.Thread(target=self.generate, args=(catalogId))
        t.start()
        return True

    # createAllCsv trigger process to create all files
    def createAllCsv(self) -> bool:
        t = threading.Thread(target=self.generateAll)
        t.start()
        return True

    # getCsvName if fileList has values concat all csv files, store it
    # and returns this new filename. Otherwise returns catalogId
    def getCsvName(self, catalogId, fileList) -> str:
        files = []
        if len(fileList) > 0:
            fileList.insert(0, catalogId)
            filename = ""
            for id in fileList:
                file = Path(self.filepath(id)).absolute()
                if file.is_file():
                    filename += id + "_"
                    files.append(file)
            if len(files) > 0:
                combined_csv = pd.concat([pd.read_csv(f) for f in files])
                combined_csv.to_csv(
                    self.filepath(filename),
                    index=False,
                    encoding='utf-8-sig')
            return filename
        return catalogId

    # filepath returns a file path using a catalogId
    def filepath(self, catalogId):  # type: ignore
        return "{}/{}".format(self.config.server.tmpLocation,
                              self.filename(catalogId))

    # filename returns a file name using a catalogId
    def filename(self, catalogId, include_time=False):  # type: ignore
        return "catalog_{}{}.csv".format(catalogId,
                                         datetime.datetime.now()
                                         .strftime("%m%d%Y%H%M%S")
                                         if include_time else "")

import domain as d
import pandas as pd  # type: ignore
from typing import List
from infraestructure.pgsql import Pgsql  # type: ignore
from infraestructure.catalog import CatalogConf  # type: ignore


class CatalogRepo(CatalogConf):
    def __init__(self) -> None:
        self.catalog: pd.DataFrame = pd.DataFrame([])

    # _parseParams get conditions and generate a query filter
    def _parseParams(self, params) -> str:
        # Translate Condition
        def translateCondition(condition):
            if condition == 'higher':
                condition = d.Condition('>')
            elif condition == 'higher_than':
                condition = d.Condition('>=')
            elif condition == 'lower_than':
                condition = d.Condition('<=')
            elif condition == 'lower':
                condition = d.Condition('<')
            elif condition == 'equal':
                condition = d.Condition('==')
            elif condition == 'not_equal':
                condition = d.Condition('!=')
            return condition
        query = ''
        for p in params:
            p["condition"] = translateCondition(p["condition"])
            if isinstance(p["value"], str):
                query += ' {field} {condition} "{value}" {union}'.format(**p)
            else:
                query += ' {field} {condition} {value} {union}'.format(**p)
        return query

    # _getQueryCatalog returns sql query to select all data
    def _getQueryCatalog(self) -> str:
        query = """
            select ad_id::int,
            ad_insertion,
            REPLACE(name,';','') as name,
            image_url,
            main_category,
            category,
            REPLACE(description,';','') as description,
            price::bigint,
            region,
            REPLACE(url,'"','') as url,
            condition,
            ios_url,
            ios_app_store_id::int,
            ios_app_name,
            android_url,
            android_package,
            android_app_name,
            num_ad_replies::int
            from data_feed;"""
        return query

    # _getParams get params on catalogConfig and return a query filter
    def _getParams(self, catalogConfig) -> str:
        query = ""
        if "params" in catalogConfig and \
                len(catalogConfig["params"]) > 0:
            query = self._parseParams(catalogConfig["params"])
        return query

    # _getData returns a dataframe using a given sql query
    def _getData(self) -> pd.DataFrame:
        return Pgsql().select(query=self._getQueryCatalog())

    # _applyFields returns a dataframe with renamed columns
    def _applyFields(self, data, catalogConfig) -> pd.DataFrame:
        if len(catalogConfig["fields"]) > 0:
            data = data.rename(columns=catalogConfig["fields"])
        return data

    # _applyCreateColumn returns a dataframe with new columns
    def _applyCreateColumn(self, data, catalogConfig) -> pd.DataFrame:
        if "create_column" in catalogConfig:
            for k, v in catalogConfig["create_column"].items():
                if v in data.columns:
                    data[k] = data.eval(v)
                else:
                    data[k] = v
        return data

    # getCatalog returns a dataframe filtered by catalogConfig parameters
    def getCatalog(self, data, catalogConfig) -> pd.DataFrame:
        if len(catalogConfig) > 0 and not data.empty:
            dataframe = data.query(self._getParams(catalogConfig))
            dataframe = self._applyCreateColumn(dataframe, catalogConfig)
            return self._applyFields(dataframe, catalogConfig)
        return pd.DataFrame

    # getRawCatalog returns a dataframe with all the data
    def getRawCatalog(self) -> pd.DataFrame:
        return self._getData()

    # getCatalogConfig returns a specific catalogConfig
    def getCatalogConfig(self, catalogId) -> d.CatalogConfig:
        return self.getCatalogConf(catalogId)

    # getAllCatalogConfig returns all catalogConfig present on config file
    def getAllCatalogConfig(self) -> d.CatalogConfig:
        return self.getAllCatalogConf()

    # getOutputFields returns a List with all configured output columns
    def getOutputFields(self, catalogConfig) -> List[str]:
        return [x for x in catalogConfig["fields"].values()]

    # getOutputDelimiter returns delimiter to be used on output file
    def getOutputDelimiter(self, catalogConfig) -> str:
        return catalogConfig if "delimiter" in catalogConfig else ","

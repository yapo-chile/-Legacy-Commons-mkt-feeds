import domain as d
import pandas as pd  # type: ignore
from typing import List
from infraestructure.pgsql import Pgsql  # type: ignore
from infraestructure.catalog import CatalogConf  # type: ignore


class CatalogRepo(CatalogConf):
    def __init__(self) -> None:
        self.catalog: pd.DataFrame = pd.DataFrame([])

    def _parseParams(self) -> str:
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
            return condition
        query = ''
        for p in self.catalogConfig["params"]:
            p["condition"] = translateCondition(p["condition"])
            if isinstance(p["value"], str):
                query += ' {field} {condition} "{value}" {union}'.format(**p)
            else:
                query += ' {field} {condition} {value} {union}'.format(**p)
        return query

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

    def _getParams(self) -> str:
        query = ""
        if "params" in self.catalogConfig and \
                len(self.catalogConfig["params"]) > 0:
            query = self._parseParams()
        return query

    def _getData(self) -> None:
        self.catalog = Pgsql().select(query=self._getQueryCatalog())
        self.catalog = self.catalog.query(self._getParams())

    def _applyFields(self) -> None:
        if len(self.catalogConfig["fields"]) > 0:
            self.catalog = \
                self.catalog.rename(columns=self.catalogConfig["fields"])

    def _applyCreateColumn(self) -> None:
        if "create_column" in self.catalogConfig:
            for k, v in self.catalogConfig["create_column"].items():
                self.catalog[k] = self.catalog.eval(v)

    def getCatalog(self) -> pd.DataFrame:
        self.catalogConfig = self.getCatalogConf(self.id)  # type: ignore
        if len(self.catalogConfig) > 0:
            self._getData()
            self._applyCreateColumn()
            self._applyFields()
            return self.catalog
        return pd.DataFrame

    def getOutputFields(self) -> List[str]:
        return [x for x in self.catalogConfig["fields"].values()]

    def getOutputDelimiter(self) -> str:
        return self.catalogConfig if "delimiter" in self.catalogConfig else ","

import domain as d
import pandas as pd  # type: ignore
from urllib import parse
from typing import List


class CatalogRepo():
    def __init__(self, db, catalogConf):
        self.catalog: pd.DataFrame = pd.DataFrame([])
        self.db = db
        self.catalogConf = catalogConf

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
            else:
                condition = ''
            return condition
        query = ''
        for p in params:
            p["condition"] = translateCondition(p["condition"])
            if not p["condition"]:
                continue
            if isinstance(p["value"], str):
                query += ' {field} {condition} "{value}" {union}'.format(**p)
            else:
                query += ' {field} {condition} {value} {union}'.format(**p)
        return query

    # _specialCases get conditions and filter a dataframe
    def _specialCases(self, data, catalogConfig) -> pd.DataFrame:
        # getMultipleWords regex just positive cases on a word list
        def getMultipleWords(words):
            list = words.split(",")
            return '(?<!no ){}'.format('|(?<!no )'.join(list))

        # getWordsList returns a list like object
        def getWordsList(words):
            return words.split(",")

        # translateCondition returns a condition to filter a dataframe
        # condition should be a boolean vector or None
        # to do that operators on condition should be bitwise
        # (| for or, & for and, and ~ for not)
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
        # https://stackoverflow.com/questions/36921951/truth-value-of-a-series-/is-ambiguous-use-a-empty-a-bool-a-item-a-any-o
        def translateCondition(data, p):
            condition = None
            if "condition" not in p or "field" not in p or "values" not in p:
                condition = None
            if p["condition"] == 'contains':
                condition = data[p["field"]].str.contains(
                    getMultipleWords(p["values"])
                )
            elif p["condition"] == 'not_contains':
                condition = ~data[p["field"]].str.contains(
                    getMultipleWords(p["values"])
                )
            elif p["condition"] == 'in':
                condition = data[p["field"]].isin(
                    getWordsList(p["values"])
                )
            elif p["condition"] == 'not_in':
                condition = ~data[p["field"]].isin(
                    getWordsList(p["values"])
                )
            return condition
        if "params_list" in catalogConfig and \
                len(catalogConfig["params_list"]) > 0:
            for p in catalogConfig["params_list"]:
                condition = translateCondition(data, p)
                data = data[condition] if condition is not None else data
        return data

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
        return self.db.select(query=self._getQueryCatalog())

    # _urlParse returns url safe string
    def _urlParse(self, url) -> str:
        url = " ".join(url.split())
        url = parse.quote(url, safe="/:?#[]@!$&'()*+;=")
        return url

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

    # _applyFormat returns a dataframe with columns format
    def _applyFormat(self, data, catalogConfig) -> pd.DataFrame:
        def translateFormat(format_column, value, data) -> pd.DataFrame:
            if format_column == 'lowercase':
                if value == 'all':
                    data = data.applymap(
                        lambda s: s.lower() if isinstance(s, str) else s
                    )
                elif value in data.columns:
                    data = data[value].str.lower()
                else:
                    print("Column not found ", value)
            elif format_column == 'uppercase':
                if value == 'all':
                    data = data.applymap(
                        lambda s: s.upper() if isinstance(s, str) else s
                    )
                elif value in data.columns:
                    data = data[value].str.upper()
                else:
                    print("Column not found ", value)
            return data
        if "format_column" in catalogConfig:
            for k, v in catalogConfig["format_column"].items():
                data.update(translateFormat(k, v, data))
        return data

    # getCatalog returns a dataframe filtered by catalogConfig parameters
    def getCatalog(self, data, catalogConfig) -> pd.DataFrame:
        if len(catalogConfig) > 0 and not data.empty:
            dataframe = data.query(self._getParams(catalogConfig))
            dataframe = self._applyCreateColumn(dataframe, catalogConfig)
            dataframe = self._applyFormat(dataframe, catalogConfig)
            dataframe = self._specialCases(dataframe, catalogConfig)
            return self._applyFields(dataframe, catalogConfig)
        return pd.DataFrame

    # getRawCatalog returns a dataframe with all the data
    def getRawCatalog(self) -> pd.DataFrame:
        data = self._getData()
        data['url'] = data.url.apply(self._urlParse)
        return data

    # getCatalogConfig returns a specific catalogConfig
    def getCatalogConfig(self, catalogId) -> d.CatalogConfig:
        return self.catalogConf.getCatalogConf(catalogId)

    # getAllCatalogConfig returns all catalogConfig present on config file
    def getAllCatalogConfig(self) -> d.CatalogConfig:
        return self.catalogConf.getAllCatalogConf()

    # getOutputFields returns a List with all configured output columns
    def getOutputFields(self, catalogConfig) -> List[str]:
        return [x for x in catalogConfig["fields"].values()]

    # getOutputDelimiter returns delimiter to be used on output file
    def getOutputDelimiter(self, catalogConfig) -> str:
        return catalogConfig if "delimiter" in catalogConfig else ","

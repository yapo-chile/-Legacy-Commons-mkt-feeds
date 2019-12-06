import domain as d


# CatalogConf checks what set of confs are needed to generate the requested csv
class CatalogConf():

    def get(self, catalogId: d.CatalogId) -> d.JSONType:
        if catalogId == 1:
            config = {
                "params": [
                    {"field": "year", "condition": "higher",
                     "value": "2000", "union": "and"},
                    {"field": "year", "condition": "lower_than",
                     "value": "2020", "union": "or"},
                    {"field": "category", "condition": "equal",
                     "value": "2020", "union": ""}],
                "fields": {"category": "categoria"},
                "create_column": {
                    "test": "year + category",
                    "future_year": "2 * year"
                }
            }
        else:
            config = {}
        return d.JSONType(config)

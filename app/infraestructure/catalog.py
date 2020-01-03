import domain as d


# CatalogConf checks what set of confs are needed to generate the requested csv
class CatalogConf():

    def get(self, catalogId: d.CatalogId) -> d.JSONType:
        if catalogId == 1:
            config = {
                "params": [
                    {"field": "price", "condition": "higher_than",
                     "value": 0, "union": ""},
                    # {"field": "price", "condition": "lower_than",
                    # "value": 4000000, "union": ""},
                    # {"field": "category", "condition": "equal",
                    # "value": "2020", "union": ""}
                    ],
                "fields": {"category": "categoria"}
                # "create_column": {
                #    "test": "year + category",
                #    "future_year": "2 * year"
                # }
            }
        else:
            config = {}
        return d.JSONType(config)

import pandas as pd

class Pgsql():
    def execute(self, params: str) -> pd.DataFrame:
        data = pd.DataFrame({'year': [2017, 2014, 2018, 2019],
                             'category': [2, 5, 3, 2],
                             'region': [10, 2, 1, 8]})
        return data.query(params)

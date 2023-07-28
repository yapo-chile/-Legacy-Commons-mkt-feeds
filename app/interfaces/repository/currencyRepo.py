import datetime
import requests
import pandas as pd  # type: ignore
from os import path


class CurrencyRepo():
    def __init__(self, ufConf) -> None:
        self.ufConf = ufConf

    # getRawCatalogWithFixedPrice returns a dataframe
    # with price on chilean pesos
    """def getRawCatalogWithFixedPrice(self, data) -> pd.DataFrame:
        uf = self.getCurrentUF()
        data['price'] = data.apply(
            lambda x: self._getUFPrice(x.price, x.currency, uf), axis=1
        )
        return data"""
    
    def getRawCatalogWithFixedPrice(self, data) -> pd.DataFrame:
        uf = self.getCurrentUF()
        if 'price' in data:
            data['price'] = data.apply(
                lambda x: self._getUFPrice(x.price, x.currency, uf), axis=1
            )
        return data


    # getCurrentUF returns updated uf from external api.
    # If it fails, gets latest or default value
    def getCurrentUF(self) -> int:
        uf = self._getUpdatedUF()
        if uf > 0:
            self._saveUF(uf)
            return uf
        uf = self._latestUF()
        if uf > 0:
            self._saveUF(uf)
            return uf
        return self.ufConf.defaultValue

    # _saveUF save uf value on a file
    def _saveUF(self, uf):
        out = open(self._getfile(), "w+")
        out.write(str(uf))
        out.close()
        return

    # _latestUF read latest uf value from file
    def _latestUF(self) -> int:
        filename = self._getfile()
        if path.exists(filename) and path.isfile(filename):
            source = open(filename, "r")
            data = source.read()
            source.close()
            try:
                uf = int(data)
                if uf > 0:
                    return uf
            except ValueError:
                return 0
        return 0

    # _getUpdatedUF returns UF value from a external api.
    # If something fails returns 0
    def _getUpdatedUF(self) -> int:
        now = datetime.datetime.now()
        dateStr = "{:02d}-{:02d}-{:04d}".format(now.day, now.month, now.year)
        try:
            response = requests.get(self.ufConf.externalApi + dateStr)
            if response.ok:
                data = response.json()
                if ('serie' in data and
                        data['serie'] and data['serie'][0]['valor']):
                    uf = int(data['serie'][0]['valor'])
                    if uf > 0:
                        return uf
        except (requests.exceptions.RequestException, ValueError):
            return 0
        return 0

    # _getUFPrice if currency is UF, it converts this value to chilean pesos.
    # otherwise returns price
    def _getUFPrice(self, price, currency, uf) -> int:
        if isinstance(currency, str) and currency == 'uf':
            price = int(price * self.ufConf.normalizeFactor * uf)
        return price

    # _getFile returns a file identifier
    def _getfile(self) -> str:
        return '{}/{}'.format(
            self.ufConf.locationFolder,
            self.ufConf.latestFile)

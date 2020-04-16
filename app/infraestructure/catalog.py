import json
import boto3  # type: ignore
import botocore  # type: ignore
import domain as d
from typing import Any, Dict


class CatalogConf():
    # CatalogConf checks what set of confs are needed
    # to generate the requested csv
    def __init__(self, conf):
        self.conf = conf

    # _getS3Resource gets s3 resource with a given session
    def _getS3Resource(self):
        session = boto3.Session(
            aws_access_key_id=self.conf.accessKey,
            aws_secret_access_key=self.conf.secretKey,
            region_name=self.conf.region,
        )
        return session.resource('s3')

    # _getKey returns a key identifier to get a file on s3
    def _getKey(self) -> str:
        return '{}/{}'.format(
            self.conf.bucketFolder,
            self.conf.configFile)

    # _getS3Conf returns s3 file body
    def _getS3Conf(self):
        s3 = self._getS3Resource()
        s3Object = s3.Object(self.conf.bucketName, self._getKey())
        return s3Object.get()['Body'].read().decode('utf-8')

    # getCatalogConf get config data on s3 file using a specific catalogId
    def getCatalogConf(self, catalogId: d.CatalogId) -> d.JSONType:
        try:
            s3Conf = self._getS3Conf()
            data = json.loads(s3Conf)
            if str(catalogId) in data:
                return d.JSONType(data[catalogId])
            else:
                return d.JSONType(Dict[str, Any]())
        except botocore.exceptions.ClientError as e:
            return d.JSONType(Dict[str, Any]())

    # getAllCatalogConf get all config data file on s3
    def getAllCatalogConf(self) -> d.CatalogConfig:
        try:
            s3Conf = self._getS3Conf()
            data = json.loads(s3Conf)
            return d.CatalogConfig(data)
        except botocore.exceptions.ClientError as e:
            return d.CatalogConfig(Dict[str, d.JSONType]())

#  type: ignore
import domain as d
import json
import boto3
import botocore


# CatalogConf checks what set of confs are needed to generate the requested csv
class CatalogConf():

    def getCatalogConf(self, catalogId: d.CatalogId) -> d.JSONType:
        session = boto3.Session(
            aws_access_key_id=self.config.aws.accessKey,
            aws_secret_access_key=self.config.aws.secretKey,
            region_name=self.config.aws.region,
        )
        s3 = session.resource('s3')
        key = '{}/{}'.format(self.config.aws.bucketFolder,
                             self.config.server.configFile)
        try:
            s3Object = s3.Object(self.config.aws.bucketName, key)
            s3Conf = s3Object.get()['Body'].read().decode('utf-8')
            data = json.loads(s3Conf)
            if str(catalogId) in data:
                return d.JSONType(data[str(catalogId)])
            else:
                return d.JSONType([])
        except botocore.exceptions.ClientError as e:
            return d.JSONType([])

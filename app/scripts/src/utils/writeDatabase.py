import psycopg2
import pandas as pd
from .logger import logger
from .configure import conf
import csv

class writeDatabase(object):
    def __init__(self):
        self.config = conf( "./utils/resources/configuration.properties" )
        self.log        = logger()
        self.host       = self.config.getSpecific( 'ENDPOINT.HOST' )
        self.port       = self.config.getSpecific( 'ENDPOINT.PORT' )
        self.dbname     = self.config.getSpecific( 'ENDPOINT.DATABASE' )
        self.user       = self.config.getSpecific( 'ENDPOINT.USERNAME' )
        self.password   = self.config.getSpecific( 'ENDPOINT.PASSWORD' )
        self.engine     = None
        self.getConnection()

    def getConnection(self):
        try:
            self.log.getLogInfo('Write to database getConnection')
            self.engine = psycopg2.connect("host="+self.host+" port="+self.port+" dbname="+self.dbname+" user="+self.user+" password="+self.password)
        except Exception as e:
            self.log.getLogError(str(e))
            exit()

    def deleteCategory(self, schemaTable=None, category=None):
        try:
            deleteCommand = 'DELETE FROM %s WHERE category = %s ' % (schemaTable, category)
            self.log.getLogInfo(deleteCommand)
            cur.execute()
            cur = self.engine.cursor(deleteCommand)
            self.engine.commit()
            cur.close()
        except Exception as e:
            self.log.getLogError(str(e))
            self.engine.close()
            exit()

    def closeConnection(self):
        try:
            self.log.getLogInfo('Close connection')
            self.engine.close()
        except Exception as e:
            self.log.getLogError('Close connection failed')
            exit()


    def insertCsv(self, schemaTable, fileName):
        try:
            insertQuery =   """ INSERT INTO """+ schemaTable+ """
                                ( 	ad_id
	                                , ad_insertion
                                    , "name"
                                    , image_url
                                    , main_category
                                    , category
	                                , description
                                    , price
                                    , region
                                    , url                                
                                    , "condition"
                                    , ios_url
                                    , ios_app_store_id
                                    , ios_app_name
                                    , android_url
                                    , android_package
                                    , android_app_name
	                                , num_ad_replies )  VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
                            """
            cur = self.engine.cursor()
            self.log.getLogInfo('INSERT INTO %s from %s' % (schemaTable, fileName))
            with open(fileName) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                rowCount=0
                for row in csv_reader:
                    rowCount += 1
                    if (rowCount > 1 ):
                        cur.execute(insertQuery, row)
                        self.engine.commit()
            cur.close()            
        except Exception as e:
            self.log.getLogError(str(e))
            self.engine.close()
            exit()
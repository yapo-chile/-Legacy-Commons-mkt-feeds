from sqlalchemy import create_engine
import pandas as pd
from .logger import logger
from .configure import conf

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
            self.log.getLogInfo('getConnection database')
            self.engine = create_engine('postgresql://'+self.user+':'+self.password+'@'+self.host+':'+self.port+'/'+self.dbname,echo=False)
        except Exception as e:
            self.log.getLogError(str(e))
            exit()

    def closeConnection(self):
        try:
            self.log.getLogInfo('closeConnection database')
            self.engine.connect().close()
        except Exception as e:
            self.log.getLogError(str(e))
            exit()

    def insertData(self, dataframe, schema, table, ifExists):
        try:
            self.log.getLogInfo("insert into " + schema + "." + table )
            dataframe.to_sql(con=self.engine
                            , schema=schema
                            , name=table
                            , if_exists=ifExists
                            , index=False )
        except Exception as e:
            self.log.getLogError(str(e))
            self.engine.connect().close()
            exit()
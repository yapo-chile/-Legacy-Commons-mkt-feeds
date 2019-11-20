from sqlalchemy import create_engine
import pandas as pd

class writeDatabase(object):
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.engine = None
    
    def getConnection(self):
        self.engine = create_engine('postgresql://'+self.user+':'+self.password+'@'+self.host+':'+self.port+'/'+self.dbname,echo=False)
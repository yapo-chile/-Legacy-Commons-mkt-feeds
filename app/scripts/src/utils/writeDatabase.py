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


    def mappingCategory(self, category=None):
        textCategory = None
        if (category == 1220): textCategory =  'Comprar'
        if (category == 1240): textCategory =  'Arrendar'
        if (category == 2020): textCategory =  'Autos, camionetas y 4x4'
        if (category == 2060): textCategory =  'Motos'
        if (category == 3020): textCategory =  'Consolas, videojuegos y accesorios'
        if (category == 3040): textCategory =  'Computadores y accesorios'
        if (category == 3060): textCategory =  'Celulares, teléfonos y accesorios'
        if (category == 3080): textCategory =  'Audio, TV, video y fotografia'
        if (category == 4020): textCategory =  'Moda y vestuario'
        if (category == 4040): textCategory =  'Bolsos, bisutería y accesorios'
        if (category == 4060): textCategory =  'Salud y belleza'
        if (category == 4080): textCategory =  'Calzado'
        if (category == 5020): textCategory =  'Muebles'
        if (category == 5040): textCategory =  'Electrodomésticos'
        if (category == 5060): textCategory =  'Jardín y herramientas'
        if (category == 5160): textCategory =  'Otros artículos del hogar'
        if (category == 6020): textCategory =  'Deportes, gimnasia y accesorios'
        if (category == 6060): textCategory =  'Bicicletas, ciclismo y accesorios'
        if (category == 6080): textCategory =  'Instrumentos musicales y accesorios'
        if (category == 6100): textCategory =  'Música y películas (DVDs, etc.)'
        if (category == 6120): textCategory =  'Libros y revistas'
        if (category == 6140): textCategory =  'Animales y sus accesorios'
        if (category == 6160): textCategory =  'Arte, antigüedades y colecciones'
        if (category == 6180): textCategory =  'Hobbies y outdoor'
        if (category == 9020): textCategory =  'Vestuario futura mamá y niños'
        if (category == 9040): textCategory =  'Juguetes'
        if (category == 9060): textCategory =  'Coches y artículos infantiles'
        return textCategory

    def deleteCategory(self, schemaTable=None, category=None):
        try:
            textCategory=self.mappingCategory(category)
            deleteCommand = """DELETE FROM """ + schemaTable + """ WHERE category = '""" + textCategory+ """' """
            self.log.getLogInfo(deleteCommand)
            cur = self.engine.cursor()
            cur.execute(deleteCommand)
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
                batchData=[]
                for row in csv_reader:
                    rowCount += 1
                    batchData.append(row)
                    if ((rowCount > 1)  and (rowCount % 500  == 0)):
                        cur.executemany(insertQuery, batchData)
                        self.engine.commit()
            cur.close()            
        except Exception as e:
            self.log.getLogError(str(e))
            self.engine.close()
            exit()
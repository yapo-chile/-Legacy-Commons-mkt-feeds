# coding=utf-8
import logging
import pandas as pd
from infraestructure.pgsql import rawSqlToDict
from infraestructure.pgsql import database
from infraestructure.config import DatabaseConf


class extractFeed(object):

    def __init__(self):
        self.log = logging.getLogger('extractData')

    def deleteUrlSpecialCharacters(self, url):
        chars = ["á", "é", "í", "ó", "ú",
                 '!', '?', ',', ';', '¨', 'º', 'ª', '$', '#', '&']
        if any(k in chars for k in url):
            return False
        return True

    def filterCategory(self, category=None):
        filter_additional_category = ""
        filter_price = ""
        group_by = " group by 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17 "
        # Filter by category
        if (category == 2020 or category == 2060):
            filter_additional_category = """ and user_id not in (3068060,
                                                4980658,688562,3263523,
                                                4317756,3762781) """
        # Filters for price
        if (category == 1220 or category == 1240):
            filter_price = " and a.price is not null and a.price > 0 "

        if (category == 2020 or category == 2060):
            filter_price = " and a.price is not null and a.price >= 1000000 "

        if (category == 3020 or category == 3040
                or category == 3060 or category == 3080):
            filter_price = " and a.price is not null and a.price > 1000 "

        if (category == 4020 or category == 4080 or category == 5020
                or category == 5040 or category == 5060 or category == 5160
                or category == 6060 or category == 6080 or category == 6100
                or category == 6120 or category == 6160 or category == 6180):
            filter_price = " and a.price is not null and a.price > 2000 "

        # Add price group by
        if (category == 1220 or category == 1240):
            group_by = group_by + ", a.price "

        return filter_additional_category, filter_price, group_by

    def generateCaseUrl(self):
        categories = {
            1220: 'comprar',
            1240: 'arrendar',
            2020: 'autos',
            3040: 'computadores',
            3060: 'celulares',
            3020: 'consolas_videojuegos',
            3080: 'television_camaras',
            4020: 'moda-vestuario',
            4040: 'bolsos-bisuteria-accesorios',
            4060: 'salud-belleza',
            4080: 'calzado',
            5020: 'muebles',
            5040: 'electrodomesticos',
            9020: 'vestuario-futura-mama-ninos',
            9040: 'juguetes',
            9060: 'coches-articulos-infantiles',
            6020: 'deportes_gimnasia',
            6060: 'bicicletas_ciclismo',
            6080: 'instrumentos_musicales',
            6100: 'musica_peliculas',
            6120: 'libros_revistas',
            6140: 'animales_accesorios',
            6160: 'arte_antiguedades_colecciones',
            6180: 'hobbies_outdoor',
            2060: 'motos',
            5060: 'jardin_herramientas',
            5160: 'articulos-del-hogar'
        }

        region = {
            1: 'arica_parinacota',
            2: 'tarapaca',
            3: 'antofagasta',
            4: 'atacama',
            5: 'coquimbo',
            6: 'valparaiso',
            7: 'ohiggins',
            8: 'maule',
            9: 'biobio',
            10: 'araucania',
            11: 'los_rios',
            12: 'los_lagos',
            13: 'aisen',
            14: 'magallanes_antartica',
            15: 'region_metropolitana',
            16: 'nuble'
        }
        out = "case"
        for c_key, c_value in categories.items():
            for r_key, r_value in region.items():
                if c_key == 3060:
                    out += """
                        when (a.region = %d and a.category = %d)
                            then 'https://www.yapo.cl/chile?q='||
                            replace(replace(replace(replace(replace(replace(replace(
                            lower(a.subject), 'á', 'a'), 'é', 'e'), 'í', 'i')
                            , 'ó', 'o'), 'ú', 'u'), ' ', '+'), '|', '')
                        """ % (r_key, c_key)
                elif c_key == 1220 or c_key == 1240:
                    out += """
                        when (a.region = %d and a.category = %d)
                            then 'https://www.yapo.cl/%s/%s/'||
                            replace(replace(replace(replace(replace(replace(
                            replace(replace(replace(replace(replace(replace(
                            replace(replace(replace(replace(replace(replace(
                            lower(a.subject),' ','_'),'á', 'a'), 'é', 'e')
                            , 'í', 'i'), 'ó', 'o'), 'ú', 'u'),'!','_')
                            ,'?','_'),',','_'),';','_'),':','_'),'¨','_')
                            ,'º','_'),'ª','_'),'$','_'),'#','_'),'&','_')
                            , '|', '')||'_'||a.list_id||'.htm'
                    """ % (r_key, c_key, r_value, c_value)
                else:
                    out += """
                        when (a.region = %d and a.category = %d)
                            then 'https://www.yapo.cl/%s/%s/'||
                                replace(replace(lower(a.subject),' ','_')
                                , '|', '')||'_'||a.list_id||'.htm'
                    """ % (r_key, c_key, r_value, c_value)
        out += "end as url,"
        return out

    def extractProductFeed(self, category=None, ad_ids_filter=""):
        """
        Method that build the query for diferents categories
        ----------
        Parameter      type     description                 Example
        category       numeric  id of subcategory           1220
        ad_ids_filter  string   Set of ad_id split by ","   349087,456645
        -------
        Return : Dictionary
        """

        if (category is None):
            return

        filter_additional_category, filter_price, group_by = self.filterCategory(category)

        filter_uniq_category = " and category in ( " + str(category) + " ) "

        filter_ad_ids = ""
        if (ad_ids_filter != ""):
            filter_ad_ids = " and ad_id in ( " + ad_ids_filter + " ) "

        self.log.info('Extract feed from category %s' % str(category))
        self.log.info('Filter add category %s' % filter_additional_category)
        self.log.info('Filter ad ids %s' % filter_ad_ids)
        query = """
        select *
        from (select
            a.list_id::text as ad_id,
            a.ad_insertion::varchar(10),
            replace(replace(replace(replace(replace(replace(
                replace(replace(replace(replace(replace(
                    replace(replace(a.subject,'á','a')
                    ,'é','e'),'í','i'),'ó','o'),'ú','u')
                    ,'Á','A'),'É','E'),'Í','I'),'Ó','O')
                    ,'Ú','U'),'\r', ' '),'\n', '--'), '|', '') as name,
            case
                when length(am.ad_media_id::text) < 10
                    then 'https://img.yapo.cl/images/0'||
                    substring(am.ad_media_id::text, 1, 1)||'/0'||
                    (am.ad_media_id::text)||'.jpg'
                else 'https://img.yapo.cl/images/'||
                    substring(am.ad_media_id::text, 1, 2)||
                    '/'||(am.ad_media_id::text)||'.jpg'
            end as image_url,
            case
                when a.category-mod(a.category,1000) = 1000
                    then 'Inmuebles'
                when a.category-mod(a.category,1000) = 2000
                    then 'Vehiculos'
                when a.category-mod(a.category,1000) = 3000
                    then 'Computadores & electronica'
                when a.category-mod(a.category,1000) = 4000
                    then 'Moda, calzado, belleza y salud'
                when a.category-mod(a.category,1000) = 5000
                    then 'Hogar'
                when a.category-mod(a.category,1000) = 6000
                    then 'Tiempo Libre'
                when a.category-mod(a.category,1000) = 9000
                    then 'Futura mamá, bebés y niños'
            end as main_category,
            case
                when a.category = 1220
                    then 'Comprar'
                when a.category = 1240
                    then 'Arrendar'
                when a.category = 2020
                    then 'Autos, camionetas y 4x4'
                when a.category = 2060
                    then 'Motos'
                when a.category = 3020
                    then 'Consolas, videojuegos y accesorios'
                when a.category = 3040
                    then 'Computadores y accesorios'
                when a.category = 3060
                    then 'Celulares, teléfonos y accesorios'
                when a.category = 3080
                    then 'Audio, TV, video y fotografia'
                when a.category = 4020
                    then 'Moda y vestuario'
                when a.category = 4040
                    then 'Bolsos, bisutería y accesorios'
                when a.category = 4060
                    then 'Salud y belleza'
                when a.category = 4080
                    then 'Calzado'
                when a.category = 5020
                    then 'Muebles'
                when a.category = 5040
                    then 'Electrodomésticos'
                when a.category = 5060
                    then 'Jardín y herramientas'
                when a.category = 5160
                    then 'Otros artículos del hogar'
                when a.category = 6020
                    then 'Deportes, gimnasia y accesorios'
                when a.category = 6060
                    then 'Bicicletas, ciclismo y accesorios'
                when a.category = 6080
                    then 'Instrumentos musicales y accesorios'
                when a.category = 6100
                    then 'Música y películas (DVDs, etc.)'
                when a.category = 6120
                    then 'Libros y revistas'
                when a.category = 6140
                    then 'Animales y sus accesorios'
                when a.category = 6160
                    then 'Arte, antigüedades y colecciones'
                when a.category = 6180
                    then 'Hobbies y outdoor'
                when a.category = 9020
                    then 'Vestuario futura mamá y niños'
                when a.category = 9040
                    then 'Juguetes'
                when a.category = 9060
                    then 'Coches y artículos infantiles'
            end as category,
            replace(replace(replace(replace(replace(replace(replace(replace(replace(
                replace(replace(replace(replace(a.body,'á','a'),'é','e'),'í','i'),'ó','o')
                ,'ú','u'),'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U')
                ,'\r',' '), '\n', '--'), '|', '') as description,
            a.price::text,
            case
                when a.region = 1 then 'XV Arica & Parinacota'
                when a.region = 2 then 'I Tarapaca'
                when a.region = 3 then 'II Antofagasta'
                when a.region = 4 then 'III Atacama'
                when a.region = 5 then 'IV Coquimbo'
                when a.region = 6 then 'V Valparaiso'
                when a.region = 7 then 'VI OHiggins'
                when a.region = 8 then 'VII Maule'
                when a.region = 9 then 'VIII Biobio'
                when a.region = 10 then 'IX Araucania'
                when a.region = 11 then 'XIV Los Rios'
                when a.region = 12 then 'X Los Lagos'
                when a.region = 13 then 'XI Aisen'
                when a.region = 14 then 'XII Magallanes & Antartica'
                when a.region = 15 then 'Region Metropolitana'
                when a.region = 16 then 'XVI Nuble'
                else 'Undefined'
            end as region,
            %s
            case
                when ap.value = '1' then 'new'
                when ap.value = '2' then 'used'
                else 'null'
            end as "condition",
            '-' as ios_url,
            '767503903' as ios_app_store_id,
            'Yapo.cl' as ios_app_name,
            '-' as android_url,
            'cl.yapo' as android_package,
            '-' as android_app_name,
            count(mq.mail_queue_id)::text as num_ad_replies
            from (--a
                select
                    ad_id,
                    list_id,
                    list_time::date as ad_insertion,
                    subject,
                    category,
                    body,
                    price,
                    region
                from
                    ads
                where
                    status = 'active'
                    %s
                    %s
                    %s
            ) a
            inner join
                ad_media am on a.ad_id = am.ad_id and am.seq_no = 0
            left join
                ad_params ap on a.ad_id = ap.ad_id and ap."name" = 'condition'
            left join
                (select * from blocket_2019.mail_queue
                union all
                select * from blocket_2018.mail_queue) mq on
                a.list_id = mq.list_id
            where
                am.ad_media_id is not null
                %s
            %s
            order by
                count(mq.mail_queue_id) desc
            ) as data
        """ % (self.generateCaseUrl(),
                filter_uniq_category,
                filter_additional_category,
                filter_ad_ids,
                filter_price,
                group_by)
        data = rawSqlToDict(query)
        self.log.info("Extract Product Feed Successed")
        return data


def getFeedToEndpoint(category=None):
    ef = extractFeed()
    dataDict = ef.extractProductFeed(category)
    dbConfig = DatabaseConf('ENDPOINT')
    dbWrite = database(dbConfig['host'],
                       dbConfig['port'],
                       dbConfig['dbname'],
                       dbConfig['user'],
                       dbConfig['password'])
    dbWrite.copyStringIterator('dm_analysis.data_feed', dataDict)
    dbWrite.closeConnection()


def mainExtract():
    categoryList = [1220, 1240,
                    2020, 2060,
                    3060, 3040, 3020, 3080,
                    4020, 4080,
                    5020, 5040, 5060, 5160,
                    6020, 6060, 6080, 6100, 6120, 6140, 6160, 6180]
    categoryList = [1220, 1240]
    for category in categoryList:
        getFeedToEndpoint(category)

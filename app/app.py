import logging
import sys
from flask import Flask, request
import domain as d
import interfaces.handlers as h
from infraestructure.config import Config
from infraestructure.migrations import Migrations
from infraestructure.pgsql import Pgsql, Datasource
from infraestructure.catalog import CatalogConf
from usecases.catalog import CatalogUsecases
from usecases.refresh import RefreshUsecases
from interfaces.repository.catalogRepo import CatalogRepo
from interfaces.repository.extractDataRepo import ExtractDataRepo
from interfaces.repository.currencyRepo import CurrencyRepo


APP = Flask(__name__)
CONFIG: Config = Config()

# Logger initial conf
LOGGER = logging.getLogger(CONFIG.logger.LogLevel)
LOGGER.setLevel(LOGGER.level)
LOGGER.info(CONFIG)

# Start Database
DB: Pgsql = Pgsql(CONFIG.database)
if not DB.start():
    LOGGER.error("Error with Database, closing ....")
    sys.exit()

# Apply migrations
MIGRATIONS: Migrations = Migrations(CONFIG.database)
MIGRATIONS.migrate()

DATASOURCE: Datasource = Datasource(CONFIG.databaseSource)
# Start catalog conf
CATALOG_CONF: CatalogConf = CatalogConf(CONFIG.aws)

# Initiallize
# Repos
CATALOG_REPO: CatalogRepo = CatalogRepo(DB, CATALOG_CONF)
EXTRACT_DATA_REPO: ExtractDataRepo = ExtractDataRepo(
    DB,
    CONFIG.database,
    DATASOURCE)
CURRENCY_REPO: CurrencyRepo = CurrencyRepo(CONFIG.ufConf)
# Usecases
CATALOG: CatalogUsecases = CatalogUsecases(CATALOG_REPO, CURRENCY_REPO, CONFIG.server, LOGGER)
REFRESH: RefreshUsecases = RefreshUsecases(EXTRACT_DATA_REPO)

# Handlers
CATALOG_HANDLER = h.CatalogHandler(
    config=CONFIG,
    catalog=CATALOG,
    logger=LOGGER
)

DATA_EXTRACTOR_HANDLER = h.DataExtractorHandler(
    dataextractor=REFRESH
)

HEALTHCHECK_HANDLER = h.HealthcheckHandler()

# /healthcheck returns service status
@APP.route("/healthcheck", methods=['GET'])
def healthcheck() -> d.JSONType:
    '''healthCheck route'''
    return HEALTHCHECK_HANDLER.status()

# /catalog/create trigger process to re-create all
# files configured on config file
@APP.route('/catalog/create', methods=['GET'])
def catalogCreateAll() -> d.JSONType:
    '''Catalog route'''
    return CATALOG_HANDLER.createAll()

# /catalog/create trigger process to re-create a
# file configured on config file
@APP.route('/catalog/create/<catalog_id>', methods=['GET'])
def catalogCreate(catalog_id) -> d.JSONType:
    '''Catalog route'''
    return CATALOG_HANDLER.create(d.CatalogId(catalog_id))

# /catalog/get/<catalog_id> returns a file using a catalog_id value
@APP.route('/catalog/get/<catalog_id>', methods=['GET'])
def catalogGet(catalog_id) -> d.JSONType:
    '''Catalog route'''
    appendList = request.args.getlist("file", type=str)
    return CATALOG_HANDLER.get(d.CatalogId(catalog_id), appendList)

# /refresh trigger process to delete db data and recreate it
@APP.route('/refresh', methods=['GET'])
def dataExtractor() -> d.JSONType:
    return DATA_EXTRACTOR_HANDLER.runExtractData()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    APP.run(host=CONFIG.server.Host,
            port=CONFIG.server.Port,
            debug=CONFIG.server.Debug,
            threaded=True)

import io
import domain as d
import logging
from .handler import Response
from interfaces.repository.extractData import mainExtract


def RunExtractData():
    mainExtract()
    r = Response(200)
    return r.toJson(msg=d.JSONType({"status": "Load data OK"}))

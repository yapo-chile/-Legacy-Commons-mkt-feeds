import io
import domain as d
import logging
from multiprocessing import Process
from .handler import Response
from interfaces.repository.extractData import generate


def runExtractData():
    generate()
    r = Response(202)
    return r.toJson(msg=d.JSONType({"status": "Load process started"}))

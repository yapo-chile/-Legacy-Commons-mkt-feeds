import io
import domain as d
from multiprocessing import Process
from .handler import Response
from interfaces.repository.extractData import generate


# runExtractData calls a process to fill db with ads
def runExtractData() -> d.JSONType:
    generate()
    r = Response(202)
    return r.toJson(msg=d.JSONType({"status": "Load process started"}))

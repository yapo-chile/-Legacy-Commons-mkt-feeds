import io
import domain as d
from .handler import Response


class DataExtractorHandler():
    # DataExtractorHandler implements the handler interface
    # and responds to [GET] /refresh
    # requests, then executes the refresh process and returns the response
    def __init__(
            self,
            dataextractor) -> None:
        self.dataextractor = dataextractor

    # runExtractData calls a process to fill db with ads
    def runExtractData(self) -> d.JSONType:
        self.dataextractor.generate()
        r = Response(202)
        return r.toJson(msg=d.JSONType({"status": "Load process started"}))

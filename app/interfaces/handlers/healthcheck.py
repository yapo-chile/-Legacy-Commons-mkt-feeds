import domain as d
from .handler import Response


class HealthcheckHandler():
    # status returns a JSONType object with a
    # success msg
    def status(self) -> d.JSONType:
        r = Response(200)
        return r.toJson(msg=d.JSONType({"status": "OK"}))

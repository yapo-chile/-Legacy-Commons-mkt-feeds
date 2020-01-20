import domain as d
from .handler import Response


# healthcheckHandlers returns a JSONType object with a
# success msg
def healthcheckHandler() -> d.JSONType:
    r = Response(200)
    return r.toJson(msg=d.JSONType({"status": "OK"}))

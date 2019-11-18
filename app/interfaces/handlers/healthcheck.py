import domain as d
from .logger import Response

def Status() -> d.JSONType:
    return Response(d.StatusCode(200)).Success('OK')

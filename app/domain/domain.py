from typing import Union, Any, List, Dict, NewType

# Json format
JSONType = NewType("JSONType", Dict[str, Any])

# Api Rest Code Status format
StatusCode = NewType("StatusCode", int)

# Catalog Id Format
CatalogId = NewType("CatalogId", int)

# Validates rest status code value
def ValidateRestStatusCode(code: StatusCode) -> StatusCode:
    if code >= 200 and code <= 208 or \
       code >= 300 and code <= 308 or \
       code >= 400 and code <= 451 or \
       code >= 500 and code <= 511:
       pass
    else:
        raise Exception("Wrong rest status code")
    return code

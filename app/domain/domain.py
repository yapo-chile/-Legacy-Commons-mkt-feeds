from http import HTTPStatus
from typing import Any, List, Dict, NewType

# Json format
JSONType = NewType("JSONType", Dict[str, Any])

# Api Rest Code Status format
StatusCode = NewType("StatusCode", int)

# Catalog Id Format
CatalogId = NewType("CatalogId", int)

# Condition Format
Condition = NewType("Condition", str)

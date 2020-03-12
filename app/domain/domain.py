from typing import Any, Dict, NewType

# Json format
JSONType = NewType("JSONType", Dict[str, Any])

# CatalogConfig stores a dict with json objects
CatalogConfig = NewType("CatalogConfig", Dict[str, JSONType])

# Api Rest Code Status format
StatusCode = NewType("StatusCode", int)

# Catalog Id Format
CatalogId = NewType("CatalogId", int)

# Condition Format
Condition = NewType("Condition", str)

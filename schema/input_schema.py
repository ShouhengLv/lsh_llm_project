import jsonschema
from jsonschema import validate, ValidationError

INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "prompt": {"type": "string"},
        "temperature": {"type": "number", "minimum": 0.0, "maximum": 2.0}
    },
    "required": ["prompt"]
}


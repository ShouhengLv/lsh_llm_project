from jsonschema import validate, ValidationError

# 输出 JSON 应该符合这个结构
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "source": {"type": "string"},
        "confidence": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0
        },
        "chat_text": {"type": "string"}
    },
    "required": ["answer", "source", "confidence", "chat_text"]
}

def validate_output_structure(data: dict):
    validate(instance=data, schema=OUTPUT_SCHEMA)

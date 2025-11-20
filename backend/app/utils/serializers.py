import json

def dumps_json(value):
    """Convert Python lists/dicts to a JSON string."""
    if value is None:
        return None
    return json.dumps(value)

def loads_json(value):
    """Convert JSON string to Python lists/dicts."""
    if value in [None, ""]:
        return None
    return json.loads(value)

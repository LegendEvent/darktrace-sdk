import base64
import json

def debug_print(message: str, debug: bool = False):
    if debug:
        print(f"[DEBUG] {message}")

def encode_query(query: dict) -> str:
    query_json = json.dumps(query)
    return base64.b64encode(query_json.encode()).decode() 
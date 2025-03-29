import os
import json
import time

CACHE_DIR = ".kite_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_path(key):
    return os.path.join(CACHE_DIR, f"{key}.json")

def save_cache(key, data):
    payload = {
        "timestamp": time.time(),
        "data": data
    }
    with open(get_cache_path(key), "w") as f:
        json.dump(payload, f)

def load_cache(key, ttl_seconds):
    path = get_cache_path(key)
    if not os.path.exists(path):
        return None, None

    with open(path) as f:
        payload = json.load(f)

    age = time.time() - payload["timestamp"]
    if age > ttl_seconds:
        return None, None

    return payload["data"], payload["timestamp"]


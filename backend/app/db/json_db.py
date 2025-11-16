import json
import os
import threading

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "database.json")

# Ensure path resolves correctly
DB_PATH = os.path.abspath(DB_PATH)

# A lock to avoid race conditions:
db_lock = threading.Lock()


def load_db():
    """
    Load and return the full JSON DB structure.
    """
    if not os.path.exists(DB_PATH):
        return {"users": {}, "profiles": {}}

    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Corrupt file fallback
            return {"users": {}, "profiles": {}}


def save_db(db):
    """
    Safely write DB to disk (atomic).
    """
    with db_lock:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)

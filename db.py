# db.py - All DB functions: init, create table, insert, update, select
import os
import sqlite3
from typing import Optional, Dict, Any, List

MAX_SUBSCRIBERS = 150

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT,
    location TEXT,
    lon REAL,
    lat REAL,
    channel TEXT,
    send_time_morning TEXT,
    send_time_afternoon TEXT,
    wind INTEGER,
    gust INTEGER,
    gif INTEGER,
    forecast_days INTEGER,
    only_weird_weather INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def get_conn(db_path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str):
    """Create database and table if not exists"""

    print()
    for _ in range(3):
        print(f"Initializing database at {db_path}...")

    #print("[DEBUG] Checking /data...")                # or /db, locally
    #print("[DEBUG] Exists:", os.path.exists("/data")) # or /db, locally
    #print("[DEBUG] Contents:", os.listdir("/data"))   # or /db, locally

    try:
        conn = get_conn(db_path)
        with conn:
            conn.execute(CREATE_TABLE_SQL)
    except Exception as e:
        print("Database init failed:", e)
    finally:
        conn.close()

def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {k: row[k] for k in row.keys()}

def insert_subscriber(db_path: str, data: Dict[str, Any]) -> int:
    """Insert a new subscriber row. Returns inserted row id."""
    conn = get_conn(db_path)
    with conn:
        cur = conn.execute("""
            INSERT INTO subscribers (
                phone_number, location, lon, lat, channel,
                send_time_morning, send_time_afternoon,
                wind, gust, gif, forecast_days, only_weird_weather
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("phone_number"),
            data.get("location"),
            data.get("lon"),
            data.get("lat"),
            data.get("channel"),
            data.get("send_time_morning"),
            data.get("send_time_afternoon"),
            1 if data.get("wind") else 0,
            1 if data.get("gust") else 0,
            1 if data.get("gif") else 0,
            data.get("forecast_days"),
            1 if data.get("only_weird_weather") else 0,
        ))
        last_id = cur.lastrowid
    conn.close()
    return last_id

def update_subscribers_by_phone(db_path: str, phone: str, data: Dict[str, Any]) -> int:
    """
    Update all subscriber rows matching the provided phone number.
    Returns the number of rows updated.
    """
    conn = get_conn(db_path)
    with conn:
        cur = conn.execute("""
            UPDATE subscribers
            SET location = ?, lon = ?, lat = ?, channel = ?,
                send_time_morning = ?, send_time_afternoon = ?,
                wind = ?, gust = ?, gif = ?, forecast_days = ?, only_weird_weather = ?, updated_at = CURRENT_TIMESTAMP
            WHERE phone_number = ?
        """, (
            data.get("location"),
            data.get("lon"),
            data.get("lat"),
            data.get("channel"),
            data.get("send_time_morning"),
            data.get("send_time_afternoon"),
            1 if data.get("wind") else 0,
            1 if data.get("gust") else 0,
            1 if data.get("gif") else 0,
            data.get("forecast_days"),
            1 if data.get("only_weird_weather") else 0,
            phone
        ))
        updated = cur.rowcount
    conn.close()
    return updated

def get_subscriber_by_phone(db_path: str, phone: str) -> Optional[Dict[str, Any]]:
    conn = get_conn(db_path)
    cur = conn.execute("SELECT * FROM subscribers WHERE phone_number = ? ORDER BY id LIMIT 1", (phone,))
    row = cur.fetchone()
    conn.close()
    return row_to_dict(row) if row else None

def get_all_subscribers(db_path: str) -> List[Dict[str, Any]]:
    conn = get_conn(db_path)
    cur = conn.execute("SELECT * FROM subscribers ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

def add_or_update_subscriber(db_path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    phone = data.get("phone_number")
    if not phone:
        raise ValueError("phone_number is required")

    existing = get_subscriber_by_phone(db_path, phone)
    if existing:
        updated = update_subscribers_by_phone(db_path, phone, data)
        return {"action": "updated", "rows": updated}

    # enforce total DB limit
    conn = get_conn(db_path)
    count = conn.execute("SELECT COUNT(*) FROM subscribers").fetchone()[0]
    conn.close()
    if count >= MAX_SUBSCRIBERS:
        raise ValueError("Subscriber limit reached")

    new_id = insert_subscriber(db_path, data)
    return {"action": "inserted", "id": new_id}

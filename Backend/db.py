import os
import sqlite3
from pathlib import Path
from typing import Any

DATABASE_PATH = Path(os.getenv("FLOWER_DB_PATH", Path(__file__).resolve().parents[1].joinpath("Database", "flower_shop.db")))


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        sql_text = Path(__file__).resolve().parents[1].joinpath("Database", "schema.sql").read_text(encoding="utf-8")
        conn.executescript(sql_text)
        conn.commit()
    seed_default_data()


def seed_default_data() -> None:
    if query_one("SELECT 1 FROM categories LIMIT 1"):
        return
    execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", ("Roses", "Classic rose bouquets."))
    execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", ("Seasonal", "Seasonal flowers and arrangements."))
    execute(
        "INSERT OR IGNORE INTO flowers (name, category_id, price, stock, description, season) VALUES (?, ?, ?, ?, ?, ?)",
        ("Red Rose", 1, 39.99, 10, "Fresh red roses for romance.", "Valentine"),
    )
    execute(
        "INSERT OR IGNORE INTO flowers (name, category_id, price, stock, description, season) VALUES (?, ?, ?, ?, ?, ?)",
        ("Tulip Bouquet", 2, 29.99, 4, "Bright mixed tulips for spring.", "Spring"),
    )
    execute(
        "INSERT OR IGNORE INTO care_instructions (flower_id, topic, content) VALUES (?, ?, ?)",
        (1, "water", "Keep roses hydrated with fresh water daily."),
    )
    execute(
        "INSERT OR IGNORE INTO care_instructions (flower_id, topic, content) VALUES (?, ?, ?)",
        (2, "sunlight", "Tulips enjoy bright, indirect sunlight."),
    )
    execute(
        "INSERT OR IGNORE INTO promotions (code, description, discount_percent, active) VALUES (?, ?, ?, ?)",
        ("SPRING10", "10% off seasonal bouquets", 10, 1),
    )
    execute(
        "INSERT OR IGNORE INTO support_articles (title, content) VALUES (?, ?)",
        ("Flower care tips", "Keep stems clean and change water every two days."),
    )


def query_all(sql: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
    with get_connection() as conn:
        cursor = conn.execute(sql, params)
        return cursor.fetchall()


def query_one(sql: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
    with get_connection() as conn:
        cursor = conn.execute(sql, params)
        return cursor.fetchone()


def execute(sql: str, params: tuple[Any, ...] = ()) -> int:
    with get_connection() as conn:
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor.lastrowid


def check_connection() -> bool:
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return True
    except sqlite3.Error:
        return False

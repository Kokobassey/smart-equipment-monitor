
import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "sensor_readings.db"
)


def initialize_database():
    """Create the sensor readings table if it doesn't exist."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL NOT NULL,
                vibration REAL NOT NULL,
                status TEXT NOT NULL,
                alerts TEXT NOT NULL
            )
        """)


def save_reading(reading, analysis):
    """Save one sensor reading and its analysis to the database."""

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            INSERT INTO sensor_readings (
                timestamp,
                temperature,
                vibration,
                status,
                alerts
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            reading["timestamp"],
            reading["temperature"],
            reading["vibration"],
            analysis["status"],
            "; ".join(analysis["alerts"]),
        ))


def get_recent_readings(limit=10):
    """Return the most recent saved readings."""

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute("""
            SELECT *
            FROM sensor_readings
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]


if __name__ == "__main__":
    initialize_database()
    print(f"Database ready at: {DATABASE_PATH}")

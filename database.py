
import sqlite3

DATABASE = "plantdoc.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT,
            predicted_disease TEXT,
            confidence REAL,
            risk_level TEXT,
            risk_score INTEGER,
            recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_report(report):
    connection = get_connection()
    cursor = connection.cursor()

    plant = report["plant_analysis"]
    environment = report["environment_analysis"]

    cursor.execute("""
        INSERT INTO reports (
            crop,
            predicted_disease,
            confidence,
            risk_level,
            risk_score,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        environment["crop"],
        plant["predicted_disease"],
        plant["confidence"],
        environment["risk_level"],
        environment["risk_score"],
        environment["recommendation"]
    ))

    connection.commit()
    connection.close()


def get_all_reports():
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reports ORDER BY id DESC")

    reports = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return reports

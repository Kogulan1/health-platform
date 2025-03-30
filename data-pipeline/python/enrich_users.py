import pyodbc
import uuid
from faker import Faker
from dotenv import load_dotenv
import os
import random
from datetime import datetime, timedelta

load_dotenv()
faker = Faker()

# DB connection
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={os.getenv('SQL_SERVER')},{os.getenv('SQL_PORT')};"
    f"DATABASE={os.getenv('SQL_DB')};"
    f"UID={os.getenv('SQL_USER')};"
    f"PWD={os.getenv('SQL_PASSWORD')};"
     f"Encrypt=yes;"
    f"TrustServerCertificate=yes;"
)
cursor = conn.cursor()


def insert_device(user_id):
    device_id = str(uuid.uuid4())
    platform = random.choice(["iOS", "Android"])
    model = faker.word() + " " + str(random.randint(10, 20))
    os_version = f"{random.randint(12, 17)}.{random.randint(0, 5)}"
    app_version = f"{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
    last_sync_time = faker.date_time_between(start_date='-7d', end_date='now')

    cursor.execute("""
        INSERT INTO user_devices (device_id, user_id, platform, model, os_version, app_version, last_sync_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, device_id, user_id, platform, model, os_version, app_version, last_sync_time)

    return platform, model


def insert_preferences(user_id):
    cursor.execute("""
        INSERT INTO user_preferences (user_id, prefers_notifications, language, dark_mode_enabled, marketing_opt_in)
        VALUES (?, ?, ?, ?, ?)
    """, user_id,
         random.choice([0, 1]),
         random.choice(['en', 'fr', 'de', 'es']),
         random.choice([0, 1]),
         random.choice([0, 1])
    )


def insert_health_events(user_id, platform, device_model):
    for _ in range(random.randint(5, 15)):
        event_id = str(uuid.uuid4())
        timestamp = faker.date_time_this_month()
        data_type = random.choice(['heart_rate', 'steps', 'spo2', 'respiration_rate'])

        if data_type == 'heart_rate':
            value_numeric = round(random.uniform(60, 100), 1)
        elif data_type == 'steps':
            value_numeric = round(random.uniform(100, 1500), 0)
        elif data_type == 'spo2':
            value_numeric = round(random.uniform(95, 100), 1)
        else:
            value_numeric = round(random.uniform(12, 20), 1)

        unit = {
            'heart_rate': 'bpm',
            'steps': 'steps',
            'spo2': '%',
            'respiration_rate': 'rpm'
        }[data_type]

        metadata = f"{{'source': '{platform}', 'device': '{device_model}'}}"

        cursor.execute("""
            INSERT INTO raw_health_events (event_id, user_id, platform, device_model, timestamp,
            data_type, value_numeric, value_string, unit, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, event_id, user_id, platform, device_model, timestamp, data_type, value_numeric, None, unit, metadata)


def run():
    print("Enriching existing users...")
    cursor.execute("SELECT user_id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    for user_id in user_ids:
        platform, model = insert_device(user_id)
        insert_preferences(user_id)
        insert_health_events(user_id, platform, model)

    conn.commit()
    print("✅ All users enriched with devices, preferences, and health events.")


if __name__ == "__main__":
    run()

import pyodbc
import uuid
from faker import Faker
from dotenv import load_dotenv
import os
import random

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

def insert_user():
    user_id = str(uuid.uuid4())
    full_name = faker.name()
    email = faker.unique.email()
    dob = faker.date_of_birth(minimum_age=18, maximum_age=80)
    gender = random.choice(["Male", "Female", "Other"])
    country = faker.country()
    consent_data = random.choice([0, 1])
    consent_trials = random.choice([0, 1])

    cursor.execute("""
        INSERT INTO users (user_id, full_name, email, date_of_birth, gender, country,
            consent_to_data, consent_to_trials)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, user_id, full_name, email, dob, gender, country, consent_data, consent_trials)

    return user_id, email

def insert_auth(user_id, email):
    provider_id = str(uuid.uuid4())
    provider_type = random.choice(["google", "apple", "email_password"])
    provider_user_id = str(uuid.uuid4())

    cursor.execute("""
        INSERT INTO auth_providers (provider_id, user_id, provider_type, provider_user_id, email, is_primary)
        VALUES (?, ?, ?, ?, ?, 1)
    """, provider_id, user_id, provider_type, provider_user_id, email)

def run():
    print("Inserting 300 users...")
    for _ in range(300):
        user_id, email = insert_user()
        insert_auth(user_id, email)
    conn.commit()
    print("✅ Done inserting 300 users + auth records.")

if __name__ == "__main__":
    run()

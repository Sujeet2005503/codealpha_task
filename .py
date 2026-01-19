
import sqlite3
import hashlib
from difflib import SequenceMatcher
connection = sqlite3.connect("cloud_database.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS data_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT UNIQUE,
    data_hash TEXT UNIQUE
)
""")
connection.commit()
def generate_hash(data):
    hash_value = hashlib.sha256(data.encode()).hexdigest()
    return hash_value
def similarity_check(data1, data2):
    similarity_ratio = SequenceMatcher(None, data1, data2).ratio()
    return similarity_ratio
def validate_data(new_data):
    new_hash = generate_hash(new_data)

    cursor.execute("SELECT data, data_hash FROM data_records")
    records = cursor.fetchall()

    for existing_data, existing_hash in records:

        # Step 6.1: Check Exact Duplicate
        if new_hash == existing_hash:
            return "REDUNDANT"

        # Step 6.2: Check False Positive
        similarity = similarity_check(new_data, existing_data)
        if similarity > 0.85:
            return "FALSE_POSITIVE"

    return "UNIQUE"
def insert_data(new_data):
    result = validate_data(new_data)

    if result == "UNIQUE":
        data_hash = generate_hash(new_data)
        cursor.execute(
            "INSERT INTO data_records (data, data_hash) VALUES (?, ?)",
            (new_data, data_hash)
        )
        connection.commit()
        print("✅ Data inserted successfully")

    elif result == "REDUNDANT":
        print("❌ Duplicate data detected. Insertion blocked")

    elif result == "FALSE_POSITIVE":
        print("⚠ Similar data found (False Positive). Review required")
while True:
    print("\n----- DATA REDUNDANCY REMOVAL SYSTEM -----")
    print("1. Add New Data")
    print("2. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        user_data = input("Enter data: ")
        insert_data(user_data)

    elif choice == "2":
        print("System closed.")
        break

    else:
        print("Invalid choice. Try again.")
connection.close()

import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "instance/jarvis.db"

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL)''')
    
    # Insert predefined users
    users = [
        ("haris", "haris@gmail.com", generate_password_hash("3103"), "admin"),
        ("abdul", "abdul@gmail.com", generate_password_hash("1610"), "user"),
        ("razia", "razia@gmail.com", generate_password_hash("2405"), "user")
    ]
    
    for user in users:
        try:
            cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", user)
        except sqlite3.IntegrityError:
            print(f"User {user[0]} already exists.")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()

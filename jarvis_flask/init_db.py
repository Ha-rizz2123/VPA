import sqlite3
from werkzeug.security import generate_password_hash
import os

DB_PATH = "instance/jarvis.db"

# Ensure instance folder exists
if not os.path.exists("instance"):
    os.makedirs("instance")

# Connect to the new database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create Users Table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
''')

# Add an Admin User
admin_password = generate_password_hash("admin123")  # Default admin password
cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", admin_password, "admin"))

conn.commit()
conn.close()

print("Database initialized successfully! Admin user created (Username: admin, Password: admin123)")

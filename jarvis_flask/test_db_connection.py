import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "instance/jarvis.db"  # Adjust if needed

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Fetch all users
cursor.execute("SELECT username, password FROM users")
users = cursor.fetchall()

for username, password in users:
    hashed_password = generate_password_hash(password)
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))

conn.commit()
conn.close()

print("Passwords updated successfully!")

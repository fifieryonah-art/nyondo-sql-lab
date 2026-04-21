import sqlite3

conn = sqlite3.connect('nyondo_stock.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'attendant'
)
''')

users = [
    ('admin', 'admin123', 'admin'),
    ('fatuma', 'pass456', 'attendant'),
    ('wasswa', 'pass789', 'manager')
]

cursor.executemany('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)', users)
conn.commit()

print("Users table created successfully!")
print("\n=== ALL USERS ===")
rows = cursor.execute('SELECT * FROM users').fetchall()
for row in rows:
    print(f"ID: {row[0]}, Username: {row[1]}, Password: {row[2]}, Role: {row[3]}")

conn.close()
print("\n✓ Users table added! Now run: python vulnerable.py")

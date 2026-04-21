import sqlite3

# Connect to database (creates file if doesn't exist)
conn = sqlite3.connect('nyondo_stock.db')
cursor = conn.cursor()

# Create products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL
)
''')

print("Table 'products' created successfully.")

# Insert all 5 products using a single INSERT command (executemany)
products = [
    ('Cement (bag)', 'Portland cement 50kg bag', 35000),
    ('Iron Sheet 3m', 'Gauge 30 roofing sheet 3m long', 110000),
    ('Paint 5L', 'Exterior wall paint white 5L', 60000),
    ('Nails 1kg', 'Common wire nails 1kg pack', 12000),
    ('Timber 2x4', 'Pine timber plank 2x4 per metre', 25000)
]

cursor.executemany('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', products)
conn.commit()

print(f"{cursor.rowcount} products inserted successfully.")
print("\n=== ALL PRODUCTS ===")

# Display all products
rows = cursor.execute('SELECT * FROM products').fetchall()
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Description: {row[2]}, Price: UGX {row[3]:,.0f}")

conn.close()
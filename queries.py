import sqlite3

conn = sqlite3.connect('nyondo_stock.db')

print("=" * 60)
print("QUERY A: Get every column of every product")
print("=" * 60)
query_a = "SELECT * FROM products"
rows = conn.execute(query_a).fetchall()
for row in rows:
    print(row)
print()

print("=" * 60)
print("QUERY B: Get only the name and price of all products")
print("=" * 60)
query_b = "SELECT name, price FROM products"
rows = conn.execute(query_b).fetchall()
for row in rows:
    print(f"Product: {row[0]}, Price: UGX {row[1]:,.0f}")
print()

print("=" * 60)
print("QUERY C: Get full details of the product with id = 3")
print("=" * 60)
query_c = "SELECT * FROM products WHERE id = 3"
row = conn.execute(query_c).fetchone()
print(f"ID: {row[0]}, Name: {row[1]}, Desc: {row[2]}, Price: UGX {row[3]:,.0f}")
print()

print("=" * 60)
print("QUERY D: Find all products whose name contains 'sheet'")
print("=" * 60)
query_d = "SELECT * FROM products WHERE name LIKE '%sheet%'"
rows = conn.execute(query_d).fetchall()
for row in rows:
    print(row)
print()

print("=" * 60)
print("QUERY E: Get all products sorted by price, highest first")
print("=" * 60)
query_e = "SELECT * FROM products ORDER BY price DESC"
rows = conn.execute(query_e).fetchall()
for row in rows:
    print(f"{row[1]}: UGX {row[3]:,.0f}")
print()

print("=" * 60)
print("QUERY F: Get only the 2 most expensive products")
print("=" * 60)
query_f = "SELECT * FROM products ORDER BY price DESC LIMIT 2"
rows = conn.execute(query_f).fetchall()
for row in rows:
    print(f"{row[1]}: UGX {row[3]:,.0f}")
print()

print("=" * 60)
print("QUERY G: Update Cement price to 38,000 and confirm")
print("=" * 60)
query_g_update = "UPDATE products SET price = 38000 WHERE id = 1"
conn.execute(query_g_update)
conn.commit()
query_g_select = "SELECT * FROM products WHERE id = 1"
row = conn.execute(query_g_select).fetchone()
print(f"UPDATED: {row[1]} now costs UGX {row[3]:,.0f}")

conn.close()
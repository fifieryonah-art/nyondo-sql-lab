import sqlite3

conn = sqlite3.connect('nyondo_stock.db')

def search_product_safe(name):
    # SECURE: Using ? placeholder - user input NEVER goes directly into query string
    query = "SELECT * FROM products WHERE name LIKE ?"
    param = f'%{name}%'
    print(f'[QUERY] {query}')
    print(f'[PARAM] {param}')
    rows = conn.execute(query, (param,)).fetchall()
    print(f'[RESULT] {rows}\n')
    return rows

def login_safe(username, password):
    # SECURE: Using ? placeholders for both username and password
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f'[QUERY] {query}')
    print(f'[PARAMS] username={username}, password={password}')
    row = conn.execute(query, (username, password)).fetchone()
    print(f'[RESULT] {row}\n')
    return row

print("\n" + "=" * 60)
print("TEST 1: Attack with OR 1=1 - Should return empty")
print("=" * 60)
result = search_product_safe("' OR 1=1--")
print(f"FINAL RESULT: {result} (empty list = safe)")

print("\n" + "=" * 60)
print("TEST 2: UNION attack - Should return empty")
print("=" * 60)
result = search_product_safe("' UNION SELECT id,username,password,role FROM users--")
print(f"FINAL RESULT: {result} (empty list = safe)")

print("\n" + "=" * 60)
print("TEST 3: Login bypass with comment - Should return None")
print("=" * 60)
result = login_safe("admin'--", "anything")
print(f"FINAL RESULT: {result} (None = safe)")

print("\n" + "=" * 60)
print("TEST 4: Always true login - Should return None")
print("=" * 60)
result = login_safe("' OR '1'='1", "' OR '1'='1")
print(f"FINAL RESULT: {result} (None = safe)")

conn.close()

import sqlite3

conn = sqlite3.connect('nyondo_stock.db')

# ========== VALIDATION FUNCTIONS ==========

def validate_product_name(name):
    """Validate product name: string, at least 2 chars, no < > or ;"""
    if not isinstance(name, str):
        return False, "Name must be a string"
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    if '<' in name or '>' in name or ';' in name:
        return False, "Name cannot contain < > or ; characters"
    return True, ""

def validate_username(username):
    """Validate username: string, no spaces, not empty"""
    if not isinstance(username, str):
        return False, "Username must be a string"
    if len(username) == 0:
        return False, "Username cannot be empty"
    if ' ' in username:
        return False, "Username cannot contain spaces"
    return True, ""

def validate_password(password):
    """Validate password: string, at least 6 characters"""
    if not isinstance(password, str):
        return False, "Password must be a string"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""

# ========== SECURE FUNCTIONS WITH VALIDATION ==========

def search_product_safe(name):
    # INPUT VALIDATION FIRST
    valid, error = validate_product_name(name)
    if not valid:
        print(f"[VALIDATION ERROR] {error}")
        print(f"[RESULT] []\n")
        return []
    
    # PARAMETERISED QUERY
    query = "SELECT * FROM products WHERE name LIKE ?"
    param = f'%{name}%'
    print(f'[QUERY] {query}')
    print(f'[PARAM] {param}')
    rows = conn.execute(query, (param,)).fetchall()
    print(f'[RESULT] {rows}\n')
    return rows

def login_safe(username, password):
    # INPUT VALIDATION FIRST
    valid_user, user_error = validate_username(username)
    if not valid_user:
        print(f"[VALIDATION ERROR] {user_error}")
        print(f"[RESULT] None\n")
        return None
    
    valid_pass, pass_error = validate_password(password)
    if not valid_pass:
        print(f"[VALIDATION ERROR] {pass_error}")
        print(f"[RESULT] None\n")
        return None
    
    # PARAMETERISED QUERY
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f'[QUERY] {query}')
    print(f'[PARAMS] username={username}, password={password}')
    row = conn.execute(query, (username, password)).fetchone()
    print(f'[RESULT] {row}\n')
    return row

# ========== TEST CASES ==========

print("\n" + "=" * 60)
print("VALIDATION TEST CASES")
print("=" * 60)

print("\n--- Test 1: search_product_safe('cement') ---")
print("Expected: Works normally, returns matching products")
search_product_safe('cement')

print("\n--- Test 2: search_product_safe('') ---")
print("Expected: REJECTED (empty string)")
search_product_safe('')

print("\n--- Test 3: search_product_safe('<script>') ---")
print("Expected: REJECTED (contains < >)")
search_product_safe('<script>')

print("\n--- Test 4: login_safe('admin', 'admin123') ---")
print("Expected: Works normally, returns admin user")
login_safe('admin', 'admin123')

print("\n--- Test 5: login_safe('admin', 'ab') ---")
print("Expected: REJECTED (password too short - needs 6+ chars)")
login_safe('admin', 'ab')

print("\n--- Test 6: login_safe('ad min', 'pass123') ---")
print("Expected: REJECTED (space in username)")
login_safe('ad min', 'pass123')

conn.close()
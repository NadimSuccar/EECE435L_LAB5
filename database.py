# database.py
import sqlite3

def connect_to_db():
    conn = sqlite3.connect('users.db')  # Create or connect to the SQLite database
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("User table created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()

def insert_user(user):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
                    (user['name'], user['email'], user['phone'], user['address'], user['country']))
        conn.commit()
        user_id = cur.lastrowid
        return get_user_by_id(user_id)
    except Exception as e:
        print(f"Error inserting user: {e}")
    finally:
        conn.close()

user = {
    "name": "John Doe",
    "email": "jondoe@gamil.com",
    "phone": "067765434567",
    "address": "John Doe Street, Innsbruck",
    "country": "Austria"
}

def get_users():
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        users = [dict(row) for row in rows]
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        conn.close()

def get_user_by_id(user_id):
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            return dict(row)
        return None
    except Exception as e:
        print(f"Error fetching user by id: {e}")
        return None
    finally:
        conn.close()

def update_user(user):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?",
                    (user['name'], user['email'], user['phone'], user['address'], user['country'], user['user_id']))
        conn.commit()
        return get_user_by_id(user['user_id'])
    except Exception as e:
        print(f"Error updating user: {e}")
        return None
    finally:
        conn.close()

def delete_user(user_id):
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        return {"status": "User deleted successfully"}
    except Exception as e:
        print(f"Error deleting user: {e}")
        return {"status": "Error deleting user"}
    finally:
        conn.close()

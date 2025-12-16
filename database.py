import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

class UserDatabase:
    def __init__(self):
        self.db_path = 'users.db'
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def create_user(self, username, email, password):
        try:
            conn = sqlite3.connect(self.db_path)
            password_hash = generate_password_hash(password)
            conn.execute('INSERT INTO users VALUES (?, ?, ?)', 
                        (username, email, password_hash))
            conn.commit()
            conn.close()
            
            # Create user's folder
            os.makedirs(f"user_data/{username}", exist_ok=True)
            return True
        except:
            return False
    
    def verify_password(self, username, password):
        conn = sqlite3.connect(self.db_path)
        result = conn.execute('SELECT password_hash FROM users WHERE username = ?', 
                            (username,)).fetchone()
        conn.close()
        
        if result and check_password_hash(result[0], password):
            return True
        return False
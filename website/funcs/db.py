import sqlite3, json, re, datetime
import hashlib, os


class Users(object):
    @staticmethod
    def _get_db_path():
        """Helper method to get consistent database path"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "dbs", "users.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return db_path

    @staticmethod
    def init():
        db_path = Users._get_db_path()
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                session_key TEXT NOT NULL
            )
        """
        )
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def check(username, password):
        db_path = Users._get_db_path()
        if not password:
            conn = sqlite3.connect(db_path, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return True
            else:
                return False
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def add(username, password, session_key):
        try:
            db_path = Users._get_db_path()
            conn = sqlite3.connect(db_path, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, session_key) VALUES (?, ?, ?)",
                (username, hashlib.sha256(password.encode()).hexdigest(), session_key),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def user_info(session_key):
        try:
            db_path = Users._get_db_path()
            conn = sqlite3.connect(db_path, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE session_key = ?", (session_key,))
            user = cursor.fetchone()
            conn.close()
            return user
        except Exception as e:
            print(e)
            return False

import sqlite3
from sqlite3 import Error
import hashlib
import os

def create_connection():
    """Crea una conexión a la base de datos SQLite."""
    conn = None
    try:
        conn = sqlite3.connect('bar_app/database/bar_database.db')
        return conn
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Crea las tablas de la base de datos."""
    try:
        c = conn.cursor()
        # Tabla de usuarios
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT NOT NULL
            );
        """)
        # Tabla de productos
        c.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                shortcut TEXT NOT NULL UNIQUE
            );
        """)
        # Tabla de ventas
        c.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                sale_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            );
        """)
        conn.commit()
    except Error as e:
        print(e)

def create_default_users(conn):
    """Crea los usuarios por defecto (admin y cajero) si no existen."""
    try:
        c = conn.cursor()

        # Admin user
        c.execute("SELECT * FROM users WHERE username = 'admin'")
        if not c.fetchone():
            password = 'admin'
            salt = os.urandom(16).hex()
            hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            c.execute("INSERT INTO users (username, password, salt, role) VALUES (?, ?, ?, ?)", ('admin', hashed_password, salt, 'admin'))

        # Cashier user
        c.execute("SELECT * FROM users WHERE username = 'cajero'")
        if not c.fetchone():
            password = 'cajero'
            salt = os.urandom(16).hex()
            hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            c.execute("INSERT INTO users (username, password, salt, role) VALUES (?, ?, ?, ?)", ('cajero', hashed_password, salt, 'cashier'))

        conn.commit()
    except Error as e:
        print(e)

def init_database():
    """Inicializa la base de datos y las tablas."""
    conn = create_connection()
    if conn is not None:
        create_tables(conn)
        create_default_users(conn)
        conn.close()
    else:
        print("Error! No se pudo crear la conexión a la base de datos.")

if __name__ == '__main__':
    init_database()

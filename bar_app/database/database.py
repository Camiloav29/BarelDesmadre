
import sqlite3
from sqlite3 import Error
import hashlib
import os

def create_connection():
    """Crea una conexión a la base de datos SQLite."""
    conn = None
    try:
        conn = sqlite3.connect('bar_app/database/bar_database.db', check_same_thread=False)
        return conn
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Crea las tablas de la base de datos con el nuevo esquema."""
    try:
        c = conn.cursor()

        # --- Tablas de Autenticación y Productos (sin cambios) ---
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT NOT NULL
            );
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                shortcut TEXT NOT NULL UNIQUE
            );
        """)

        # --- Nuevas Tablas para Pedidos y Ventas ---
        # 1. Tabla de Pedidos (uno por transacción)
        c.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_amount REAL NOT NULL,
                order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                order_type TEXT NOT NULL CHECK(order_type IN ('bar', 'billar'))
            );
        """)

        # 2. Tabla de Items del Pedido (múltiples por pedido)
        c.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                price_per_unit REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            );
        """)

        # 3. Tabla para Cuentas Abiertas de Billar
        c.execute("""
            CREATE TABLE IF NOT EXISTS billar_tabs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 4. Tabla de Items de Cuentas de Billar
        c.execute("""
            CREATE TABLE IF NOT EXISTS billar_tab_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tab_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                price_per_unit REAL NOT NULL,
                FOREIGN KEY (tab_id) REFERENCES billar_tabs (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products (id)
            );
        """)

        # Renombrar la tabla 'sales' si existe de una versión anterior
        c.execute("ALTER TABLE IF EXISTS sales RENAME TO old_sales_data;")

        conn.commit()
    except Error as e:
        print(f"Error creating tables: {e}")

def create_default_users(conn):
    """Crea los usuarios por defecto (admin y cajero) si no existen."""
    try:
        c = conn.cursor()
        # Admin
        c.execute("SELECT * FROM users WHERE username = 'admin'")
        if not c.fetchone():
            password = 'admin'
            salt = os.urandom(16).hex()
            hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            c.execute("INSERT INTO users (username, password, salt, role) VALUES (?, ?, ?, ?)", ('admin', hashed_password, salt, 'admin'))
        # Cajero
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

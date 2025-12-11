import sqlite3

def get_products():
    """Obtiene todos los productos de la base de datos."""
    conn = sqlite3.connect('bar_app/database/bar_database.db')
    c = conn.cursor()
    c.execute("SELECT id, name, quantity, price, shortcut FROM products ORDER BY name")
    products = c.fetchall()
    conn.close()
    return products

def add_product(name, quantity, price, shortcut):
    """Añade un nuevo producto a la base de datos."""
    conn = sqlite3.connect('bar_app/database/bar_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO products (name, quantity, price, shortcut) VALUES (?, ?, ?, ?)",
              (name, quantity, price, shortcut))
    conn.commit()
    conn.close()

def update_product(product_id, name, quantity, price, shortcut):
    """Actualiza un producto existente en la base de datos."""
    conn = sqlite3.connect('bar_app/database/bar_database.db')
    c = conn.cursor()
    c.execute("""
        UPDATE products
        SET name = ?, quantity = ?, price = ?, shortcut = ?
        WHERE id = ?
    """, (name, quantity, price, shortcut, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    """Elimina un producto de la base de datos."""
    conn = sqlite3.connect('bar_app/database/bar_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def is_shortcut_unique(shortcut, product_id=None):
    """Verifica si un atajo es único."""
    conn = sqlite3.connect('bar_app/database/bar_database.db')
    c = conn.cursor()
    if product_id:
        c.execute("SELECT id FROM products WHERE shortcut = ? AND id != ?", (shortcut, product_id))
    else:
        c.execute("SELECT id FROM products WHERE shortcut = ?", (shortcut,))
    result = c.fetchone()
    conn.close()
    return result is None

def get_products(db_conn):
    """Obtiene todos los productos de la base de datos."""
    c = db_conn.cursor()
    c.execute("SELECT id, name, quantity, price, shortcut FROM products ORDER BY name")
    products = c.fetchall()
    return products

def add_product(db_conn, name, quantity, price, shortcut):
    """Añade un nuevo producto a la base de datos."""
    c = db_conn.cursor()
    c.execute("INSERT INTO products (name, quantity, price, shortcut) VALUES (?, ?, ?, ?)",
              (name, quantity, price, shortcut))
    db_conn.commit()

def update_product(db_conn, product_id, name, quantity, price, shortcut):
    """Actualiza un producto existente en la base de datos."""
    c = db_conn.cursor()
    c.execute("""
        UPDATE products
        SET name = ?, quantity = ?, price = ?, shortcut = ?
        WHERE id = ?
    """, (name, quantity, price, shortcut, product_id))
    db_conn.commit()

def delete_product(db_conn, product_id):
    """Elimina un producto de la base de datos."""
    c = db_conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db_conn.commit()

def is_shortcut_unique(db_conn, shortcut, product_id=None):
    """Verifica si un atajo es único."""
    c = db_conn.cursor()
    if product_id:
        c.execute("SELECT id FROM products WHERE shortcut = ? AND id != ?", (shortcut, product_id))
    else:
        c.execute("SELECT id FROM products WHERE shortcut = ?", (shortcut,))
    result = c.fetchone()
    return result is None

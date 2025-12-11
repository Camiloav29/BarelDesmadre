import sqlite3

def get_product_by_shortcut(shortcut):
    """Busca un producto por su atajo."""
    conn = sqlite3.connect('bar_app/database/bar_database.db')
    c = conn.cursor()
    c.execute("SELECT id, name, quantity, price FROM products WHERE shortcut = ?", (shortcut,))
    product = c.fetchone()
    conn.close()
    return product

def record_sale(product_id, quantity, total_price):
    """Registra una nueva venta y actualiza el stock del producto."""
    conn = sqlite3.connect('bar_app/database/bar_database.db')
    c = conn.cursor()

    # Insertar la venta
    c.execute("INSERT INTO sales (product_id, quantity, total_price) VALUES (?, ?, ?)",
              (product_id, quantity, total_price))

    # Actualizar el stock
    c.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))

    conn.commit()
    conn.close()

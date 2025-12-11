def get_product_by_shortcut(db_conn, shortcut):
    """Busca un producto por su atajo."""
    c = db_conn.cursor()
    c.execute("SELECT id, name, quantity, price FROM products WHERE shortcut = ?", (shortcut,))
    product = c.fetchone()
    return product

def record_sale(db_conn, product_id, quantity, total_price):
    """Registra una nueva venta y actualiza el stock del producto."""
    c = db_conn.cursor()

    # Insertar la venta
    c.execute("INSERT INTO sales (product_id, quantity, total_price) VALUES (?, ?, ?)",
              (product_id, quantity, total_price))

    # Actualizar el stock
    c.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))

    db_conn.commit()

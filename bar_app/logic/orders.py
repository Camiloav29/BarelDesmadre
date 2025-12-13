def create_order(db_conn, items, order_type):
    """
    Crea un nuevo pedido, registra sus items y actualiza el stock de productos.
    'items' debe ser una lista de tuplas: (product_id, quantity, price_per_unit)
    """
    c = db_conn.cursor()

    # Calcular el total del pedido
    total_amount = sum(item[1] * item[2] for item in items)

    # 1. Crear el registro del pedido
    c.execute("INSERT INTO orders (total_amount, order_type) VALUES (?, ?)", (total_amount, order_type))
    order_id = c.lastrowid

    # 2. Registrar cada item del pedido
    for product_id, quantity, price_per_unit in items:
        c.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price_per_unit)
            VALUES (?, ?, ?, ?)
        """, (order_id, product_id, quantity, price_per_unit))

        # 3. Actualizar el stock del producto
        c.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))

    db_conn.commit()
    return order_id

def get_last_n_orders(db_conn, n=5, order_type='bar'):
    """
    Obtiene los últimos 'n' pedidos de un tipo específico.
    """
    c = db_conn.cursor()
    c.execute("""
        SELECT id, total_amount, order_time
        FROM orders
        WHERE order_type = ?
        ORDER BY order_time DESC
        LIMIT ?
    """, (order_type, n))
    return c.fetchall()

def create_tab(db_conn, customer_name):
    """Crea una nueva cuenta de billar para un cliente."""
    c = db_conn.cursor()
    c.execute("INSERT INTO billar_tabs (customer_name) VALUES (?)", (customer_name,))
    db_conn.commit()
    return c.lastrowid

def get_open_tabs(db_conn):
    """Obtiene todas las cuentas de billar abiertas."""
    c = db_conn.cursor()
    c.execute("SELECT id, customer_name, created_at FROM billar_tabs ORDER BY created_at DESC")
    return c.fetchall()

def add_item_to_tab(db_conn, tab_id, product_id, quantity, price_per_unit):
    """Añade un producto a una cuenta de billar existente."""
    c = db_conn.cursor()
    c.execute("""
        INSERT INTO billar_tab_items (tab_id, product_id, quantity, price_per_unit)
        VALUES (?, ?, ?, ?)
    """, (tab_id, product_id, quantity, price_per_unit))
    db_conn.commit()

def get_tab_items(db_conn, tab_id):
    """Obtiene todos los productos de una cuenta de billar."""
    c = db_conn.cursor()
    c.execute("""
        SELECT p.name, i.quantity, i.price_per_unit, (i.quantity * i.price_per_unit) as total
        FROM billar_tab_items i
        JOIN products p ON i.product_id = p.id
        WHERE i.tab_id = ?
    """, (tab_id,))
    return c.fetchall()

def get_tab_items_for_order(db_conn, tab_id):
    """Obtiene los items en el formato necesario para crear un pedido."""
    c = db_conn.cursor()
    c.execute("SELECT product_id, quantity, price_per_unit FROM billar_tab_items WHERE tab_id = ?", (tab_id,))
    return c.fetchall()

def close_tab(db_conn, tab_id):
    """Elimina una cuenta de billar (después de liquidarla)."""
    c = db_conn.cursor()
    # ON DELETE CASCADE se encargará de los items
    c.execute("DELETE FROM billar_tabs WHERE id = ?", (tab_id,))
    db_conn.commit()

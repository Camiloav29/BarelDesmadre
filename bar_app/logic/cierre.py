import sqlite3
from datetime import date

def get_daily_sales_report(db_conn):
    """
    Obtiene un reporte de ventas para la fecha actual, compatible con el nuevo esquema.
    """
    c = db_conn.cursor()

    today = date.today().strftime('%Y-%m-%d')

    query = """
    SELECT
        p.name,
        SUM(oi.quantity) as total_quantity_sold,
        SUM(oi.quantity * oi.price_per_unit) as total_revenue,
        p.quantity as remaining_stock
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE DATE(o.order_time, 'localtime') = ?
    GROUP BY p.name
    ORDER BY total_revenue DESC
    """

    c.execute(query, (today,))
    report = c.fetchall()
    return report

def get_total_revenue(db_conn):
    """
    Calcula el total de ingresos de todos los pedidos del día actual.
    """
    c = db_conn.cursor()

    today = date.today().strftime('%Y-%m-%d')

    c.execute("SELECT SUM(total_amount) FROM orders WHERE DATE(order_time, 'localtime') = ?", (today,))
    total_revenue = c.fetchone()[0]
    return total_revenue if total_revenue else 0

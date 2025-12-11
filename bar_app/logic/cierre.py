import sqlite3
from datetime import date

def get_daily_sales_report(db_conn):
    """
    Obtiene un reporte de ventas para la fecha actual, agrupando por producto.
    """
    c = db_conn.cursor()

    today = date.today().strftime('%Y-%m-%d')

    query = """
    SELECT
        p.name,
        SUM(s.quantity) as total_quantity_sold,
        SUM(s.total_price) as total_revenue,
        p.quantity as remaining_stock
    FROM sales s
    JOIN products p ON s.product_id = p.id
    WHERE DATE(s.sale_time, 'localtime') = ?
    GROUP BY p.name
    ORDER BY total_revenue DESC
    """

    c.execute(query, (today,))
    report = c.fetchall()
    return report

def get_total_revenue(db_conn):
    """
    Calcula el total de ingresos de todas las ventas del día actual.
    """
    c = db_conn.cursor()

    today = date.today().strftime('%Y-%m-%d')

    c.execute("SELECT SUM(total_price) FROM sales WHERE DATE(sale_time, 'localtime') = ?", (today,))
    total_revenue = c.fetchone()[0]
    return total_revenue if total_revenue else 0

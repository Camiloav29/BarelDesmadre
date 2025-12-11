import sqlite3
import hashlib

def verify_user(username, password):
    """Verifica las credenciales del usuario contra la base de datos."""
    conn = sqlite3.connect('bar_app/database/bar_database.db')
    c = conn.cursor()

    # Hashear la contraseña ingresada para la comparación
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user is not None

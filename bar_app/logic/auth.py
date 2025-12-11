import hashlib

def verify_user(db_conn, username, password):
    """
    Verifica las credenciales del usuario usando salting y devuelve su rol si son correctas.
    """
    c = db_conn.cursor()

    c.execute("SELECT password, salt, role FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    if result:
        stored_password, salt, role = result
        # Combinar la contraseña ingresada con el salt y hashear
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

        if hashed_password == stored_password:
            return role  # Login exitoso
    return None # Usuario no encontrado o contraseña incorrecta

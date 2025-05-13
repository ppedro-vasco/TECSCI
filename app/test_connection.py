# test_connection.py

from db.connection import get_connection

try:
    conn = get_connection()
    print("Conexão com o banco de dados estabelecida com sucesso!")
    conn.close()
except Exception as e:
    print("Falha ao conectar com o banco de dados:", repr(e))

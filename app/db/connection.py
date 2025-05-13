import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="usinas_db",
            user="admin",
            password="admin",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados 2:", repr(e))
        raise

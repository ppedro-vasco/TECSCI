from db.connection import get_connection

class InversorModel:
    @staticmethod
    def criar(id, usina_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO inversor (id, usina_id) VALUES (%s, %s);", (id, usina_id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, usina_id FROM inversor;")
        inversores = cur.fetchall()
        cur.close()
        conn.close()

        return inversores

    @staticmethod
    def buscar_por_id(inversor_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, usina_id FROM inversor WHERE id = %s;", (inversor_id))
        inversor = cur.fetchone()
        cur.close()
        conn.close()

        return inversor

    @staticmethod
    def atualizar(inversor_id, novo_usina_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE inversor SET usina_id = %s WHERE id = %s;", (inversor_id, novo_usina_id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def deletar(inversor_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM inversor WHERE id = %s;", (inversor_id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def listar_por_usina(usina_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM inversor WHERE usina_id = %s", (usina_id,))
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return [row[0] for row in resultados]
    
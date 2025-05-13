from db.connection import get_connection

class UsinaModel:
    @staticmethod
    def criar(nome):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO usina (nome) VALUES (%s) RETURNING id;", (nome,))
        usina_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return usina_id
    
    @staticmethod
    def listar():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM usina;")
        usinas = cur.fetchall()
        cur.close()
        conn.close()

        return usinas
    
    @staticmethod
    def buscar_por_id(usina_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM usina WHERE id = %s;", (usina_id,))
        usina = cur.fetchone()
        cur.close()
        conn.close()

        return usina
    
    @staticmethod
    def atualizar(usina_id, novo_nome):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE usina SET nome = %s WHERE id = %s;", (novo_nome, usina_id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def deletar(usina_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM usina WHERE id = %s;", (usina_id))
        conn.commit()
        cur.close()
        conn.close()
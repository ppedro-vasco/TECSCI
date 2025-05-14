from db.connection import get_connection
from datetime import datetime

class MedicaoModel:
    @staticmethod
    def inserir(inversor_id, data_hora, potencia, temperatura):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO medicao (inversor_id, data_hora, potencia_ativa_watt, temperatura_celsius)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (inversor_id, data_hora) DO NOTHING;
        """, (inversor_id, data_hora, potencia, temperatura))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def listar_potencias_por_inversor(inversor_id: int, data_inicio: datetime, data_fim: datetime):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT data_hora, potencia_ativa_watt
            FROM medicao
            WHERE inversor_id = %s
                AND data_hora BETWEEN %s AND %s
                AND potencia_ativa_watt IS NOT NULL
            ORDER BY data_hora;
        """, (inversor_id, data_inicio, data_fim))

        resultados = cur.fetchall()
        cur.close()
        conn.close()

        return resultados # lista de tuplas

    @staticmethod
    def listar_temperaturas_por_inversor(inversor_id: int, data_inicio: datetime, data_fim: datetime):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT data_hora, temperatura_celsius
            FROM medicao
            WHERE inversor_id = %s
                AND data_hora BETWEEN %s AND %s
                AND temperatura_celsius IS NOT NULL
            ORDER BY data_hora;
        """, (inversor_id, data_inicio, data_fim))

        resultados = cur.fetchall()
        cur.close()
        conn.close()

        return resultados # lista de tuplas

    def buscar_por_inversor_e_periodo(inversor_id: int, data_inicio: datetime, data_fim: datetime):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT data_hora, potencia_ativa_watt
            FROM medicao
            WHERE inversor_id = %s AND data_hora BETWEEN %s AND %s
            ORDER BY data_hora;
        """, (inversor_id, data_inicio, data_fim))

        resultados = cur.fetchall()
        cur.close()
        conn.close()

        return resultados # tupla
    

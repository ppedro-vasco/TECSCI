from service.insights_service import gerar_por_inversor
from service.insights_service import gerar_por_usina

def handle_geracao_inversor(handler, query_params):
    try:
        inversor_id = int(query_params.get("inversor_id", [None])[0])
        data_inicio = query_params.get("data_inicio", [None])[0]
        data_fim = query_params.get("data_fim", [None])[0]

        if not all([inversor_id, data_inicio, data_fim]):
            handler._send_response({
                "erro": "Parâmetros obrigatórios: inversor_id, data_inicio, data_fim"
            }, status=400)
            return

        resultado = gerar_por_inversor(inversor_id, data_inicio, data_fim)
        handler._send_response({"geracao_wh": resultado})

    except Exception as e:
        handler._send_response({"erro": str(e)}, status=400)

def handle_geracao_usina(handler, query_params):
    try:
        usina_id = int(query_params.get("usina_id", [None])[0])
        data_inicio = query_params.get("data_inicio", [None])[0]
        data_fim = query_params.get("data_fim", [None])[0]

        if not all([usina_id, data_inicio, data_fim]):
            handler._send_response({
                "erro": "Parâmetros obrigatórios: usina_id, data_inicio, data_fim"
            }, status=400)
            return

        resultado = gerar_por_usina(usina_id, data_inicio, data_fim)
        handler._send_response({"geracao_wh": resultado})

    except Exception as e:
        handler._send_response({"erro": str(e)}, status=400)
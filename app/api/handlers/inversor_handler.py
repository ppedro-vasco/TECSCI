import json
from model.inversor_model import InversorModel

def handle_inversores(handler):
    method = handler.command

    if method == "GET":
        inversores = InversorModel.listar()
        lista = [{"id": i[0], "usina_id": i[1]} for i in inversores]
        handler._send_response(lista)

    elif method == "POST":
        content_length = int(handler.headers.get("Content-Length", 0))
        body = handler.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(body)
            inversor_id = data.get("id")
            usina_id = data.get("usina_id")
            if not inversor_id or not usina_id:
                raise ValueError("Campos 'id' e 'usina_id' são obrigatórios")
            InversorModel.criar(inversor_id, usina_id)
            handler._send_response({"id": inversor_id, "usina_id": usina_id}, status=201)
        except Exception as e:
            handler._send_response({"erro": str(e)}, status=400)

    elif method == "PUT":
        content_length = int(handler.headers.get("Content-Length", 0))
        body = handler.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(body)
            inversor_id = data.get("id")
            nova_usina_id = data.get("usina_id")
            if not inversor_id or not nova_usina_id:
                raise ValueError("Campos 'id' e 'usina_id' são obrigatórios")
            InversorModel.atualizar(inversor_id, nova_usina_id)
            handler._send_response({"mensagem": "Inversor atualizado com sucesso"})
        except Exception as e:
            handler._send_response({"erro": str(e)}, status=400)

    elif method == "DELETE":
        content_length = int(handler.headers.get("Content-Length", 0))
        body = handler.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(body)
            inversor_id = data.get("id")
            if not inversor_id:
                raise ValueError("Campo 'id' é obrigatório")
            InversorModel.deletar(inversor_id)
            handler._send_response({"mensagem": "Inversor removido com sucesso"})
        except Exception as e:
            handler._send_response({"erro": str(e)}, status=400)

    else:
        handler._send_response({"erro": "Método não suportado"}, status=405)

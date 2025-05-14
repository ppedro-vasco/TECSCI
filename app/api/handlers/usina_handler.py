import json
from model.usina_model import UsinaModel

def handle_usinas(handler):
    method = handler.command

    if method == "GET":
        usinas = UsinaModel.listar()
        lista = [{"id": u[0], "nome": u[1]} for u in usinas]
        handler._send_response(lista)

    elif method == "POST":
        content_length = int(handler.headers.get("Content-Length", 0))
        body = handler.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(body)
            nome = data.get("nome")
            if not nome:
                raise ValueError("Campo 'nome' é obrigatório")
            usina_id = UsinaModel.criar(nome)
            handler._send_response({"id": usina_id, "nome": nome}, status=201)
        except Exception as e:
            handler._send_response({"erro": str(e)}, status=400)

    elif method == "PUT":
        content_length = int(handler.headers.get("Content-Length", 0))
        body = handler.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(body)
            usina_id = data.get("id")
            novo_nome = data.get("nome")
            if not usina_id or not novo_nome:
                raise ValueError("Campos 'id' e 'nome' são obrigatórios")
            UsinaModel.atualizar(usina_id, novo_nome)
            handler._send_response({"mensagem": "Usina atualizada com sucesso"})
        except Exception as e:
            handler._send_response({"erro": str(e)}, status=400)

    elif method == "DELETE":
        content_length = int(handler.headers.get("Content-Length", 0))
        body = handler.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(body)
            usina_id = data.get("id")
            if not usina_id:
                raise ValueError("Campo 'id' é obrigatório")
            UsinaModel.deletar(usina_id)
            handler._send_response({"mensagem": "Usina removida com sucesso"})
        except Exception as e:
            handler._send_response({"erro": str(e)}, status=400)

    else:
        handler._send_response({"erro": "Método não suportado"}, status=405)

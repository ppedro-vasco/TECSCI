from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

from api.handlers.insights_handler import (
    handle_geracao_inversor,
    handle_geracao_usina,
)

class SimpleRouter(BaseHTTPRequestHandler):
    def _send_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if path == "/geracao/inversor":
            handle_geracao_inversor(self, query_params)

        elif path == "/geracao/usina":
            handle_geracao_usina(self, query_params)

        else:
            self._send_response({"erro": "Rota não encontrada"}, status=404)
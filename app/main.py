from http.server import HTTPServer
from api.router import SimpleRouter

def run():
    host = "localhost"
    port = 8080
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleRouter)
    print(f"Servidor iniciado em http://{host}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
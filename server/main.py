import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import database

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.file_name = 'index.html'
        elif self.path == '/data':
            data = database.fetch_survey_data()  
            if data is not None:
                json_data = json.dumps(data)  
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json_data.encode())  
                return
        else:
            self.file_name = self.path.lstrip('/')

        file_path = os.path.join(os.path.dirname(__file__), 'public', self.file_name)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            if file_path.endswith('.html'):
                self.send_header('Content-type', 'text/html')
            elif file_path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif file_path.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            self.end_headers()

            with open(file_path, 'rb') as file:
                content = file.read()
                self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, POST request!')

    def do_PUT(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, PUT request!')

    def do_DELETE(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, DELETE request!')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=6161):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server started on http://localhost:{port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
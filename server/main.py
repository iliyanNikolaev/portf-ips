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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode('utf-8'))
            if 'name' not in data or 'age' not in data or 'info' not in data:
                raise ValueError('missing data in body')
            if not data['name'] or not data['age'] or not data['info']:
                raise ValueError('all fields are required')
        
        except ValueError as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e).encode()) 
            return 
    
        name = data.get('name', '')
        age = data.get('age', '')
        info = data.get('info', '')

        is_ok = database.post_survey_data(name, age, info)
        
        if is_ok:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'ok')
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'internal server err')

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
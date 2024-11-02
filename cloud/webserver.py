from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Remove the leading '/' from the path
        path = self.path.lstrip('/')

        # Handle the root URL
        if path == '' or path == '/':
            path = 'index.html'  # Default to index.html if no path is specified

        # Construct the full path to the file
        full_path = os.path.join(os.getcwd(), path)

        # Check if the file exists
        if not os.path.exists(full_path):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"File not found")
            return

        # Check if the path is a file
        if not os.path.isfile(full_path):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"File not found")
            return

        # Determine the content type based on the file extension
        content_type = self.get_content_type(full_path)

        # Open the file in binary mode and read its content
        with open(full_path, 'rb') as file:
            content = file.read()

        # Send the response
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def get_content_type(self, path):
        # Determine the content type based on the file extension
        if path.endswith('.html'):
            return 'text/html'
        elif path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.js'):
            return 'text/javascript'
        elif path.endswith('.json'):
            return 'application/json'
        else:
            return 'application/octet-stream'

if __name__ == "__main__":
    server_address = ("localhost", 8080)
    server = HTTPServer(server_address, MyHttpRequestHandler)
    print("Server started on http://localhost:8080")
    server.serve_forever()

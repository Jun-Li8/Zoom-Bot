from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from get_window import bot
from email_setup import sent_email

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b'You may now exit this page.')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        data = json.loads(post_data)
        if data["event"] == "recording.started":
            bot('start')
        
        if data["event"] == "recording.stopped":
            bot('ended')
            sent_email()

def start_server(port):
    httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    httpd.serve_forever()

# if __name__ == "__main__":
#     start_server(8080)
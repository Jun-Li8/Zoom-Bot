from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import requests
import threading


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
            print('+Convoz is online')
            # print('cool')
            # date = data["payload"]["object"]["start_time"].split("T")[0]
            # file_name = "{date}_audio_transcript.vtt".format(date=date)
            # for recording_file in data["payload"]["object"]["recording_files"]:
            #     if recording_file["file_type"] == "TRANSCRIPT":

            #         headers = {
            #             'authorization': "Bearer {download_token}".format(download_token=data["download_token"]),
            #             'content-type': "application/json"
            #         }
                    
            #         transcript = requests.get(recording_file["download_url"], allow_redirects=True, headers=headers)
            #         open(file_name, 'wb').write(transcript.content)
            #         print('done')
            

def start_server(port):
    httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    start_server(8080)
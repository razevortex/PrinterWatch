# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer, CGIHTTPRequestHandler
from HTML.html_builder import *
import time
import os

hostName = "localhost"
serverPort = 8080


builder = HTMLCreator()

def statistics_info(readme, grouped=False):
    if grouped is not True:
        string = '<p>Spreadsheet statistics variables info: </p>'
    else:
        string = '<p>Spreadsheet model statistics variables calculation info: </p>'
    with open(fr'A:\Raze VorteX\Documents\PrinterWatch\PrinterWatch\excel_sheets\{readme}.txt', 'r') as help:
        text = help.readlines()
        for line in text:
            if line != '':
                string += f'<p>{line}</p>'
    return string

sheet_path = r'https://docs.google.com/spreadsheets/d/1lSXBP5OPtdYT9VPXkcwKnn5nrwIv1dCh/edit?usp=sharing&ouid=102357389013742688623&rtpof=true&sd=true'
readme_path = r'https://drive.google.com/file/d/1lJPZrVBe_DfBqAISg0PQXrUicKZJ27Xn/view?usp=sharing'
model_sheet_path = r'https://docs.google.com/spreadsheets/d/1lfzx2177TMdF3bBibrutn-0OE_zXu6K_/edit?usp=sharing&ouid=102357389013742688623&rtpof=true&sd=true'

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        for line in builder.basecode:
            self.wfile.write(bytes(line, "utf-8"))
        '''        self.wfile.write(bytes("<html><head><title>PrinterWatch</title></head>", "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes(
                    f"<iframe src='{sheet_path}' width='100%' "
                    "height='800px' frameborder='0'> </iframe>", "utf-8"))
                self.wfile.write(bytes(f"{statistics_info('ReadMe')}", "utf-8"))
                self.wfile.write(bytes(
                    f"<iframe src='{model_sheet_path}' width='100%' "
                    "height='800px' frameborder='0'> </iframe>", "utf-8"))
                self.wfile.write(bytes(f"{statistics_info('ReadMeGrouped', grouped=True)}", "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))'''

refresh_timer = time.time()



def run_webserver():
    os.chdir('../HTML')

    webServer = HTTPServer(('', 80), MyServer)
    print("Server started http://172.20.12.179/")
    try:


            webServer.serve_forever(900)

    except KeyboardInterrupt:
        pass


    print("Server stopped.")

if __name__ == "__main__":
    while True:
        run_webserver()

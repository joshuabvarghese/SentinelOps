import http.server
import socketserver
import os

PORT = 8080
# Set directory to where your dashboard.html and results.json are
DIRECTORY = "." 

class MonitoringHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Prevents the browser from blocking the data request
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        # Default to showing the dashboard
        if self.path == '/':
            self.path = '/dashboard.html'
        return super().do_GET()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), MonitoringHandler) as httpd:
        print(f"🚀 Dashboard: http://localhost:{PORT}")
        httpd.serve_forever()
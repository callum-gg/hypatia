# Python 3.x
import http.server
import socketserver

# Set the port number you want to use
port = 8000

# Specify the handler to use (in this case, SimpleHTTPRequestHandler)
handler = http.server.SimpleHTTPRequestHandler

# Create the server
with socketserver.TCPServer(("", port), handler) as httpd:
    print(f"Serving on port {port}")
    
    # Start the server
    httpd.serve_forever()
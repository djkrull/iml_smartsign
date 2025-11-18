#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP server for serving SmartSign template and data
Serves HTML template with dynamic CSV loading
Optimized for Railway deployment
"""

import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class SmartSignRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for SmartSign template and data"""

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        path = self.path

        # Log the request
        print(f"[REQUEST] {path}")

        # Root path (/) serves template_simple.html
        if path == '/' or path == '/index.html':
            self.serve_file('template_simple.html', 'text/html; charset=utf-8')
            return

        # /seminarier.csv serves the CSV data file
        if path == '/seminarier.csv':
            self.serve_file('seminarier.csv', 'text/csv; charset=utf-8')
            return

        # Serve static assets (PNG)
        if path.endswith('.png'):
            filename = path.lstrip('/')
            self.serve_file(filename, 'image/png')
            return

        # Serve static assets (JPG/JPEG)
        if path.endswith(('.jpg', '.jpeg')):
            filename = path.lstrip('/')
            self.serve_file(filename, 'image/jpeg')
            return

        # Health check endpoint
        if path == '/health':
            self.send_response(200)
            self.add_cors_headers()
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'OK')
            return

        # Default: 404
        self.send_response(404)
        self.add_cors_headers()
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'404 - File not found')

    def serve_file(self, filename, content_type):
        """Serve a file with proper headers"""
        try:
            with open(filename, 'rb') as f:
                content = f.read()

            self.send_response(200)
            self.add_cors_headers()
            self.add_cache_headers(filename)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            print(f"[OK] Served {filename}")

        except FileNotFoundError:
            self.send_response(404)
            self.add_cors_headers()
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"404 - File not found: {filename}".encode())
            print(f"[NOT FOUND] {filename}")
        except Exception as e:
            self.send_response(500)
            self.add_cors_headers()
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"500 - Server error: {str(e)}".encode())
            print(f"[ERROR] {filename}: {str(e)}")

    def add_cors_headers(self):
        """Add CORS headers to response"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def add_cache_headers(self, filename):
        """Add cache headers based on file type"""
        if filename.endswith('.csv'):
            # CSV: short cache (5 minutes) - data changes daily
            self.send_header('Cache-Control', 'public, max-age=300')
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            # Images: longer cache (24 hours) - assets don't change often
            self.send_header('Cache-Control', 'public, max-age=86400')
        elif filename.endswith('.html'):
            # HTML: short cache (5 minutes) - template may be updated
            self.send_header('Cache-Control', 'public, max-age=300')
        else:
            # Default: 5 minutes
            self.send_header('Cache-Control', 'public, max-age=300')

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def run_server(port=8080):
    """Start the HTTP server"""
    handler = SmartSignRequestHandler
    server = HTTPServer(('0.0.0.0', port), handler)

    print("=" * 80)
    print("SMARTSIGN TEMPLATE & DATA SERVER")
    print("=" * 80)
    print(f"Server running on port {port}")
    print(f"Access template at: http://localhost:{port}/")
    print(f"Access CSV data at: http://localhost:{port}/seminarier.csv")
    print(f"Health check at: http://localhost:{port}/health")
    print("Press Ctrl+C to stop")
    print("=" * 80)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        server.shutdown()

if __name__ == "__main__":
    # Get port from environment (Railway sets this) or use 8080
    port = int(os.environ.get('PORT', 8080))
    run_server(port)

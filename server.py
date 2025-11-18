#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP server for serving SmartSign template and data
Serves HTML template with dynamic CSV loading
Optimized for Railway deployment
"""

import os
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial

class SmartSignRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for SmartSign template and data"""

    def end_headers(self):
        """Add CORS and cache headers to all responses"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

        # Set cache headers based on content type
        if self.path.endswith('.csv'):
            # CSV: short cache (5 minutes) - data changes daily
            self.send_header('Cache-Control', 'public, max-age=300')
        elif self.path.endswith(('.png', '.jpg', '.jpeg')):
            # Images: longer cache (24 hours) - assets don't change often
            self.send_header('Cache-Control', 'public, max-age=86400')
        elif self.path.endswith('.html'):
            # HTML: short cache (5 minutes) - template may be updated
            self.send_header('Cache-Control', 'public, max-age=300')
        else:
            # Default: 5 minutes
            self.send_header('Cache-Control', 'public, max-age=300')

        super().end_headers()

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        path = self.path

        # Root path (/) serves template_simple.html
        if path == '/' or path == '/index.html':
            return self.serve_file('template_simple.html', 'text/html; charset=utf-8')

        # /seminarier.csv serves the CSV data file
        elif path == '/seminarier.csv':
            return self.serve_file('seminarier.csv', 'text/csv; charset=utf-8')

        # Serve static assets
        elif path.endswith('.png'):
            return self.serve_file(path.lstrip('/'), 'image/png')

        elif path.endswith('.jpg') or path.endswith('.jpeg'):
            return self.serve_file(path.lstrip('/'), 'image/jpeg')

        # Health check endpoint for Railway
        elif path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'OK')
            return

        # Default: 404
        else:
            self.send_error(404, "File not found")

    def serve_file(self, filename, content_type):
        """Serve a file with proper headers"""
        try:
            with open(filename, 'rb') as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, f"File not found: {filename}")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

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

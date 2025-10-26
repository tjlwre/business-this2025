#!/usr/bin/env python3
import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler
import os

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Cache-Control', 'public, max-age=3600')
        self.send_header('Content-Security-Policy', "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://fonts.googleapis.com https://fonts.gstatic.com https://cdnjs.cloudflare.com https://va.vercel-scripts.com; img-src 'self' data: https:;")
        super().end_headers()

    def do_GET(self):
        # Serve landing_page.html as index
        if self.path == '/' or self.path == '/index.html':
            self.path = '/landing_page.html'
        return super().do_GET()

if __name__ == "__main__":
    PORT = 8000
    Handler = CustomHTTPRequestHandler
    
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"🚀 BusinessThis Landing Page Server")
        print(f"📍 Server running at: http://127.0.0.1:{PORT}")
        print(f"🌐 Landing page: http://127.0.0.1:{PORT}/")
        print(f"📱 App preview: http://127.0.0.1:{PORT}/app_preview.html")
        print(f"⏹️  Press Ctrl+C to stop")
        print("=" * 50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
            httpd.shutdown()

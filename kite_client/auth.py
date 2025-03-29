import http.server
import socketserver
import webbrowser
import urllib.parse
import requests
import hashlib
import os
import json

from cryptography.fernet import Fernet
from . import config

KEY_FILE = "kite_secret.key"

# -----------------------------------------------------------------------------
# Encryption Helpers
# -----------------------------------------------------------------------------
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_token(token: str) -> bytes:
    fernet = Fernet(load_key())
    return fernet.encrypt(token.encode())

def decrypt_token(data: bytes) -> str:
    fernet = Fernet(load_key())
    return fernet.decrypt(data).decode()

# -----------------------------------------------------------------------------
# Token File Helpers
# -----------------------------------------------------------------------------
def save_token(token: str):
    encrypted = encrypt_token(token)
    with open(config.TOKEN_FILE, "wb") as f:
        f.write(encrypted)

def load_token():
    if os.path.exists(config.TOKEN_FILE):
        with open(config.TOKEN_FILE, "rb") as f:
            encrypted = f.read()
            return decrypt_token(encrypted)
    return None

# -----------------------------------------------------------------------------
# Local HTTP server to capture request_token
# -----------------------------------------------------------------------------
class TokenHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # ✅ Block weird paths like /livereload, /favicon.ico etc.
        if parsed.path != "/":
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid path.")
            return

        params = urllib.parse.parse_qs(parsed.query)

        if "request_token" in params:
            self.server.request_token = params["request_token"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Login successful!</h1><p>You can close this window now.</p>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing request_token.")


class TokenServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.request_token = None

def open_browser_and_capture_token():
    login_url = f"https://kite.zerodha.com/connect/login?v=3&api_key={config.API_KEY}"
    print("🔓 Opening login page in browser...")
    webbrowser.open(login_url)

    with TokenServer(("", config.PORT), TokenHandler) as httpd:
        httpd.handle_request()

        if not httpd.request_token:
            raise RuntimeError("❌ Failed to capture request_token from redirect.")
        return httpd.request_token

# -----------------------------------------------------------------------------
# Exchange request_token for access_token
# -----------------------------------------------------------------------------
def generate_checksum(api_key, token, secret):
    return hashlib.sha256((api_key + token + secret).encode()).hexdigest()

def get_access_token(request_token):
    checksum = generate_checksum(config.API_KEY, request_token, config.API_SECRET)
    payload = {
        "api_key": config.API_KEY,
        "request_token": request_token,
        "checksum": checksum
    }
    headers = {
        "X-Kite-Version": "3",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://api.kite.trade/session/token", data=payload, headers=headers)
    response.raise_for_status()
    return response.json()["data"]["access_token"]

# -----------------------------------------------------------------------------
# Main entry: load or generate token
# -----------------------------------------------------------------------------
def authenticate(force_refresh=False):
    if not force_refresh:
        token = load_token()
        if token:
            return token

    print("🔑 Starting login flow...")
    request_token = open_browser_and_capture_token()
    token = get_access_token(request_token)
    save_token(token)
    return token

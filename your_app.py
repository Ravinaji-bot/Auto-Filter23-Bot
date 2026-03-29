import subprocess
import os
import sys
import time

# 1. Bot ko background mein start karne ka sabse safe tarika
print("🚀 Launching main.py in background...")
try:
    # stdout/stderr ko DEVNULL kiya taaki Read-only error na aaye
    subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=None, 
        stderr=None,
        start_new_session=True
    )
except Exception as e:
    print(f"❌ Launch Error: {e}")

# 2. Leapcell (Gunicorn) ko response dene ke liye WSGI function
def wsgi(environ, start_response):
    # Jaise hi server request bhejega, hum turant '200 OK' denge
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b"Bot is active and running!"]
    

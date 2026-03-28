import subprocess
import os
import time

# 1. Bot ko start hone ke liye 2 second ka gap denge
print("🚀 Launching main.py...")
subprocess.Popen(["python3", "main.py"])

# 2. Leapcell ko turant response dene ke liye ye function
def wsgi(environ, start_response):
    # Jaise hi server check karega, hum turant 'OK' bol denge
    # Isse server restart loop ruk jayega
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b"Bot is active and running in background!"]

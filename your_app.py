import subprocess
import os

# Bot ko background mein start karega
try:
    print("🚀 Starting Telegram Bot (main.py)...")
    subprocess.Popen(["python3", "main.py"])
except Exception as e:
    print(f"Error launching bot: {e}")

# Leapcell isi function ko dhund raha hai
def wsgi(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b"Bot is active and running!"]
    

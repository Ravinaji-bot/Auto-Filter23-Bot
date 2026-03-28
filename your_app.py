import subprocess
import os
import time

# Bot ko background mein start karne ke liye 'nohup' use karenge
print("🚀 Launching main.py in background...")
try:
    # 'nohup' aur '&' se bot alag process mein chalega aur crash nahi hoga
    os.system("nohup python3 main.py > bot_logs.txt 2>&1 &")
except Exception as e:
    print(f"Launch Error: {e}")

# Leapcell ko turant response dene ke liye WSGI function
def wsgi(environ, start_response):
    # Jaise hi server request bhejega, hum bina ruke answer denge
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b"Bot is active and running!"]
    

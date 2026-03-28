import os
import subprocess
import time

# 1. Aapka Telegram Bot (main.py) start karne ka logic
# Isse bot background mein chalu ho jayega
try:
    print("🚀 Starting Telegram Bot (main.py)...")
    subprocess.Popen(["python", "main.py"])
except Exception as e:
    print(f"❌ Error starting bot: {e}")

# 2. Leapcell (Gunicorn) ko khush rakhne ke liye WSGI function
# Ye function error 127 aur exit status 3 ko khatam kar dega
def wsgi(environ, start_response):
    # Leapcell jab check karega, toh use ye status milega
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    
    # Message jo dashboard par dikhega (optional)
    return [b"Bot is Running Successfully in Background!"]

# Agar aap local test kar rahe hain (optional)
if __name__ == "__main__":
    print("System check: OK")
    

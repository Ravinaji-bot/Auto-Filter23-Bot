import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters, idle
from thefuzz import process

# --- Bot Config ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client(
    "filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    workdir="/tmp",
    sleep_threshold=30 # Bot ko jaldi connect karne ke liye
)

# --- Sample Movie Data ---
MOVIES = {"Pushpa 2": "https://t.me/example/1", "Stree 2": "https://t.me/example/2"}

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("✅ Bot Online Hai Sir! Main ready hoon.")

@app.on_message(filters.text & filters.private)
async def search(client, message):
    query = message.text
    choices = list(MOVIES.keys())
    result, score = process.extractOne(query, choices)
    if score > 60:
        await message.reply_text(f"🔍 Result: {result}\n🔗 {MOVIES[result]}")
    else:
        await message.reply_text("❌ Movie nahi mili.")

# --- Universal Health Check Server ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Leapcell ke health check ko turant handle karega
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is Running!")
    def log_message(self, format, *args):
        return # Logs ko clean rakhne ke liye

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    server.serve_forever()

# --- Run ---
async def start_everything():
    # Web server ko turant start karenge taaki Leapcell restart na kare
    threading.Thread(target=run_server, daemon=True).start()
    
    print("🛰 Connecting to Telegram...")
    try:
        await app.start()
        print("✅ SUCCESS: BOT IS ONLINE!")
        await idle()
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    finally:
        if app.is_connected:
            await app.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_everything())
    

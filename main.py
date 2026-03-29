import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters, idle

# --- Configuration ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-100")) 

app = Client(
    "rescue_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    workdir="/tmp"
)

movie_db = {}

# Channel indexing function
async def index_movies():
    print("📂 Scanning Channel...")
    try:
        async for message in app.get_chat_history(CHANNEL_ID, limit=300):
            if message.document or message.video:
                name = message.caption or (message.document.file_name if message.document else "Unknown")
                movie_db[name.lower()] = message.id
        print(f"✅ SUCCESS: {len(movie_db)} movies found!")
    except Exception as e:
        print(f"❌ Indexing Error: {e}")

@app.on_message(filters.text & filters.private)
async def handle_search(client, message):
    query = message.text.lower()
    if query == "/start":
        await message.reply_text("👋 Namaste! Movie ka naam likhiye.")
        return

    for name, msg_id in movie_db.items():
        if query in name:
            await client.copy_message(message.chat.id, CHANNEL_ID, msg_id)
            return
    await message.reply_text("❌ Nahi mili sir.")

# --- Leapcell Web Server ---
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_web_server():
    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    server.serve_forever()

async def main():
    # Pehle web server start karein taaki Leapcell 'Healthy' dikhaye
    threading.Thread(target=run_web_server, daemon=True).start()
    
    print("🛰 Connecting Pyrogram...")
    try:
        await app.start()
        await index_movies()
        print("🚀 BOT IS LIVE!")
        await idle()
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    

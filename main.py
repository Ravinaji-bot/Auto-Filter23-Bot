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
    "auto_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    workdir="/tmp"
)

movie_db = {}

async def index_movies():
    print("📂 Indexing movies...")
    try:
        async for message in app.get_chat_history(CHANNEL_ID, limit=500):
            if message.document or message.video:
                file_name = message.caption or (message.document.file_name if message.document else "Unknown")
                movie_db[file_name.lower()] = message.id
        print(f"✅ Indexed {len(movie_db)} movies!")
    except Exception as e:
        print(f"❌ Indexing Error: {e}")

@app.on_message(filters.text & filters.private)
async def search_movie(client, message):
    query = message.text.lower()
    for name, msg_id in movie_db.items():
        if query in name:
            await client.copy_message(message.chat.id, CHANNEL_ID, msg_id)
            return
    await message.reply_text("❌ Movie nahi mili sir.")

# --- Leapcell Friendly Server ---
class UniversalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Auto Filter Active")
    def do_POST(self): # POST ko bhi handle karega taaki error na aaye
        self.send_response(200)
        self.end_headers()

def run_server():
    HTTPServer(('0.0.0.0', 8080), UniversalHandler).serve_forever()

async def start_bot():
    threading.Thread(target=run_server, daemon=True).start()
    await app.start()
    await index_movies()
    print("🚀 BOT IS READY!")
    await idle()

if __name__ == "__main__":
    asyncio.run(start_bot())
        

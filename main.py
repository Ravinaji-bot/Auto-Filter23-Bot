import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters, idle

# --- Configuration ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
# Apni Private Channel ka ID yahan daalein (Example: -100123456789)
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-100")) 

app = Client(
    "auto_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    workdir="/tmp"
)

# Database to store movie info
movie_db = {}

# 1. Automatic Indexing: Channel ki purani aur nayi posts read karega
async def index_movies():
    print("📂 Indexing movies from channel...")
    async for message in app.get_chat_history(CHANNEL_ID):
        if message.document or message.video:
            # File ka naam ya caption uthayega
            file_name = message.caption or (message.document.file_name if message.document else "Unknown")
            movie_db[file_name.lower()] = message.id
    print(f"✅ Indexed {len(movie_db)} movies!")

# 2. Search Handler: Group ya Private mein jab koi naam likhe
@app.on_message(filters.text & ~filters.service)
async def search_movie(client, message):
    query = message.text.lower()
    
    # Matching logic
    for name, msg_id in movie_db.items():
        if query in name:
            # Movie file ko channel se forward karega
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=msg_id,
                caption=f"🎬 **Found:** {name}\n\nJoin: @GajabFactsGujarati"
            )
            return
    
    if message.chat.type == "private":
        await message.reply_text("❌ Sorry, ye movie mere database mein nahi hai.")

# --- Fake Server for Leapcell ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Auto Filter is Running!")

def run_server():
    HTTPServer(('0.0.0.0', 8080), SimpleHandler).serve_forever()

async def start_bot():
    threading.Thread(target=run_server, daemon=True).start()
    await app.start()
    await index_movies() # Bot start hote hi channel read karega
    print("🚀 AUTO-FILTER BOT IS LIVE!")
    await idle()

if __name__ == "__main__":
    asyncio.run(start_bot())
                

import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters, idle
import pyrogram

# --- Configuration ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-100123456789")) # Apna sahi ID dalein

app = Client(
    "auto_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    workdir="/tmp",
    sleep_threshold=30 # Connection issues prevent karega
)

movie_db = {}

# 1. Faster & Limited Indexing
async def index_movies():
    print("📂 Fast Indexing movies... Please wait!")
    movie_db.clear() # database clear karein
    count = 0
    try:
        # Fast approach ke liye limit lagate hain aur service messages avoid karte hain
        async for message in app.get_chat_history(CHANNEL_ID, limit=500): 
            if message.document or message.video:
                file_name = message.caption or (message.document.file_name if message.document else "Unknown_Movie")
                movie_db[file_name.lower()] = message.id
                count += 1
        print(f"✅ Indexed {count} movies! Bot is now ready.")
    except Exception as e:
        print(f"❌ Indexing Error (Check CHANNEL_ID & Admin rights): {e}")

# 2. Optimized Search Handler
@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def search_movie(client, message):
    if not movie_db:
        # Agar db khali ho toh try karein fir se index karne ka
        await index_movies()

    query = message.text.lower()
    found_count = 0
    
    # Matching logic
    for name, msg_id in movie_db.items():
        if query in name:
            try:
                # File ko channel se forward karega
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=CHANNEL_ID,
                    message_id=msg_id
                )
                found_count += 1
                # Ek match milte hi ruk jayega, agar saari files chahiye toh 'return' hata dein
                return 
            except Exception as e:
                print(f"❌ Forward Error: {e}")
                
    if found_count == 0:
        await message.reply_text("❌ Sorry, ye movie nahi mili. Naam check karein.")

# Command handlers
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text("🙏 **Namaste! Gajab Facts Bot Live Hai!**\nMovie search kijiye.")

# --- Fake Server for Leapcell with HEAD Support ---
class UniversalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Auto Filter Running")
    def do_HEAD(self): # <--- Ye add kiya hai error hatane ke liye
        self.send_response(200)
        self.end_headers()
    def do_POST(self): # Uptime robot support
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        return # Logs clean rahengi

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), UniversalHandler)
    server.serve_forever()

# --- Run Bot with Indexed Data Check ---
async def start_bot():
    threading.Thread(target=run_server, daemon=True).start()
    print("🛰 Starting Bot Client...")
    try:
        await app.start()
        # Bot connect hote hi channel scan karega
        await index_movies()
        print("🚀 BOT IS LIVE AND READY FOR SEARCH!")
        await idle()
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    finally:
        if app.is_connected:
            await app.stop()

if __name__ == "__main__":
    asyncio.run(start_bot())
        

import os
import asyncio
from pyrogram import Client, filters, idle
from thefuzz import process
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- 1. Bot Configuration ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# RAM use karne ke liye in_memory=True
app = Client(
    "filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    workdir="/tmp"
)

# --- 2. Movie Database ---
MOVIES = {
    "Pushpa 2": "https://t.me/example/1",
    "Maharaja": "https://t.me/example/4",
    "Stree 2": "https://t.me/example/5"
}

# --- 3. Handlers ---
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text("**Namaste! Bot Live Hai Sir! 🙏**")

@app.on_message(filters.text & filters.private)
async def search_handler(client, message):
    query = message.text
    choices = list(MOVIES.keys())
    result, score = process.extractOne(query, choices)
    if score > 60:
        await message.reply_text(f"🔍 **Result:** {result}\n🔗 [Download]({MOVIES[result]})")
    else:
        await message.reply_text("❌ Nahi mili sir.")

# --- 4. Fake Server (Leapcell ko khush rakhne ke liye) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    print("🌐 Web Server Started on Port 8080")
    server.serve_forever()

# --- 5. Main Execution ---
async def start_everything():
    # Server ko background mein chalayenge
    threading.Thread(target=run_server, daemon=True).start()
    
    # Bot start karenge
    print("🛰 Starting Pyrogram...")
    await app.start()
    print("✅ Bot is Online!")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_everything())

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
    workdir="/tmp"
)

# --- Sample Movie Data ---
MOVIES = {"Pushpa 2": "https://t.me/example/1", "Stree 2": "https://t.me/example/2"}

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("✅ Bot Online Hai Sir! Kaise madad karun?")

@app.on_message(filters.text & filters.private)
async def search(client, message):
    query = message.text
    choices = list(MOVIES.keys())
    result, score = process.extractOne(query, choices)
    if score > 60:
        await message.reply_text(f"🔍 Result: {result}\n🔗 {MOVIES[result]}")
    else:
        await message.reply_text("❌ Nahi mila!")

# --- Universal Health Check Server ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Kisi bhi path (/kaithhealthcheck ho ya kuch bhi) par 200 OK dega
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    print("🌐 Health Check Server Active on Port 8080")
    server.serve_forever()

# --- Run ---
async def start_bot():
    # Server ko alag thread mein start karenge
    threading.Thread(target=run_server, daemon=True).start()
    
    print("🛰 Starting Pyrogram...")
    await app.start()
    print("✅ SUCCESS: BOT LIVE HOGAYA!")
    await idle()

if __name__ == "__main__":
    asyncio.run(start_bot())
    

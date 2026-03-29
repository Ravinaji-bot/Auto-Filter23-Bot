import os
import asyncio
import threading
from pyrogram import Client, filters, idle
from thefuzz import process

# --- 1. Bot Configuration ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# in_memory=True aur workdir="/tmp" taaki Read-only error na aaye
app = Client(
    "my_filter_bot",
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
    await message.reply_text("**Bot Online Hai Sir! 🙏**\nMovie ka naam bhejiye.")

@app.on_message(filters.text & filters.private)
async def search_handler(client, message):
    query = message.text
    choices = list(MOVIES.keys())
    result, score = process.extractOne(query, choices)
    if score > 60:
        await message.reply_text(f"🔍 **Mili:** {result}\n🔗 [Download]({MOVIES[result]})")
    else:
        await message.reply_text("❌ Nahi mili sir.")

# --- 4. Bot Runner Function ---
def run_pyrogram():
    print("🚀 Starting Pyrogram Bot...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.start())
    print("✅ Bot is Online!")
    idle()

# Bot ko alag thread mein start karna taaki Leapcell ko response milta rahe
threading.Thread(target=run_pyrogram, daemon=True).start()

# --- 5. Leapcell WSGI Handler ---
def wsgi(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b"Bot is Running!"]

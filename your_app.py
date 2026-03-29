import os
import asyncio
import threading
from pyrogram import Client, filters, idle
from thefuzz import process

# --- Bot Configuration ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# 'in_memory=True' aur 'workdir="/tmp"' Read-only system ke liye RAM use karte hain
app = Client(
    "my_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    workdir="/tmp"
)

# --- Movie Database ---
MOVIES = {
    "Pushpa 2": "https://t.me/example/1",
    "Maharaja": "https://t.me/example/4",
    "Stree 2": "https://t.me/example/5"
}

# --- Handlers ---
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

# --- Bot Runner ---
def run_pyrogram():
    print("🚀 Starting Pyrogram Bot in Background...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(app.start())
        print("✅ SUCCESS: Bot is Online!")
        idle()
    except Exception as e:
        print(f"❌ Pyrogram Error: {e}")

# Threading start
t = threading.Thread(target=run_pyrogram, daemon=True)
t.start()

# --- Leapcell WSGI Handler ---
def wsgi(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b"Bot is Running!"]

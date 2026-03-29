import os
import asyncio
from pyrogram import Client, filters, idle
from thefuzz import process

# --- Configuration (Leapcell Env Variables se lega) ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Bot Client Setup
# workdir="/tmp" dena zaroori hai Leapcell ke liye
app = Client(
    "auto_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    workdir="/tmp" 
)

# --- Movie Database ---
MOVIES = {
    "Pushpa 2": "https://t.me/example/1",
    "Maharaja": "https://t.me/example/4"
}

# --- Handlers ---
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text("**Namaste! 🙏\nMain online hoon aur kaam kar raha hoon!**")

@app.on_message(filters.text & filters.private)
async def search_handler(client, message):
    query = message.text
    choices = list(MOVIES.keys())
    result, score = process.extractOne(query, choices)
    
    if score > 60: 
        link = MOVIES[result]
        await message.reply_text(f"🔍 **Result:** {result}\n🔗 [Download]({link})")
    else:
        await message.reply_text("❌ Sorry, ye movie nahi mili!")

# --- Boot Logic ---
async def run_bot():
    try:
        print("🛰 Connecting to Telegram...")
        await app.start()
        print("✅ SUCCESS: Bot is Online!")
        await idle()
    except Exception as e:
        print(f"❌ BOT CRASH ERROR: {e}")
    finally:
        if app.is_connected:
            await app.stop()

if __name__ == "__main__":
    # Asyncio loop ko sahi se handle karne ke liye
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        pass
    

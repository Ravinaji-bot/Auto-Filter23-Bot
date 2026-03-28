import os
import asyncio
import sys
from pyrogram import Client, filters, idle
from thefuzz import process

# --- Configuration (Leapcell Settings se fetch karega) ---
#
try:
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
except ValueError:
    print("❌ ERROR: API_ID must be a number! Check Leapcell Env Variables.")
    sys.exit(1)

# Bot Client Setup
# in_memory=True lagaya hai taaki read-only system par session file ka error na aaye
app = Client(
    "auto_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True 
)

# --- Sample Movie Data ---
#
MOVIES = {
    "Pushpa 2": "https://t.me/example/1",
    "Van Helsing": "https://t.me/example/2",
    "Pirates of the Caribbean": "https://t.me/example/3",
    "Maharaja": "https://t.me/example/4"
}

# --- Handlers ---

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text(
        "**Namaste! 🙏**\n\n"
        "Main online hoon. Bas movie ka naam likhiye, "
        "main link dhund kar de dunga!"
    )

@app.on_message(filters.text & filters.private)
async def search_handler(client, message):
    query = message.text
    choices = list(MOVIES.keys())
    
    # Fuzzy matching logic
    result, score = process.extractOne(query, choices)
    
    if score > 60: 
        link = MOVIES[result]
        await message.reply_text(
            f"🔍 **Result Found:** `{result}`\n"
            f"✅ **Match Score:** {score}%\n\n"
            f"🔗 [Download Link]({link})",
            disable_web_page_preview=True
        )
    else:
        await message.reply_text("❌ Sorry! Ye movie hamare database mein nahi hai.")

# --- Main Boot Logic ---

async def run_bot():
    try:
        print("🛰 Connecting to Telegram...")
        await app.start()
        print("✅ SUCCESS: Bot is Online!")
        await idle()
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
    finally:
        if app.is_connected:
            await app.stop()

if __name__ == "__main__":
    # Asyncio loop run karne ka sahi tarika
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())

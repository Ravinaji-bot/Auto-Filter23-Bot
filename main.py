import os
import asyncio
from pyrogram import Client, filters, idle
from thefuzz import process

# --- Configuration (Leapcell Settings se lega) ---
API_ID = int(os.environ.get("API_ID", "0")) 
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Bot Client Setup
app = Client(
    "auto_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Sample Movie Data (Yahan apni list badal sakte hain) ---
MOVIES = {
    "Pushpa 2": "https://t.me/your_channel/1",
    "Van Helsing": "https://t.me/your_channel/2",
    "Pirates of the Caribbean": "https://t.me/your_channel/3",
    "Maharaja": "https://t.me/your_channel/4"
}

# --- Handlers ---

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text(
        "**Namaste! 🙏**\n\n"
        "Main ek Auto-Filter Bot hoon. Bas movie ka naam likhiye, "
        "main link dhund kar de dunga!"
    )

@app.on_message(filters.text & filters.private)
async def search_handler(client, message):
    query = message.text
    choices = list(MOVIES.keys())
    
    # Fuzzy matching logic (naam thoda galat hone par bhi dhund lega)
    result, score = process.extractOne(query, choices)
    
    if score > 60: 
        link = MOVIES[result]
        await message.reply_text(
            f"🔍 **Result Found:** `{result}`\n"
            f"✅ **Match Score:** {score}%\n\n"
            f"🔗 [Yahan se Download karein]({link})",
            disable_web_page_preview=True
        )
    else:
        await message.reply_text("❌ Sorry! Ye movie hamare database mein nahi hai.")

# --- Boot Logic ---

async def main():
    print("🚀 Bot starting...")
    await app.start()
    print("✅ Bot is Online!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    # Asyncio loop run karne ke liye
    asyncio.get_event_loop().run_until_complete(main())
    

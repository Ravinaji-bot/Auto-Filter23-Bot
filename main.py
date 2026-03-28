import os
import asyncio
import sys
from pyrogram import Client, idle

# --- Configuration ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client(
    "auto_filter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def start_bot():
    try:
        print("🛰 Attempting to connect to Telegram...")
        await app.start()
        print("✅ BOT IS ONLINE NOW!")
        await idle()
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        # Isse server turant restart nahi hoga, hum error padh payenge
        await asyncio.sleep(30) 
    finally:
        if app.is_connected:
            await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
    

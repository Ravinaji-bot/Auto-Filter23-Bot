import os
import asyncio
from pyrogram import Client, idle

# Bot Client - in_memory=True lagana zaroori hai read-only system ke liye
app = Client(
    "my_bot",
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN"),
    in_memory=True  # Ye line Read-only error ko fix karegi
)

async def start():
    await app.start()
    print("✅ Bot is Online!")
    await idle()

if __name__ == "__main__":
    asyncio.run(start())
    

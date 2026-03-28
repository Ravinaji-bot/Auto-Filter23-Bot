import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from thefuzz import process, fuzz

# --- APNI DETAILS YAHAN BHAREIN ---
API_ID = 24358501
API_HASH = "fa51ce8876c215d8a76c98c755e6d2d3"
BOT_TOKEN = "aapka_bot_token"
OWNER_ID = 1834715690 # <--- Yahan apni Telegram User ID daalein (BotFather ya @userinfobot se mil jayegi)

SOURCE_CHANNEL_ID = -1002006644667 
TARGET_GROUP_ID = -1002142709211
DELETE_TIME = 300 
# --------------------------------

app = Client("AdvancedMovieBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

movie_db = {} 

async def update_movie_list():
    global movie_db
    async for msg in app.get_chat_history(SOURCE_CHANNEL_ID, limit=500):
        if msg.caption:
            title = msg.caption.split('\n')[0].strip()
            movie_db[title] = msg.id

# --- STATS COMMAND (SIRF OWNER KE LIYE) ---
@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def get_stats(client, message):
    # Bot kitne groups/chats mein hai uski counting
    count = 0
    async for dialog in client.get_dialogs():
        count += 1
    
    # Isme hum approximate members bhi dikha sakte hain agar bot admin hai
    status_text = (
        "📊 **Bot Statistics**\n\n"
        f"👥 **Total Chats/Groups:** `{count}`\n"
        f"🎥 **Movies in DB:** `{len(movie_db)}`\n"
        "👤 **Access:** `Owner Only`"
    )
    await message.reply_text(status_text)

# --- SEARCH LOGIC ---
@app.on_message(filters.chat(TARGET_GROUP_ID) & filters.text & ~filters.command(["stats"]))
async def search_and_send(client, message):
    query = message.text.lower()
    found_msg = None

    # 1. Direct Search
    async for m in client.search_messages(chat_id=SOURCE_CHANNEL_ID, query=query, limit=1):
        found_msg = m

    # 2. AI Fuzzy Matching (Agar spelling galat hai)
    if not found_msg and movie_db:
        titles = list(movie_db.keys())
        best_match, score = process.extractOne(query, titles, scorer=fuzz.token_set_ratio)
        
        if score > 75: 
            post_id = movie_db[best_match]
            found_msg = await client.get_messages(SOURCE_CHANNEL_ID, post_id)

    # 3. Post bhejna aur Auto-Delete
    if found_msg and found_msg.media:
        buttons = []
        if found_msg.reply_markup and found_msg.reply_markup.inline_keyboard:
            for row in found_msg.reply_markup.inline_keyboard:
                btn_row = [InlineKeyboardButton(b.text, url=b.url) for b in row if b.url]
                if btn_row: buttons.append(btn_row)

        sent_msg = await found_msg.copy(
            chat_id=TARGET_GROUP_ID,
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
        )

        info = await message.reply_text(f"✅ **Result found!**\n🗑️ Auto-delete in 5 mins.")
        
        await asyncio.sleep(DELETE_TIME)
        try:
            await sent_msg.delete()
            await info.delete()
            await message.delete()
        except: pass
    else:
        err = await message.reply_text(f"❌ '{query}' nahi mila.")
        await asyncio.sleep(10)
        try:
            await err.delete()
            await message.delete()
        except: pass

@app.on_connect()
async def on_start(client, _):
    await update_movie_list()
    print("✅ Movie Database Updated & Bot is Ready!")

app.run()
  

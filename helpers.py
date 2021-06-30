class Text():
    how_to = "`Either reply to an audio file or give me a youtube link to play from!`"
    not_yet = "`This is not yet supported!`"
    dl = "`Downloading...`"
    
async def play_a_song(pycalls, message, song):
    try:
        await pycalls.stream(message.chat.id, song)
    except Exception as e:
        await message.reply_text(f"ERROR:\n{e}")

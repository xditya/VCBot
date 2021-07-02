class Text:
    how_to = "`Either reply to an audio file or give me a youtube link to play from!`"
    not_yet = "`This is not yet supported!`"
    dl = "`Downloading...`"
    helper = """
**Available Commands:**\n
  - `{x}on` - __check if the (user)bot is online.__
  - `{x}stream <url/reply to song file>` - __play song in vc.__ 
  - `{x}pause` - __pause track.__
  - `{x}resume` - __resumes the paused track.__
  - `{x}song <song name>` - __donwload the song.__

**Support:** __@BotzHubChat__."""


async def play_a_song(pycalls, message, song):
    try:
        await pycalls.stream(message.chat.id, song)
    except Exception as e:
        await message.reply_text(f"ERROR:\n{e}")

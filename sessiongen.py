from pyrogram import Client

API_ID = API_HASH = None
try:
    from decouple import config

    API_ID = config("API_ID")
    API_HASH = config("API_HASH")
except:
    API_ID = int(input("Enter your api id: "))
    API_HASH = input("Enter your api hash: ")

# generate a session
print("Enter phone number when asked.\n\n")
if not API_ID and API_HASH:
    print("Missing api id and hash!")
    exit(0)
with Client(":memory", api_id=API_ID, api_hash=API_HASH) as pyro:
    ss = pyro.export_session_string()
    pyro.send_message(
        "me",
        f"`{ss}`\n\nAbove is your Pyrogram Session String for music bot. **DO NOT SHARE it.**",
    )
    print("Session has been sent to your saved messages!")
    exit(0)

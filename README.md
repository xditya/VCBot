# VCBOT
Fully working VC (user)Bot, based on py-tgcalls and py-tgcalls-wrapper with minimal [features](#TODO).   


## Deploying
* To heroku:   
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)   
Turn the dyno on and hope it works.   

* Local machine/VPS:   
`git clone https://github.com/xditya/VCBot`   
`pip install -r requirements.txt`   
`apt-get install ffmpeg`   
`python bot.py`   


## Commands:   
- `!on` - Check if the (user)bot is online.   
- `!stream` - Either give a youtube URL or reply to a telegram file to play it.   
- `!pause` - Pause the stream.   
- `!resume` - Yes, resume.   

## Support
- [@BotzHub](https://t.me/BotzHubChat)   


## TODO
(Contributions accepted, I'm lazy af.)    
- A queue system.   
- Play with song name.   
- JoinVC/LeaveVC   


## Credits
- [pytgcalls](https://github.com/pytgcalls/pytgcalls)   
- [pytgcalls-wrapper](https://github.com/callsmusic/pytgcalls-wrapper)   
- [Pyrogram](https://github.com/pyrogram/pyrogram)   
- [Me](https://github.com/xditya)   

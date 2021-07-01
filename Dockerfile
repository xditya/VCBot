# debian.
FROM debian:latest

RUN apt-get update && apt-get upgrade -y

# the basic requirements.
RUN apt-get install -y ffmpeg python3-pip curl
RUN python3 -m pip install -U pip

# install nodejs.
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

COPY . .

# install requirements.
RUN python3 -m pip install -U -r requirements.txt

# run the bot.
CMD ["python3", "bot.py"]

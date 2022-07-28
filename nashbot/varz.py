# varz.py


from pathlib import Path


# trackers

frozen_users = []
active_menus = []


# constants

BLANK = '\n\u200b\n'
STOP_EMOJI = '\N{BLACK SQUARE FOR STOP}\ufe0f'
BOT_INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id=985864214260371476&permissions=8&scope=bot'

FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', }
YDL_OPTS = {'format': 'bestaudio', 'noplaylist': True, }

ALBUMS_PATH = Path('E:/BACKUPS/Music Backup/Music/')
DOWNLOADS_PATH = Path('E:/BACKUPS/Music Backup/unsorted/nashbot downloads/')
DOWNLOADS_LOG_PATH = Path('history/downloads_log.txt')
COGS_PATH = Path('cogs/')
MEDIA_PATH = Path('media/')
SKELLY_PATH = MEDIA_PATH / 'skeleton_gifs/'

# vars.py


from pathlib import Path


# trackers

frozen_users = []
active_menus = []


# constants

FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', }
YDL_OPTS = {'format': 'bestaudio', 'noplaylist': True, }

ALBUMS_PATH = Path('E:/BACKUPS/Music Backup/Music/')
COGS_PATH = Path('cogs/')
MEDIA_PATH = Path('media/')
SKELLY_PATH = MEDIA_PATH / 'skeleton_gifs/'

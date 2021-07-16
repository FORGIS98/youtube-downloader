# youtube-downloader
"Tool" to download music (or videos) from youtube with the help of youtube-dl. The code makes a call to the youtube API, then it lists some videos, you choose the one you want to download and done :D

# Instalation
## Getting the Token
First step is to get youtube API token (to be aible to call youtube API):
- Check this link [Get api key for yt](https://www.slickremix.com/docs/get-api-key-for-youtube/) where they explain how to get it.
- Or this one...where they don't explain it ["Get api key for yt"](https://developers.google.com/youtube/registering_an_application?hl=en)

## Prerequisites
This tool will use [youtube-dl](https://github.com/ytdl-org/youtube-dl):
```bash
sudo apt install youtube-dl
sudo pacman -Sy youtube-dl
sudo pip install youtube-dl
```
Or check https://github.com/ytdl-org/youtube-dl  

Then also the python library [google-api-python-client](https://github.com/googleapis/google-api-python-client)
```bash
pip isntall google-api-python-client
```

## About Python
This are the versions I'm using:
```console
λ ~ pip -V                              
pythopip 20.3.4 from /usr/lib/python3.9/site-packages/pip (python 3.9)

λ ~ python -V                  
Python 3.9.6
```

## How to use it

```bash
git clone https://github.com/FORGIS98/youtubeDownloader.git
cd youtubeDownloader
```

Availables flags:
- `--SEARCH`: What do you want to search on youtube, please wrap the text with double-quotes.
- `--max-results`: How many results do you want to output.
- `--folder`: Where do you want to put the song or video you are downloading.
- `--format`: Chose between mp3 and mp4.

Examples:
```bash
python youtubeDownloader.py --SEARCH="EDM" --max-results=5 --folder="~/MyAwesomeMusic" --format="mp3"
python youtubeDownloader.py --SEARCH="EDM"
```

The code has some default options if you don't put a flag. If you wan't to change them, open the code, go all the way down and change `default` values. For example:  
```python
# Original code
parser.add_argument('--SEARCH', help="Search from term", default="Music")
parser.add_argument('--max-results', help="Max results output", default=5)
parser.add_argument('--folder', help="Full path to downloads folder", default=music_folder)
parser.add_argument('--format', help="mp3 or mp4", default="mp3")

# Example changes
parser.add_argument('--max-results', help="Max results output", default=10)
parser.add_argument('--folder', help="Full path to downloads folder", default="~/MyAwesomeMusic/CoolMusic")
```

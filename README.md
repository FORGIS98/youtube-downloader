# youtubeDownloader
This tool will help you download mp3 and mp4 youtube videos. The main objective of this tool is to learn how to use an API, in this case, youtube API. For this tool to work on your computer, you will need a token given by youtube.

## Getting the Token
- Check this link https://www.slickremix.com/docs/get-api-key-for-youtube/ where they explain it.
- Or here...where they don't explain it https://developers.google.com/youtube/registering_an_application?hl=en

## Prerequisites
This tool will use youtube-dl and youtube API, for youtube-dl do:
```bash
sudo apt install youtube-dl
sudo pacman -Sy youtube-dl
sudo pip3 install youtube-dl
```
Or check https://github.com/ytdl-org/youtube-dl
_I will add more details after I run some test on a docker to check if some extra things are needed._

## How to use it
After cloning the repo and moving to the folder:
```bash
git clone https://github.com/FORGIS98/youtubeDownloader.git
cd youtubeDownloader
```
You have 2 options, using all the flags available or opening `youtubeDownloader.py` and changing the global variables at the beginning of the code.

If you want to use flags:
- `--SEARCH`: What do you want to search on youtube, please wrap the text with double-quotes.
- `--max-results`: How many results do you want to output.
- `--folder`: Where do you want to put the song or video you are downloading.
- `--format`: Chose between mp3 and mp4.
Example (use python version of your choice):
```bash
python3 youtubeDownloader.py --SEARCH="Chill Music" --max-results=5 --folder="~/MyAwesomeMusic" --format="mp3"
```

If you want to change global variables, I will upload more details soon.

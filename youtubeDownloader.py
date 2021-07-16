#!/usr/bin/env python3

import os
import argparse
import subprocess, shlex

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = os.environ['DEV_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = 'v3'

# This is for youtube-dl
YOUTUBE_DL_URL="https://www.youtube.com/watch?v="

### BEGIN - AUX FUNCTIONS ###
def getUserRegion():
    someRegions = {
        "Madrid" : "ES",
        "Paris" : "FR",
        "London" : "GB",
        "Berlin" : "DE",
        "Rome" : "IT",
        "America" : "US"
    }
    command = "timedatectl | grep Time"
    zone = subprocess.getoutput('timedatectl show --va -p Timezone | cut -d\'/\' -f2')
    try:
        return someRegions[zone]
    except KeyError:
        return "ES"


def changeName():
    ans = str(input("Do you want to rename the title? [Y/n]: "))
    if(ans in ["", "Y", "y"]):
        return str(input("New title: "))
    return None
### END - AUX FUNCTIONS ###


def yt_search(args):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    yt_response = youtube.search().list(
        q=args.SEARCH,
        part='id, snippet',
        maxResults=args.max_results,
        order="relevance",
        regionCode=getUserRegion()
    ).execute()

    videos = []
    videoId = []
    videosChannel = []

    for yt_result in yt_response.get('items', []):
        if yt_result['id']['kind'] == "youtube#video":
            videos.append('%s ' % (yt_result['snippet']['title']))
            videoId.append('%s ' % (yt_result['id']['videoId']))
            videosChannel.append('%s ' % (yt_result['snippet']['channelTitle']))
    video_selection(videos, videoId, videosChannel, args)


def video_selection(videos, videoId, videosChannel, args):
    print("")
    for i in range (len(videos)):
        print("Video Nº " + "%d" % (i+1) + ": " + videosChannel[i] + " ==> " + videos[i])
    print("")
    print("\n")

    # x = int(input("Choose the video you like to download: ")) - 1
    # com_line = "youtube-dl -x --audio-format " + args.format + " -o "+ args.folder + " " + YOUTUBE_DL_URL + videoId[x]
    # 
    # newName = changeName()
    # if(newName != None):
    #     subprocess.call(shlex.split(com_line))
    #     oldOne = os.path.join(args.folder, videos[x])
    #     newOne = os.path.join(args.folder, newName)
    #     os.rename(oldOne, newOne)
    # else:
    #     subprocess.call(shlex.split(com_line))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--SEARCH', help="Search from term", default="Music")
    parser.add_argument('--max-results', help="Max results output", default=5)
    parser.add_argument('--folder', help="Full path to downloads folder", default="~/")
    parser.add_argument('--format', help="mp3 or mp4", default="mp3")

    args = parser.parse_args()

    try:
        yt_search(args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    except Exception as e:
        print(e)

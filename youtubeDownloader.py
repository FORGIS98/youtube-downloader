#!/usr/bin/env python3

import os
import argparse
import subprocess, shlex

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = os.environ['DEV_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = 'v3'

YOUTUBE_DL_URL="https://www.youtube.com/watch?v="


### BEGIN - AUX FUNCTIONS ###

def getUserRegion():
    """
    Returns your region, we use the value when searching videos on youtube.
    Default value is ES
    """
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
    """
    Allows to give a new name to the video you are about to download.
    """
    ans = str(input("Do you want to rename the title? [Y/n]: "))
    if(ans in ["", "Y", "y"]):
        newName = str(input("New title: "))
        newName += ".%(ext)s"
        return newName
    # Format for youtube-dl, the video/audio will have the original yt name
    return "%(title)s-%(id)s.%(ext)s" 

### END - AUX FUNCTIONS ###


def yt_search(args):
    """ 
    Calls Youtube API and gets a list of videos.
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    yt_response = youtube.search().list(
        q=args.SEARCH,
        part='id, snippet',
        maxResults=args.max_results,
        order="relevance",
        regionCode=getUserRegion()
    ).execute()

    videos = []
    videosId = []
    videosChannel = []

    # We "sort" the info in 3 diff lists
    for yt_result in yt_response.get('items', []):
        if yt_result['id']['kind'] == "youtube#video":
            videos.append('%s ' % (yt_result['snippet']['title'])) # To show the video title
            videosId.append('%s ' % (yt_result['id']['videoId'])) # To know the video id you may want to download
            videosChannel.append('%s ' % (yt_result['snippet']['channelTitle'])) # To know the channels name
    video_selection(videos, videosId, videosChannel, args)


def video_selection(videos, videosId, videosChannel, args):
    """
    Shows a list of videos and let's you choose one, change the name and download it.
    """
    print("")
    for i in range (len(videos)):
        print("Video Nº " + "%d" % (i+1) + ": " + videosChannel[i] + " ==> " + videos[i])
    print("")
    print("\n")

    videoNumber = int(input("Choose the video you like to download: ")) - 1
    newName = changeName()

    command = "youtube-dl -x --audio-format " + args.format + " -o " + args.folder + newName + " " + YOUTUBE_DL_URL + videosId[videoNumber]
    print(command)
    subprocess.call(shlex.split(command))


if __name__ == '__main__':

    music_folder = subprocess.getoutput('xdg-user-dir MUSIC') # Get your music folder

    parser = argparse.ArgumentParser()
    parser.add_argument('--SEARCH', help="Search from term", default="Music")
    parser.add_argument('--max-results', help="Max results output", default=5)
    parser.add_argument('--folder', help="Full path to downloads folder", default=music_folder)
    parser.add_argument('--format', help="mp3 or mp4", default="mp3")
    args = parser.parse_args()

    if(not args.folder.endswith("/")):
        args.folder += "/"

    try:
        yt_search(args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    except Exception as e:
        print(e)

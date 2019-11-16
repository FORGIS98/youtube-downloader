#!/usr/bin/env python3

import os                   # for environment variables
import argparse             # for flags
import subprocess, shlex    # to call UNIX commands

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = os.environ['DEV_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = 'v3'
MY_YOUTUBE_SEARCH="https://www.youtube.com/watch?v="
USER_FOLDER = ""
USER_FORMAT = ""
USER_MAX_RESULTS = ""


class downloader():
    # myRegion() will return the ISO 3166 alpha-2 code of yout region.
    # If your region is not in the list, read README.md for details.
    def myRegion(self): # returns a STRING

        someRegions = {
            "Madrid" : "ES",
            "Paris" : "FR",
            "London" : "GB",
            "Berlin" : "DE",
            "Rome" : "IT",
            "America" : "US"
        }

        stupidList = ["Madrid", "Paris", "London", "Berlin", "Rome", "America"]

        command = "cat /etc/timezone"
        # WTF is this, so, .run runs the command, .stdout takes the output, .decode decodes the byte output to string.
        zone = subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode('utf-8')

        # TODO: Improve this little function
        for z in stupidList:
            if(z in zone):
                return someRegions[z]
        return "ES" # Default: Spain

    # yt_search(args) returns the youtube search specified in --SEARCH flag
    def yt_search(self, args):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        yt_response = youtube.search().list(
            q=args.SEARCH, # The parameter q specifies the query term to be searched.
            part='id, snippet', # The part parameter specifies a comma separated list of one or more search resource properties that the API response will include.
            maxResults=USER_MAX_RESULTS, # With the '_' instead of '-'.
            order="relevance", # Videos will be sorted by views.
            regionCode=self.myRegion() # The API will display the search results for the specified country.
        ).execute()

        videos = []
        videoId = []
        videosChannel = []

        for yt_result in yt_response.get('items', []):
            if yt_result['id']['kind'] == "youtube#video":
                videos.append('%s ' % (yt_result['snippet']['title']))
                videoId.append('%s ' % (yt_result['id']['videoId']))
                videosChannel.append('%s ' % (yt_result['snippet']['channelTitle']))
        self.video_selection(videos, videoId, videosChannel)

    def video_selection(self, videos, videoId, videosChannel):
        for i in range (len(videos)):
            print("----------------------------------------------------------------------")
            print("Video Nº " + "%d" % (i+1) + ": " + videos[i] + "   Uploaded by: " + videosChannel[i])
        print("----------------------------------------------------------------------")
        print("\n")

        x = int(input("Choose the video you like to download: ")) - 1
        com_line = "youtube-dl -x --audio-format " + USER_FORMAT + " -o "+ USER_FOLDER + " " + MY_YOUTUBE_SEARCH + videoId[x]
        #subprocess.call(shlex.split(com_line))
        print("CONTROL PRINT")

# In python3 you don't need the if __name__ == '__main__':
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--SEARCH', help="Search from term.", default="youtube")
    parser.add_argument('--max-results', help="Max results output", default=5)
    parser.add_argument('--folder', help="Folder where files download", default="~/")
    parser.add_argument('--format', help="mp3 or mp4", default="mp3")

    args = parser.parse_args()

    if USER_FOLDER == "":
        USER_FOLDER = "\'" + args.folder + "%(title)s.%(ext)s\'"
    if USER_FORMAT == "":
        USER_FORMAT = args.format
    if USER_MAX_RESULTS == "":
        USER_MAX_RESULTS = args.max_results

    myDownload = downloader()
    myDownload.yt_search(args)

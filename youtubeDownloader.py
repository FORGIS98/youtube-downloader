#!/usr/bin/python

import os                   # for environment variables
import argparse             # for flags
import subprocess, shlex    # to call UNIX commands

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = os.environ['DEV_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = 'v3'

# In python3 you don't need the if __name__ == '__main__':
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--SEARCH', help="Search from term.", default="youtube")
    parser.add_argument('--max-results', help="Max results output", default=5)
    args = parser.parse_args()

    yt_search(args)

    # flags = " -l -a"
    # com_line = "ls" + flags
    # subprocess.call(shlex.split(com_line))
    

# yt_search(args) returns the youtube search specified in --SEARCH flag
def yt_search(args):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    yt_response = youtube.search().list(
        q=args.SEARCH, # The parameter q specifies the query term to be searched.
        part='id, snippet', # The part parameter specifies a comma separated list of one or more search resource properties that the API response will include.
        maxResults=args.max_results # With the '_' instead of '-'
    ).execute()

    videos = []

    for yt_result in yt_response.get('items', []):
        if yt_result['id']['kind'] == "youtube#video":
            videos.append('%s (%s)' % (yt_result['snippet']['title'], yt_result['id']['videoId']))

    print("Videos: \n", "\n".join(videos), "\n")

















main()

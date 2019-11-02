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
        maxResults=args.max_results, # With the '_' instead of '-'.
        order="relevance", # Videos will be sorted by visits.
        regionCode=myRegion() # The API will display the search results for the specified country.
    ).execute()

    videos = []

    for yt_result in yt_response.get('items', []):
        if yt_result['id']['kind'] == "youtube#video":
            videos.append('%s (%s)' % (yt_result['snippet']['title'], 
                yt_result['id']['videoId']))
            # print("ID DEL VIDEO :: ", yt_result['id']['videoId'])

    print("Videos: \n", "\n".join(videos), "\n")


# myRegion() will return the ISO 3166 alpha-2 code of yout region.
# If your region is not in the list, read README.md for details.
def myRegion(): # returns a STRING
    
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









main()

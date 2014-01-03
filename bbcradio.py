#!/usr/local/bin/python3
"""
Tools for helping Audio Hijack Pro record BBC Radio programmes

Command-line usage:
    bbcradio.py <programme name>

The programme name should be a key of PROG_DICT, and its value is
the unique programme code used on the BBC website.

This programme code is then used to fetch the unique episode code,
from which we can create the streaming URL and fetch the track list.

When run as a shell script, it prints the URL to stdout and writes
the track list to a file in the Audio Hijack Pro recordings directory,
with the intention that this is cleaned up by a post-processing
AppleScript run by Audio Hijack Pro once the recording is finished.

"""

import sys
import requests
from bs4 import BeautifulSoup as soup

PROG_DICT = {'jazz on 3': 'b006tt0y',
             'jazz line-up': 'b006tnmw'}


def latest_episode_code(programme):
    """Returns the code for a programme’s latest episode"""
    guide_url = 'http://www.bbc.co.uk/programmes/{}/episodes/player'
    guide_response = requests.get(guide_url.format(programme))
    guide_soup = soup(guide_response.text)

    try:
        soup_node = guide_soup.find(class_='episode')
        code = soup_node.a['href'].split('/')[-1]
    except AttributeError:
        sys.exit('No episodes available')

    return code


def episode_player_url(episode):
    """Returns the player URL for the given episode code"""
    player_url = 'http://www.bbc.co.uk/radio/player/{}'
    return player_url.format(episode)


def fetch_episode_details(episode):
    """Returns a formatted track list string for the given episode code"""
    episode_url = 'http://www.bbc.co.uk/programmes/{}'
    episode_response = requests.get(episode_url.format(episode))
    episode_soup = soup(episode_response.text)

    track_nodes = episode_soup.select('li.segment.track')
    track_list = []
    for node in track_nodes:
        try:
            artist = node.find(class_='artist').text
            title = node.find(class_='title').text

            # Extra try block in case times are missing
            try:
                time = node.find(class_='play-time').text
            except AttributeError:
                time = None

            # Join details, filtering for None
            details = '\n'.join([x for x in [time, artist, title] if x])
            track_list.append(details)
        except AttributeError:
            continue

    track_list_string = '\n\n'.join(track_list)
    descriptive_title = episode_soup.find(class_='episode-title').text
    date_node = episode_soup.find('p', {'datatype': 'xsd:datetime'})
    broadcast_date = date_node['content'].split('T')[0]
    return (broadcast_date, descriptive_title, track_list_string)

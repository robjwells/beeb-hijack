#!/usr/local/bin/python3
"""
Tools for helping Audio Hijack Pro record BBC Radio programmes

This module should not be run directly, but rather imported
by pre/post-recording scripts called by Audio Hijack Pro.
"""

import sys
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup

PROG_DICT = {'jazz on 3': 'b006tt0y',
             'jazz line-up': 'b006tnmw'}


def latest_episode_code(programme):
    """Get the code for a programme’s most recent episode"""
    guide_url = 'http://www.bbc.co.uk/programmes/{}/episodes/player'
    try:
        guide_response = urlopen(guide_url.format(programme))
    except HTTPError:
        return None
    guide_soup = soup(guide_response.read().decode())

    try:
        soup_node = guide_soup.find(class_='episode')
        code = soup_node.a['href'].split('/')[-1]
    except AttributeError:
        sys.exit('No episodes available')

    return code


def episode_player_url(episode):
    """Return the player URL for the given episode code"""
    player_url = 'http://www.bbc.co.uk/radio/player/{}'
    return player_url.format(episode)


def episode_details(episode):
    """Construct a tuple of the episode’s date, title and track list"""
    episode_url = 'http://www.bbc.co.uk/programmes/{}'
    episode_response = urlopen(episode_url.format(episode))
    episode_soup = soup(episode_response.read().decode())

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

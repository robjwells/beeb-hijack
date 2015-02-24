#!/usr/local/bin/python3
"""
Tools for helping Audio Hijack Pro record BBC Radio programmes

This module should not be run directly, but rather imported
by pre/post-recording scripts called by Audio Hijack Pro.
"""

import re
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

    soup_node = guide_soup.find(class_='programme--episode')
    code = soup_node['resource'].split('/')[-1]

    return code


def episode_player_url(episode):
    """Return the player URL for the given episode code"""
    player_url = 'http://www.bbc.co.uk/radio/player/{}'
    return player_url.format(episode)


def episode_details(episode):
    """Construct a tuple of the episode’s date, title and track list"""
    segments_url = 'http://www.bbc.co.uk/programmes/{}/segments'
    try:
        segments_response = urlopen(segments_url.format(episode))
        segments_soup = soup(segments_response.read().decode())

        track_nodes = segments_soup.find_all(class_='segment__track')
        track_list = []
        for node in track_nodes:
            try:
                artist = node.find(class_='artist').text
                title = node.find('p').find(property='name').text

                # Extra try block in case times are missing
                try:
                    time = node.find(text=re.compile(r'^\d{2}:\d{2}$'))
                except AttributeError:
                    time = None

                # Join details, filtering for None
                details = '\n'.join([x for x in [time, artist, title] if x])
                track_list.append(details)
            except AttributeError:
                continue

        track_list_string = '\n\n'.join(track_list)
    except HTTPError:
        track_list_string = ''

    prog_page = 'http://www.bbc.co.uk/programmes/{}'
    prog_response = urlopen(prog_page.format(episode))
    prog_soup = soup(prog_response.read().decode())
    descriptive_title = prog_soup.h1.text
    date_node = prog_soup.find(attrs={'datatype': 'xsd:dateTime'})
    broadcast_date = date_node['content'].split('T')[0]
    return (broadcast_date, descriptive_title, track_list_string)

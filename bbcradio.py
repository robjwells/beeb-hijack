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

from bs4 import BeautifulSoup

PROG_DICT = {'jazz on 3': 'b006tt0y',
             'jazz line-up': 'b006tnmw'}


class NoneAvailableError(Exception):
    """Raised when there are no episodes of a programme available"""
    pass


def latest_episode_code(programme_name):
    """Get the code for a programme’s most recent episode"""
    programme_code = PROG_DICT[programme_name]
    guide_url = 'http://www.bbc.co.uk/programmes/{}/episodes/player'
    try:
        guide_response = urlopen(guide_url.format(programme_code))
    except HTTPError:
        raise NoneAvailableError(
            'Could not open the guide page for {}'.format(programme_name)
            )
    guide_soup = BeautifulSoup(guide_response.read().decode(), 'html.parser')

    soup_node = guide_soup.find(class_='programme--episode')
    try:
        ep_code = soup_node['resource'].split('/')[-1]
        return ep_code
    except TypeError:
        raise NoneAvailableError(
            'No episodes available for {}'.format(programme_name)
            )


def episode_player_url(episode):
    """Return the player URL for the given episode code"""
    player_url = 'http://www.bbc.co.uk/radio/player/{}'
    return player_url.format(episode)


def episode_details(episode):
    """Construct a tuple of the episode’s date, title and track list"""
    segments_url = 'http://www.bbc.co.uk/programmes/{}/segments'
    try:
        segments_response = urlopen(segments_url.format(episode))
        segments_soup = BeautifulSoup(segments_response.read().decode(),
                                      'html.parser')

        track_nodes = segments_soup.find_all(class_='segment__track')
        track_list = []
        for node in track_nodes:
            try:
                artist = node.find(class_='artist').text
                title = node.find('p').find(property='name').text
                time = node.find(text=re.compile(r'^\d{2}:\d{2}$'))

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
    prog_soup = BeautifulSoup(prog_response.read().decode(),
                              'html.parser')
    descriptive_title = prog_soup.h1.text
    date_node = prog_soup.find(attrs={'datatype': 'xsd:dateTime'})
    broadcast_date = date_node['content'].split('T')[0]
    return (broadcast_date, descriptive_title, track_list_string)

import os
import time
from urllib.parse import urlencode

import requests

import home

SDAROT_FULL_WATCH = 'https://www.sdarot.tw/ajax/watch'
LOGIN = '/login'
USERNAME = 'enter here your username'
PASSWORD = 'enter here your password'
SEASON = 'season_'
EPISODE = 'episode_'
VIDEO_END = '.mp4'
session = requests.session()
SDAROT_FILE = r'C:\Users\tlv\Documents\Sdarot'


def login():
    """
    function that connect with the user to sdarot.buzz
    :return: nothing
    """
    data = {
        "location": "/index",
        "username": USERNAME,
        "password": PASSWORD,
        "login_remember": "0",
        "submit_login": ""
    }

    headers = {
        "content-Type": "application/x-www-form-urlencoded",
        "Host": "sdarot.tw",
        "Content-Length": str(len(data)),
        "Accept": "*/*",
        "Referer": home.BASE_URL + '/'
    }
    session.post(home.BASE_URL + LOGIN, data=data, headers=headers)


def get_token(sid, season, episode):
    """
    function that get correct token from the server
    :param sid: the show sid
    :param season: the chosen season
    :param episode: the chosen episode
    :return: the token
    """
    login()
    sdarot_cookie = session.cookies.values()[0]  # 0
    url = SDAROT_FULL_WATCH
    data = urlencode({
        "preWatch": False,
        "SID": sid,
        "season": season,
        "ep": episode
    })
    cookie = {
        'Sdarot': sdarot_cookie
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "sdarot.tw",
        "Content-Length": str(len(data)),
        "Accept": "/",
        "Referer": home.BASE_URL + '/'
    }

    resp = session.post(url, data=str(data), headers=headers, cookies=cookie)
    return resp.text


def request_episode(token, sid, season, episode):
    """
    function that send episode requests to the server
    :param token: the token
    :param sid: the show sid
    :param season: the chosen season
    :param episode: the chosen episode
    :return: the response from the server
    """
    sdarot_cookie = session.cookies.values()[0]
    data1 = {'watch': 'true', 'token': token, 'serie': sid, 'season': season, 'episode': episode,
             'type': 'episode'}
    cookie = {
        'Sdarot': sdarot_cookie}
    headers = {
        'authority': 'sdarot.tw',
        'origin': home.BASE_URL,
        'referer': home.BASE_URL + '/',
    }
    response = session.post(SDAROT_FULL_WATCH, cookies=cookie, headers=headers, data=data1)

    return response


def wait(response):
    """
    function that wait the needed time for the episode
    :param response: the response from the server with the time need to wait
    :return:
    """
    print((response.json()))
    time_to_wait = int((response.json())['error'].split(' ')[2])
    time.sleep(time_to_wait)


def download(url, series):
    """
    function that download the episode to downloads
    :param series: the series ( class: ShowDetails )
    :param url: the episode video
    :return: nothing
    """
    r = session.get(url, stream=True)
    file_name = get_file_name(series)
    download_to = get_basic_dir(series)
    full_dir = get_final_dir(download_to, file_name)
    if not os.path.exists(download_to):
        os.makedirs(download_to)
    with open(full_dir, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
    print('The episode has been successfully downloaded ! enjoy :)')
    session.close()


def get_file_name(series):
    """
    function that make the file name
    :param series: the series ( class: ShowDetails )
    :return: the file name
    """
    file_name = EPISODE + series.get_episode() + VIDEO_END
    return file_name


def get_basic_dir(series):
    """
    function that return the basic dir to download
    :param series: the series ( class: ShowDetails )
    :return: the dir
    """
    show_name_folder = series.get_english_name()
    show_season_folder = SEASON + series.get_season()
    basic_dir = f'{SDAROT_FILE}\{show_name_folder}\{show_season_folder}'  # set the file you want to download to
    return basic_dir


def get_final_dir(download_to, file_name):
    """

    :param download_to:
    :param file_name:
    :return:
    """
    full_dir = os.path.join(download_to, file_name)
    return full_dir

import os
import requests
from bs4 import BeautifulSoup
import show_info
import get_episodes

BASE_URL = 'https://sdarot.tw'
SDAROT_INDEX = '/ajax/index'
SHOWS_DICT_PARAM = {'srl': '1'}
ENGLISH_NAME = 'eng'
HEBREW_NAME = 'heb'
BASE_WATCH = '/watch/'
BASE_SEASON = '/season/'
ERROR = 'error'
BASE_START = 'https:'
EXIST_MESSAGE = 'The episode already exists, you can watch it in your folder, enjoy! :)'


def get_shows_dict():
    shows_dict = requests.get(f'{BASE_URL}{SDAROT_INDEX}', params=SHOWS_DICT_PARAM).json()
    return shows_dict


def find_show_id(show_name):
    shows_dict = get_shows_dict()
    show_id = ''
    for show in shows_dict:
        if show[HEBREW_NAME] == show_name or show[ENGLISH_NAME] == show_name:
            show_id = show['id']
    return show_id


def get_parse_show(show_id):
    show_html_details = requests.get(f'{BASE_URL}{BASE_WATCH}{show_id}')
    parse_show = BeautifulSoup(show_html_details.content, 'html.parser')
    return parse_show


def get_relevant_answer(parse_show):
    relevant_answer = parse_show.find('div', attrs={'class': 'content'})
    return relevant_answer


def get_series(relevant_answer, parse_show):
    """
    function that get series ( type : ShowDetails(ShowLink) )
    :param relevant_answer: the html answer for the show search
    :param parse_show: all the html text
    :return: series ( type : ShowDetails(ShowLink) )
    """
    series = show_info.set_movie(relevant_answer, parse_show)
    return series


def check_if_exist(series):
    episode_dir = get_episodes.get_final_dir(get_episodes.get_basic_dir(series), get_episodes.get_file_name(series))
    if os.path.exists(episode_dir):
        return True
    return False


def get_movie(relevant_answer, parse_show, series):
    """
    get the final url and send it to download
    :param series: series ( type : ShowDetails(ShowLink) )
    :param relevant_answer: the html answer for the show search
    :param parse_show: all the html text
    :return: nothing
    """
    token = get_episodes.get_token(series.get_sid(), series.get_season(), series.get_episode())
    final_response = get_server_response(token, series.get_sid(), series.get_season(), series.get_episode())
    if ERROR in final_response.json().keys():
        print(final_response.json()[ERROR])
        get_movie(relevant_answer, parse_show, series)
    else:
        url = find_video_url(final_response)
        get_episodes.download(url, series)


def get_server_response(token, sid, season, episode):
    """
    function that get the server final server response about the episode ( after the 30 seconds )
    :param token: the token
    :param sid: the show sid
    :param season: the chosen season
    :param episode: the chosen episode
    :return: the server final response about the episode ( after the 30 seconds )
    """
    response = get_episodes.request_episode(token, sid, season, episode)
    get_episodes.wait(response)
    final_response = get_episodes.request_episode(token, sid, season, episode)
    return final_response


def find_video_url(final_response):
    """
    function that find the video url
    :param final_response: the server final response about the episode ( after the 30 seconds )
    :return: the video url
    """
    episode_dict = final_response.json()
    sdarot_url = str(episode_dict['watch']).split("'")[3]
    url = BASE_START + sdarot_url
    return url


def main():
    show_name = input('Enter show name: ')
    show_id = find_show_id(show_name)
    while show_id == '':
        show_name = "The show does not exist or is written incorrectly.\nEnter show name: "
        show_id = find_show_id(show_name)
    parse_show = get_parse_show(show_id)
    relevant_answer = get_relevant_answer(parse_show)
    series = get_series(relevant_answer, parse_show)
    for episode in series.get_episodes_list():
        series.set_episode(episode)
        if not check_if_exist(series):
            get_movie(relevant_answer, parse_show, series)
        else:
            print(EXIST_MESSAGE)


if __name__ == '__main__':
    main()

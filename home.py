import os
import requests
from bs4 import BeautifulSoup
import get_episodes
import search_results
import show_search

BASE_SDAROT_URL = 'https://www.sdarot.buzz'
BASE_START = 'https:'
BASE_SEARCH = '/search?term='
SHOW_DOESNT_FOUND = 'לא נמצאו תוצאות חיפוש לביטוי ""'
BASE_WATCH = '/watch/'
BASE_SEASON = '/season/'
BASE_EPISODE = '/episode/'
ERROR = 'error'


def get_relevant_answer(html_answer):
    """
    function that find the relevant html from the answer
    :param html_answer: the answer
    :return: the relevant answer
    """
    relevant_answer = html_answer.find('div', attrs={'class': 'content'})
    return relevant_answer


def get_search_info(relevant_answer):
    """
    function that find the the result from the show search
    :param relevant_answer: relevant html from the answer
    :return: the result from the show search
    """
    search_info = relevant_answer.findAll('div', attrs={'class': 'sInfo text-center'})
    return search_info


def get_search_results(show_name):
    """
    search the show name
    :return: the pattern result from the search
    """
    show_server_answer = requests.get(BASE_SDAROT_URL + BASE_SEARCH + show_name)
    html_answer = BeautifulSoup(show_server_answer.content, 'html.parser')
    return html_answer


def check_if_one(search_info):
    """
    check if there is one result from search or more
    :param search_info: the result from the show search
    :return: True, if there is more than one result, False if the show doesnt exist or if there is one result
    """
    if search_info:
        return False
    else:
        return True


def check_if_exist(relevant_answer):
    """
    check if the show exist
    :param relevant_answer: the html answer for the show search
    :return: True, if the show exist, false if not
    """
    text_answer = relevant_answer.find('p').text
    if text_answer == SHOW_DOESNT_FOUND:
        return False
    else:
        return True


def find_show_pattern(search_info, relevant_answer):
    """
    function that find the pattern result from the search
    :param search_info: the result from the show search
    :param relevant_answer: the html answer for the show search
    :return: the pattern result from the search
    """
    show_link = BASE_SDAROT_URL + search_results.get_url(search_info, relevant_answer)
    show_server_answer = requests.get(show_link)
    new_html_answer = BeautifulSoup(show_server_answer.content, 'html.parser')
    return new_html_answer


def get_series(relevant_answer, html_answer):
    """
    function that get series ( type : ShowDetails(ShowLink) )
    :param relevant_answer: the html answer for the show search
    :param html_answer: all the html text
    :return: series ( type : ShowDetails(ShowLink) )
    """
    series = show_search.set_movie(relevant_answer, html_answer)
    return series


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


def get_movie(relevant_answer, html_answer, series):
    """
    get the final url and send it to download
    :param series: series ( type : ShowDetails(ShowLink) )
    :param relevant_answer: the html answer for the show search
    :param html_answer: all the html text
    :return: nothing
    """
    token = get_episodes.get_token(series.get_sid(), series.get_season(), series.get_episode())
    print(token)
    final_response = get_server_response(token, series.get_sid(), series.get_season(), series.get_episode())
    if ERROR in final_response.json().keys():
        print(final_response.json()[ERROR])
        get_movie(relevant_answer, html_answer, series)
    else:
        url = find_video_url(final_response)
        get_episodes.download(url, series)


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


def main_checker_sender(html_answer):
    """
    check if there is one result, if the show exist and if it is send to get movie
    :param html_answer: all the html text
    :return: False if the show doesnt found, else relevant answer and html text
    """
    relevant_answer = get_relevant_answer(html_answer)
    search_info = get_search_info(relevant_answer)
    is_one = check_if_one(search_info)
    if is_one:
        is_exist = check_if_exist(relevant_answer)
        if is_exist:
            return relevant_answer, html_answer
        else:
            print(SHOW_DOESNT_FOUND)
            main()
    else:
        new_html_answer = find_show_pattern(search_info, relevant_answer)
        new_relevant_answer = get_relevant_answer(new_html_answer)
        return new_relevant_answer, new_html_answer


def main():
    show_name = input('Enter the show name: ')
    html_answer = get_search_results(show_name)
    relevant_answer, html_answer = main_checker_sender(html_answer)
    series = get_series(relevant_answer, html_answer)
    if not series.get_episodes_list():
        episode_dir = get_episodes.get_final_dir(get_episodes.get_basic_dir(series), get_episodes.get_file_name(series))
        if os.path.exists(episode_dir):
            print('The episode already exists, you can watch it in your folder, enjoy! :)')
        else:
            get_movie(relevant_answer, html_answer, series)
    else:
        for episode in series.get_episodes_list():
            series.set_episode(episode)
            episode_dir = get_episodes.get_final_dir(get_episodes.get_basic_dir(series),
                                                     get_episodes.get_file_name(series))
            if os.path.exists(episode_dir):
                print('The episode already exists, you can watch it in your folder, enjoy! :)')
            else:
                get_movie(relevant_answer, html_answer, series)


if __name__ == '__main__':
    main()

    # testttttt

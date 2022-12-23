import re
import requests
from bs4 import BeautifulSoup
import classes
import home

EPISODES_RANGE = '3'
WHOLE_SEASON = '1'
ONE_EPISODE = '2'
SID = 'SID 			'
RATING = 'sRating 		'
NAME = 'Sname 			'


def find_detail_from_script(name, html_answer):
    """
    find the relevant value from javascript
    :param name: the value name
    :param html_answer: the html text
    :return: the value
    """
    string = f'var {name}= (.*?);$'
    pattern_value = re.compile(string, re.MULTILINE | re.DOTALL)
    script_value = html_answer.find("script", text=pattern_value)
    relevant_value = pattern_value.search(script_value.text).group(1)
    return relevant_value


def find_genre(html_answer):
    """
    find the genres of the show
    :param html_answer: the html text
    :return: the genres
    """
    html_genre = html_answer.find('section', attrs={'class': 'background rounded'}).find('h3').text
    genre = " ".join(html_genre.split())
    split_genre = genre.split(':')
    genre_value = split_genre[1]
    return genre_value


def find_seasons(html_answer):
    """
    find how many seasons there are in the show
    :param html_answer: the html text
    :return: the seasons number
    """
    html_seasons = html_answer.findAll('li')
    seasons = []
    for season in html_seasons:
        if season.get('data-season') is not None:
            seasons.append(season.get('data-season'))
    return seasons


def find_hebrew_english_name(name):
    """
    find the hebrew and the english name of show
    :param name: string: ["hebrew_name","english_name"]
    :return: the hebrew name and the english name of show
    """
    in_list = name[1:-1]
    split_names = in_list.split('"')
    hebrew_name = split_names[1]
    english_name = split_names[3]
    return hebrew_name, english_name


def set_details(relevant_answer, html_answer):
    """
    find and set the show relevant details in class
    :param relevant_answer: the relevant html text
    :param html_answer: all the html text
    :return: the series ( class: ShowDetails )
    """
    show_relevant_info = relevant_answer.findAll('div', attrs={'class': 'binfo transparent'})
    summary = relevant_answer.find('div', attrs={'class': 'col-lg-9 col-md-8 col-sm-7 col-xs-12'}).find('p').text
    year = relevant_answer.find('div', attrs={'id': 'year'}).find('span').text
    views = show_relevant_info[1].findAll('p')[1].text
    broadcast_network = show_relevant_info[2].find('a').text
    country = show_relevant_info[3].findAll('p')[1].text
    sid = find_detail_from_script(SID, html_answer)
    rating = find_detail_from_script(RATING, html_answer)
    names = find_detail_from_script(NAME, html_answer)
    hebrew_english_names = find_hebrew_english_name(names)
    hebrew_name = hebrew_english_names[0]
    english_name = hebrew_english_names[1]
    genre = find_genre(html_answer)
    seasons = find_seasons(html_answer)
    img = html_answer.find('img', attrs={'class': 'img-responsive img-rounded'}).get('src')
    link = home.BASE_SDAROT_URL + home.BASE_WATCH + sid
    series = classes.ShowDetails(hebrew_name, english_name, year, genre, img, link, summary, views, broadcast_network,
                                 country, sid, rating, seasons)
    return series


def season_or_episode():
    """
    input the client download choice
    :return: 1 - if the client choose to download whole season, 2 - if the client choose to download one episode
    """
    download_choice = input('click:\n1 - if you want to download all season\n2 - if you want to download specific '
                            'episode\n3 - if you want to download episodes range\n\nyour choice: ')
    return download_choice


def send_season(season, series):
    """
    send to sdarot.buzz new request with the season
    :param season: the chosen season
    :param series: the series info ( class  )
    :return: html info about the season and her episodes
    """
    season_response = requests.get(
        home.BASE_SDAROT_URL + home.BASE_WATCH + series.get_sid() + home.BASE_SEASON + season)
    html_season_answer = BeautifulSoup(season_response.content, 'html.parser')
    season_episodes_html = html_season_answer.findAll('li')
    return season_episodes_html


def choose_episode(season, series):
    """
    input episode from the client
    :param season: the chosen season
    :param series: the show info ( class )
    :return: the chosen episode
    """
    seasons_episode_html = send_season(season, series)
    episodes = find_episodes(seasons_episode_html)
    episodes_number = len(episodes)
    print('episodes: ', episodes, '\nepisodes number: ', episodes_number)
    episode = input('Choose episode: ')
    while episode not in episodes:
        episode = input('false, choose episode: ')
    series.set_episode(episode)
    return episode


def choose_episode_range(season, series):
    """
    input episode range from the client
    :param season: the chosen season
    :param series: the show info ( class )
    :return: list with all the episode that in the range
    """
    seasons_episodes_html = send_season(season, series)
    episodes = find_episodes(seasons_episodes_html)
    print('episodes: ', episodes, '\nepisodes number: ', len(episodes))
    start_episode = input('Choose start episode: ')
    while start_episode not in episodes:
        start_episode = input('false, choose start episode: ')
    last_episode = input('Choose last episode: ')
    while last_episode not in episodes or int(last_episode) < int(start_episode):
        last_episode = input('false, choose last episode: ')
    episodes_list = episodes[episodes.index(start_episode):episodes.index(last_episode) + 1]
    return episodes_list


def find_episodes(seasons_episode_html):
    """
    find the episodes the season have
    :param seasons_episode_html: the html info about the seasons
    :return: the episodes
    """

    episodes = []
    for episode in seasons_episode_html:
        if episode.get('data-episode') is not None:
            episodes.append(episode.get('data-episode'))
    return episodes


def choose_season(series):
    """
    input season from the client
    :param series: the show info ( class )
    :return: the chosen season
    """
    print_details(series)
    season = input('Choose season: ')
    while season not in series.get_seasons():
        season = input('False, choose season: ')
    return season


def print_details(series):
    """
    print the series details
    :param series: the series ShowDetails object
    :return: nothing
    """
    series.print_values()


def set_movie(relevant_answer, html_answer):
    """
    input season and episode ( only season if the client want to download all season ) and update in class
    :param relevant_answer:
    :param html_answer:
    :return:
    """
    series = set_details(relevant_answer, html_answer)
    season = choose_season(series)
    download_choice = season_or_episode()
    if download_choice == WHOLE_SEASON:
        series.set_season(season)
        series.set_episodes_list(find_episodes(send_season(season, series)))
    elif download_choice == ONE_EPISODE:
        episode = choose_episode(season, series)
        series.set_season(season)
        series.set_episode(episode)
    elif download_choice == EPISODES_RANGE:
        series.set_season(season)
        series.set_episodes_list(choose_episode_range(season, series))

    return series

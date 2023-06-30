BASE_SDAROT_URL = 'https://www.sdarot.buzz'
BASE_START = 'https:'
SEASON = '/season/'
EPISODE = '/episode/'


class BaseShow:
    def __init__(self, hebrew_name, english_name, year, genre, img):
        self.hebrew_name = hebrew_name
        self.english_name = english_name
        self.year = year
        self.genre = genre
        self.img = BASE_START + img

    def print_values(self):
        print('hebrew_name: ' + self.hebrew_name)
        print('english_name: ' + self.english_name)
        print('year: ' + self.year)
        print('genre: ' + self.genre)
        print('img: ' + self.img)

    def get_hebrew_name(self):
        return self.hebrew_name

    def get_english_name(self):
        return self.english_name

    def get_year(self):
        return self.year

    def get_genre(self):
        return self.genre

    def get_img(self):
        return self.img


class ShowLink(BaseShow):

    def __init__(self, hebrew_name, english_name, year, genre, img, link):
        super().__init__(hebrew_name, english_name, year, genre, img)
        self.link = link

    def print_values(self):
        BaseShow.print_values(self)
        print('link: ' + self.link)

    def get_link(self):
        return self.link


class ShowDetails(ShowLink):

    def __init__(self, hebrew_name, english_name, year, genre, img, link, summary, views, broadcast_network, country,
                 sid, rating, seasons):
        super().__init__(hebrew_name, english_name, year, genre, img, link)
        self.summary = 'summary: ' + summary
        self.views = 'views: ' + views
        self.broadcast_network = 'broadcast_network: ' + broadcast_network
        self.country = 'country: ' + country
        self.sid = sid
        self.rating = 'rating: ' + rating
        self.seasons = seasons
        self.seasons_number = seasons
        self.season_number = ''
        self.episode_number = ''
        self.episodes_list = []
        self.season_link = ''
        self.episode_link = ''

    def print_values(self):
        print(self.summary)
        ShowLink.print_values(self)
        print(self.views + '\n' + self.broadcast_network + '\n' + self.country + '\n' + self.rating + '\n' +
              'seasons: ', self.seasons, '\n')

    def get_summary(self):
        return self.summary

    def get_views(self):
        return self.views

    def get_broadcast_network(self):
        return self.broadcast_network

    def get_country(self):
        return self.country

    def get_sid(self):
        return self.sid

    def get_rating(self):
        return self.rating

    def get_seasons(self):
        return self.seasons

    def get_seasons_number(self):
        return self.seasons_number

    def set_episode(self, episode):
        self.episode_number = episode

    def set_season(self, season):
        self.season_number = season

    def get_episode(self):
        return self.episode_number

    def get_season(self):
        return self.season_number

    def set_episodes_list(self, episodes_list):
        self.episodes_list = episodes_list

    def get_episodes_list(self):
        return self.episodes_list

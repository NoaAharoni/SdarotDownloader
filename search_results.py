import classes

SERIES_LINK_START = 'href'
IMAGE_LINK_START = 'src'


def find_links(relevant_answer, link_type):
    """
    find the series link or the image link of every show of the results
    :param link_type: the type of the link : href for series link, src for image link
    :param relevant_answer: the html relevant answer
    :return: all the series links or the images links
    """
    links_list = []
    for link in relevant_answer():
        if link.get(link_type) is not None:
            links_list.append(link.get(link_type))  # href or src
    return links_list


def set_in_class(search_info, link_list, img_list):
    """
    set the relevant parameters in class
    :param search_info: the html with all the shows result
    :param link_list: all the shows links
    :param img_list: all the show images
    :return: dict with ShowLink values, the key is in order of the result
    """
    counter = 0
    shows_dict = {}
    for show in search_info:
        hebrew = show.h4.string
        english = show.h5.string
        year = show.find('p').text
        genre = show.findAll('p')[1].text
        link = link_list[counter]
        img = img_list[counter]
        series = classes.ShowLink(hebrew, english, year, genre, img, link)
        shows_dict[counter] = series
        counter += 1
    return shows_dict


def print_all_shows(shows_dict):
    """
    print all the details about the show
    :param shows_dict: dict with ShowLink values, the key is in order of the result
    :return: nothing
    """
    counter = 0
    for i in range(len(shows_dict)):
        print(i + 1, '.')
        shows_dict[i].print_values()
        counter += 1


def choose_show(show_dict):
    """
    input the show that the client enter and find her link
    :param show_dict: dict with ShowLink values, the key is in order of the result
    :return: the show url
    """
    print_all_shows(show_dict)
    show_number = int(input('choose the number of the show that you want: '))
    show_link = show_dict[show_number - 1].get_link()
    return show_link


def get_url(search_info, relevant_answer):
    """
    find the show url
    :param search_info: the html with all the shows result
    :param relevant_answer: the html relevant answer
    :return: the show url
    """
    link_list = find_links(relevant_answer, SERIES_LINK_START)
    img_list = find_links(relevant_answer, IMAGE_LINK_START)
    show_dict = set_in_class(search_info, link_list, img_list)
    show_url = choose_show(show_dict)
    return show_url

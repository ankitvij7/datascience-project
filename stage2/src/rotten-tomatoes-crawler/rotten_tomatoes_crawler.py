import bs4 as bs


def extract_info(movie_html):
    movie_soup = bs.BeautifulSoup(movie_html, 'html.parser')
    movie_info = {}
    movie_info["Title: "] = movie_soup.find('h1', class_='title').text.strip(' \t\n\r')
    movie_info["TomatoMeter: "] = movie_soup.find('span', class_='meter-value superPageFontColor').find('span').text
    movie_info["Audience Score: "] = movie_soup.find('div', class_='meter media').find('span', class_='superPageFontColor').text

    movie_attributes = movie_soup.find_all('li', class_='meta-row clearfix');
    for movie_attribute in movie_attributes:
        info_type = movie_attribute.find('div', class_='meta-label').text
        info_value = movie_attribute.find('div', class_='meta-value')
        if info_type == "Genre: " or info_type == "Directed By: " or info_type == "Written By: " or info_type == "Studio: ":
            values = []
            sub_info_values = info_value.find_all('a');
            for sub_value in sub_info_values:
                values.append(sub_value.text.strip(' \t\n\r'))
            info_value = ''.join(values)
        else:
            info_value = info_value.text

        movie_info[info_type] = info_value.strip(' \t\n\r')

    complete_movie_info = ""
    for key, value in movie_info.items():
        complete_movie_info = complete_movie_info + key + value + ", "

    print("RESULT IS HERE- " + complete_movie_info)

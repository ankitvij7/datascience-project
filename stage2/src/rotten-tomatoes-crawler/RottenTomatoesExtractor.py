import bs4 as bs


def extract_info(movie_html, output, movie_url):
    movie_soup = bs.BeautifulSoup(movie_html, 'html.parser')
    movie_info = dict()
    title = movie_soup.find('h1', class_='title')
    movie_info["Title: "] = "NA" if title is None else title.text.strip(' \t\n\r')
    tomato_meter = movie_soup.find('span', class_='meter-value superPageFontColor')
    movie_info["TomatoMeter: "] = "NA" if tomato_meter is None else tomato_meter.find('span').text
    audience_score = movie_soup.find('div', class_='meter media')
    movie_info["Audience Score: "] = "NA";
    if audience_score is not None:
        audience_score = audience_score.find('span', class_='superPageFontColor')
        movie_info["Audience Score: "] = audience_score.text if audience_score is not None else "NA"

    movie_attributes = movie_soup.find_all('li', class_='meta-row clearfix')
    for movie_attribute in movie_attributes:
        info_type = movie_attribute.find('div', class_='meta-label').text
        info_value = movie_attribute.find('div', class_='meta-value')
        if info_type == "Genre: " or info_type == "Directed By: " or info_type == "Written By: " or info_type == "Studio: ":
            values = []
            sub_info_values = info_value.find_all('a')
            for sub_value in sub_info_values:
                values.append(sub_value.text.strip(' \t\n\r'))
            info_value = ';'.join(values)
        else:
            info_value = info_value.text

        movie_info[info_type] = info_value.strip(' \t\n\r')

    in_theaters = movie_soup.find('li', class_='meta-row clearfix js-theater-release-dates')
    if in_theaters is not None:
        in_theaters = "NA" if in_theaters.find('time') is None else in_theaters.find('time').text
    else:
        in_theaters = 'NA'

    output.writerow({'Url': movie_url,
                     'Title': 'NA' if "Title: " not in movie_info else movie_info["Title: "],
                     'Score': 'NA' if "TomatoMeter: " not in movie_info else movie_info["TomatoMeter: "],
                     'Rating': 'NA' if "Rating: " not in movie_info else movie_info["Rating: "],
                     'Genre': 'NA' if "Genre: " not in movie_info else movie_info["Genre: "],
                     'Directed By': 'NA' if "Directed By: " not in movie_info else movie_info["Directed By: "],
                     'Written By': 'NA' if "Written By: " not in movie_info else movie_info["Written By: "],
                     'Box Office': 'NA' if "Box Office: " not in movie_info else movie_info["Box Office: "],
                     'Release Date': in_theaters,
                     'Runtime': 'NA' if "Runtime: " not in movie_info else movie_info["Runtime: "],
                     'Studio': 'NA' if "Studio: " not in movie_info else movie_info["Studio: "],
                     'Audience Score': 'NA' if "Audience Score: " not in movie_info else movie_info[
                         "Audience Score: "]})

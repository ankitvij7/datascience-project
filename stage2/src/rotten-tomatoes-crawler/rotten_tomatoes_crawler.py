import bs4 as bs


def extract_info(movie_html, output, movie_url):
    movie_soup = bs.BeautifulSoup(movie_html, 'html.parser')
    movie_info = dict()
    title = movie_soup.find('h1', class_='title')
    movie_info["Title: "] = "NA" if title is None else title.text.strip(' \t\n\r')
    movie_info["TomatoMeter: "] = movie_soup.find('span', class_='meter-value superPageFontColor').find('span').text
    audience_score = movie_soup.find('div', class_='meter media')
    movie_info["Audience Score: "] = "NA";
    if audience_score is not None:
        audience_score = audience_score.find('span', class_='superPageFontColor')
        movie_info["Audience Score: "] = audience_score.text if audience_score is not None else "NA"

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

    # complete_movie_info = ""
    # for key, value in movie_info.items():
    #     complete_movie_info = complete_movie_info + key + value + ", "

    output.writerow({'Title': 'NA' if "Title: " not in movie_info else movie_info["Title: "],
                     'TomatoMeter': 'NA' if "TomatoMeter: " not in movie_info else movie_info["TomatoMeter: "],
                     'Audience Score': 'NA' if "Audience Score: " not in movie_info else movie_info["Audience Score: "],
                     'Rating': 'NA' if "Rating: " not in movie_info else movie_info["Rating: "],
                     'Genre': 'NA' if "Genre: " not in movie_info else movie_info["Genre: "],
                     'Directed By': 'NA' if "Directed By: " not in movie_info else movie_info["Directed By: "],
                     'Written By': 'NA' if "Written By: " not in movie_info else movie_info["Written By: "],
                     'On Disc/Streaming': movie_info["On Disc/Streaming: "],
                     'Box Office': 'NA' if "Box Office: " not in movie_info else movie_info["Box Office: "],
                     'Runtime': 'NA' if "Runtime: " not in movie_info else movie_info["Runtime: "],
                     'Studio': 'NA' if "Studio: " not in movie_info else movie_info["Studio: "],
                     'Movie Url': movie_url})
    # print("RESULT IS HERE- " + complete_movie_info)

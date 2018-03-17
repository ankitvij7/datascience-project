import bs4 as bs
import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl


class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def extract_info(url):
    movie_page = Page(url)
    movie_soup = bs.BeautifulSoup(movie_page.html, 'html.parser')
    movie_info = {}
    movie_info["Title: "] = movie_soup.find('h1', class_='title').text.strip(' \t\n\r')
    movie_info["TomatoMeter: "] = movie_soup.find('span', class_='meter-value superPageFontColor').find('span').text
    movie_info["Audience Score: "] = movie_soup.find('div', class_='meter media').find('span',
                                                                                       class_='superPageFontColor').text
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
    del movie_page

    print("RESULT IS HERE- " + complete_movie_info)

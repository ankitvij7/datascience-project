import bs4 as bs
import sys
# import copy
from PyQt5.QtWebEngineWidgets import QWebEnginePage
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import (pyqtSignal, QThread)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from rotten_tomatoes_crawler import extract_info
import requests
import csv


class Page(QWebEnginePage):
    def __init__(self, url, appl):
        self.app = appl
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        # print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def get_list(url, appl, output):
    movies = requests.get(url).json()["results"]
    # page = Page(url, appl)
    # %soup = bs.BeautifulSoup(page.html, 'html.parser')
    # movies = soup.find_all('div', class_='movie_info')

    # print("NUMBER OF MOVIES IS - : " + str(len(movies)))
    for movie in movies:
        movie_url = "https://www.rottentomatoes.com" + movie["url"]
        movie_page = Page(movie_url, appl)
        extract_info(movie_page.html, output)


fieldnames = ['Title', 'TomatoMeter', 'Audience Score', 'Rating', 'Genre',
              'Directed By', 'Written By', 'On Disc/Streaming', 'Box Office', 'Runtime',
              'Studio']

output = csv.DictWriter(open("RottenTomatoesMovieDatabase", "w"), fieldnames=fieldnames)
output.writeheader()
myApp = QApplication(sys.argv)
count = 1;
while count < 95:
    request_url = "https://www.rottentomatoes.com/api/private/v2.0/browse?maxTomato=100&maxPopcorn=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified=false&sortBy=release&type=dvd-streaming-all&page=" + str(
        count)
    get_list(request_url, myApp, output)
    count = count + 1

# print('one done')
# get_list('https://www.rottentomatoes.com/browse/dvd-streaming-new', myApp)
# print('two done')

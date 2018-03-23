import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from RottenTomatoesExtractor import extract_info
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

    for movie in movies:
        movie_url = "https://www.rottentomatoes.com" + movie["url"]
        movie_page = Page(movie_url, appl)
        extract_info(movie_page.html, output, movie_url)


fieldnames = ['Url', 'Title', 'Score', 'Rating', 'Genre',
              'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime',
              'Studio', 'Audience Score']

output = csv.DictWriter(open("RottenTomatoesMovieDatabase.raw", "a"), fieldnames=fieldnames)
#output.writeheader()
myApp = QApplication(sys.argv)
#count = 1
count = 49
while count < 96:
    print("SERVING CURRENT PAGE WITH NUMBER: " + str(count))
    request_url = "https://www.rottentomatoes.com/api/private/v2.0/browse?maxTomato=100&maxPopcorn=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified=false&sortBy=release&type=dvd-streaming-all&page=" + str(
        count)
    get_list(request_url, myApp, output)
    count = count + 1

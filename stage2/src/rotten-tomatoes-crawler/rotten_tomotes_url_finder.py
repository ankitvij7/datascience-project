import bs4 as bs
import sys
# import copy
from PyQt5.QtWebEngineWidgets import QWebEnginePage
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import (pyqtSignal, QThread)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from rotten_tomatoes_crawler import extract_info


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
        #print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def get_list(url, appl):
    page = Page(url, appl)
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    movies = soup.find_all('div', class_='movie_info')

    print("NUMBER OF MOVIES IS - : " + str(len(movies)))
    for movie in movies:
        movie_url = "https://www.rottentomatoes.com" + movie.find('a', href=True)['href']
        #print(movie_url)
        movie_page = Page(movie_url, appl)
        extract_info(movie_page.html)


myApp = QApplication(sys.argv)
get_list('https://www.rottentomatoes.com/browse/top-dvd-streaming', myApp)
print('one done')
get_list('https://www.rottentomatoes.com/browse/dvd-streaming-new', myApp)
print('two done')

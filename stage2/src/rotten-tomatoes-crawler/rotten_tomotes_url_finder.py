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
        print('lock')
        QWebEnginePage.__init__(self)
        print('unlock')
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


def get_list(url, appl):
    page = Page(url, appl)
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    movies = soup.find_all('div', class_='movie_info')

    print("NUMBER OF MOVIES IS - : " + str(len(movies)))
    for movie in movies:
        movie_url = "https://www.rottentomatoes.com" + movie.find('a', href=True)['href']
        print(movie_url)
        movie_page = Page(movie_url, appl)
        extract_info(movie_page.html)


myApp = QApplication(sys.argv)
get_list('https://www.rottentomatoes.com/browse/top-dvd-streaming', myApp)
print('one done')
get_list('https://www.rottentomatoes.com/browse/dvd-streaming-new', myApp)
print('two done')


#Old crap to be delete shortly...
# def render_to_html(url):
#     import sys
#     import copy
#     from PyQt5.QtWebEngineWidgets import QWebEnginePage
#     from PyQt5.QtWidgets import QApplication
#     from PyQt5.QtCore import QUrl
#
#     class Pager(QWebEnginePage):
#         def __init__(self, pager_url):
#             print('Starting Up')
#             self.app = QApplication(sys.argv)
#             print('SU2')
#             QWebEnginePage.__init__(self)
#             print('SU3')
#             self.html = ''
#             self.loadFinished.connect(self._on_load_finished)
#             print('SU4')
#             self.load(QUrl(pager_url))
#             print('Executing')
#             self.app.exec_()
#             print('Executing2')
#
#         def __exit__(self, exc_type, exc_value, traceback):
#             print('exit')
#             del self.app
#
#         def _on_load_finished(self):
#             self.html = self.toHtml(self.Callable)
#             print('Load finished')
#
#         def Callable(self, html_str):
#             self.html = html_str
#             print('Quiting')
#             self.app.quit()
#             #self.app.exit()
#
#     pager = Pager(url)
#     ret_string = copy.copy(pager.html)
#     del pager
#     return ret_string
#
#
# class Pager(QWebEnginePage):
#     finished = pyqtSignal()
#
#     def __init__(self):
#         QWebEnginePage.__init__(self)
#         self.html = ''
#         print('load')
#         self.loadFinished.connect(self._on_load_finished)
#
#     def load_it(self, url):
#         self.load(QUrl(url))
#         print('load3 ' + url)
#
#     def _on_load_finished(self):
#         print('loaded')
#         self.html = self.toHtml(self.Callable)
#         # self.html_str = self.page().toHtml(self.Callable)
#         # self.page().toHtml(self.Callable)
#         print('Emitting')
#         self.finished.emit()
#
#     def Callable(self, html_str):
#         self.html = html_str
#         print('Emitting')
#
#
# def got_page():
#     print(pager.html)
#     page_html = copy.copy(pager.html)
#     soup = bs.BeautifulSoup(page_html, 'html.parser')
#     movies = soup.find_all('div', class_='movie_info')
#     print("NUMBER OF MOVIES IS - : " + str(len(movies)))
#     for movie in movies:
#         movie_url = "https://www.rottentomatoes.com" + movie.find('a', href=True)['href']
#         print(movie_url)
#         # movie_
#         # extract_info(movie_url)
#     app.quit()
#
#
# app = QApplication(sys.argv)
# print("startup")
# thread = QThread()
# print("su1")
# pager = Pager()
# print("su2")
# pager.moveToThread(thread)
# print("su3")
# pager.finished.connect(got_page)
# print("su4")
# # when signal is done execute this.
# #thread.finished.connect(app.exit)
# thread.start()
# pager.load_it('https://www.rottentomatoes.com/browse/top-dvd-streaming')
# print("su5")
# sys.exit(app.exec_())

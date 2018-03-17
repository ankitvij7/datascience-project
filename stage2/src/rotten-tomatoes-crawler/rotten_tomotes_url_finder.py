import bs4 as bs
import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from rotten_tomatoes_crawler import extract_info


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


page = Page('https://www.rottentomatoes.com/browse/top-dvd-streaming')
soup = bs.BeautifulSoup(page.html, 'html.parser')
movies = soup.find_all('div', class_='movie_info')
print("NUMBER OF MOVIES IS - : " + str(len(movies)))
for movie in movies:
    movie_url = "https://www.rottentomatoes.com" + movie.find('a', href=True)['href']
    extract_info(movie_url)

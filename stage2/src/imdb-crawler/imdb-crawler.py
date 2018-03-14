from bs4 import BeautifulSoup
import requests

page = requests.get('http://www.imdb.com/title/tt1365519/?ref_=inth_ov_tt')
soup = BeautifulSoup(page.text, 'html.parser')
print(soup.prettify())


from core import Scraper, Translator

scraper = Scraper('https://fdfb354e0.bi27.cc/')

soup = scraper.cook_soup('https://fdfb354e0.bi27.cc/read/169736/1.html')

content = soup.find_all('div', id='chaptercontent')
texts = "\n".join([i.text for i in content])

translator = Translator()

print(translator.translate(texts))

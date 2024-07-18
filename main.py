from core import Scraper, Translator, Bookbinder
import re

scraper = Scraper('https://fdfb354e0.bi27.cc/')
translator = Translator()
binder = Bookbinder()

url = "https://fdfb354e0.bi27.cc/read/169736/154.html"

for i in range (1, 215):
    print(f'Adding Chapter {i}/214')
    soup = scraper.cook_soup(f'https://fdfb354e0.bi27.cc/read/169736/{i}.html')
    html = soup.find_all('div', id='chaptercontent')
    title = soup.find('span', class_='title')

    content = "\n\n".join([title.text[2:], str(html[0])])

    translated = translator.translate(content)
    chap_title = translated.splitlines()[0]
    chap_content = "".join(["<p>" + i.lstrip() + "</p>" for i in translated.splitlines()[1:]])

    binder.add_chapter(chap_title, chap_content)

print('Creating epub...')
binder.create_book(title='Immortality Cultivate I Farm in the System space', source_url='https://fdfb354e0.bi27.cc/read/169736/', authors=['Light Salted Fish'])
print('Created epub!')

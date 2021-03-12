from datetime import datetime
from lxml import html
import requests
import sys
import os


if __name__ == '__main__':
	BASE_DIR = os.path.dirname(os.path.realpath(__file__))
	if sys.platform == 'win32':
		BASE_DIR += f'\\data_{datetime.today().strftime("%d.%m.%Y_%H:%M:%S")}\\'
		FILENAME = '\\{}.txt'
	else:
		BASE_DIR += f'/data_{datetime.today().strftime("%d.%m.%Y_%H:%M:%S")}/'
		FILENAME = '/{}.txt'

	os.mkdir(BASE_DIR)

	links = {
		'positive': 'https://www.kinopoisk.ru/reviews/type/comment/status/good/period/month/page/{}/',
		'neutral': 'https://www.kinopoisk.ru/reviews/type/comment/status/neutral/period/month/page/{}/',
		'negative': 'https://www.kinopoisk.ru/reviews/type/comment/status/bad/period/month/page/{}/'
	}

	for link in links:
		file = 0
		pagenum = 1
		os.mkdir(BASE_DIR + link)
		while True:
			print(f'{link} {pagenum} страницу')
			page = requests.get(links[link].format(pagenum))
			if page.status_code == 404:
				break
			tree = html.fromstring(page.content)
			reviews = tree.xpath('//span[@class="_reachbanner_"]')
			for review in reviews:
				if review.text is not None:
					with open(BASE_DIR + link + FILENAME.format(file), 'w', encoding='utf=8') as f:
						f.write(review.text)
					file += 1
			pagenum += 1
		print()

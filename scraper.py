from datetime import datetime
import time
import urlparse

import requests
import bs4

base_url = 'http://www.tulibrodevisitas.com/libro.php?id=11014'

class Post:
	def __init__(self):
		self.username = ''
		self.stateToOrFrom =  ''
		self.genre = ''
		self.website = ''
		self.email = ''
		self.publicationDate = ''
		self.message = ''

class Scraper(object):

	def doRequest(self, url):
		return requests.get(url)

	def getSoup(self, url):

		# return bs4.BeautifulSoup(open("posts.html", "r").read())	
		response = self.doRequest(url)
		return bs4.BeautifulSoup(response.text)

	def getPages(self):

		soup = self.getSoup(base_url)

		pages = []

		for a in soup.find_all('a', title=""):
			href = a['href']
			url = urlparse.urlparse(href)
			params = urlparse.parse_qs(url.query)
			if 'paginacion' in params:
				pages.append(params['paginacion'][0])

		return self.distinct(pages)

	def distinct(self, seq, idfun=None): 
	   # order preserving
	   # Taken from: http://www.peterbe.com/plog/uniqifiers-benchmark
	   if idfun is None:
	       def idfun(x): return x
	   seen = {}
	   result = []
	   for item in seq:
	       marker = idfun(item)
	       # in old Python versions:
	       # if seen.has_key(marker)
	       # but in new ones:
	       if marker in seen: continue
	       seen[marker] = 1
	       result.append(item)
	   return result

	def scrapePage(self, page = -1):
		"""If not page specified, the function will scrape the last page, ordered by publication date in a descendent order"""

		posts = []
		soup = None

		if type(page) is int  and page < 0:
			soup = self.getSoup(base_url)
			posts = self.scrape(soup)
		elif type(page) is int  and page > 0:
			soup = self.getSoup(base_url + '&paginacion=' + str(page))
			posts = self.scrape(soup)
		elif type(page) is list:
			for page_ in page:
				soup = self.getSoup(base_url + '&paginacion=' + str(page_))
				tempPosts = self.scrape(soup)
				posts.extend(tempPosts)
		else:
			pages = self.getPages()
			for page_ in pages:
				soup = self.getSoup(base_url + '&paginacion=' + str(page_))
				tempPosts = self.scrape(soup)
				posts.extend(tempPosts)
		
		return posts

	def scrape(self, soup):
		posts = []
		for trs in soup.find_all('tr', bgcolor = ['#CCCCCC', '#FFFFFF']):

				post = Post()

				for span in trs.find_all('span', class_ = 'Mensaje'):

						msg = span.find_all()
						if len(msg) == 0:
							post.message = span.text.strip().replace('\n', ' ').replace('\r', '')

						for strong in span.find_all('strong'):
												
							img_genre = strong.find_all('img')
							if len(img_genre) > 0:

								# Get the genre of the post owner
								if img_genre[0]['src'] == 'Images/libro_mujer.gif':
									post.genre = 'f'
								elif img_genre[0]['src'] == 'Images/libro_hombre.gif':
									post.genre = 'm'
								else:
									post.genre = 'u'
								
								for img in img_genre:

									# Get the website
									if img['src'] == 'Images/libro_web.gif':
										post.website = img.parent['href']

									# Get the email
									if img['src'] == 'Images/libro_mail.gif':
										post.email = img.parent['href'].replace('mailto:','').strip().lower()

							# Get the title of the publication
							if len(strong) != 1:
								lines = strong.text.strip().split('-')
								if len(lines) > 1:
									post.username = lines[0].strip().upper()
									post.stateToOrFrom = lines[1].strip().upper()
								else:
									post.username = strong.text.strip()
							else:
								tempPublicationDate = strong.text.replace('de','', 1).replace('del','')
								# tempTimeAndDate = tempPublicationDate.strip().split('-')
								# post.publicationDate = time.strptime(str(tempTimeAndDate[0]).lower() + str(tempTimeAndDate[1]).replace(':',' ') , "%d %B %Y %H %M %S")

								post.publicationDate = tempPublicationDate


				posts.append(post);
		return posts

	def getAllPosts(self):
		return self.scrapePage(0)

	def getLastPosts(self):
		return self.scrapePage()

	def searchByMessage(self, searchCriteria):

		posts = []

		tempPosts = self.scrapePage(0)
		for post in tempPosts:
			if searchCriteria.lower() in post.message.lower():
				posts.append(post)

		return posts

	def searchByState(self, searchCriteria):
		posts = []

		tempPosts = self.scrapePage()
		for post in tempPosts:
			if searchCriteria.lower() in post.stateToOrFrom.lower():
				posts.append(post)

		return posts
import requests
import bs4
import urlparse
from datetime import datetime

class Post:
	def __init__(self):
		self.username = ''
		self.stateToOrFrom =  ''
		self.genre = ''
		self.website = ''
		self.email = ''
		self.publicationDate = ''
		self.message = ''

base_url = 'http://www.tulibrodevisitas.com/libro.php?id=11014'

def doRequest(url):
	return requests.get(url)

def getSoup(url):
	response = doRequest(url)
	return bs4.BeautifulSoup(response.text)

def getPages():

	soup = getSoup(base_url)

	pages = []

	for a in soup.find_all('a', title=""):
		href = a['href']
		url = urlparse.urlparse(href)
		params = urlparse.parse_qs(url.query)
		if 'paginacion' in params:
			pages.append(params['paginacion'][0])

	return distinct(pages)

def distinct(seq, idfun=None): 
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

def scrape(page = -1):
	"""If not page specified, the function will scrape the last page, ordered by publication date in a descendent order"""

	posts = []
	soup = None

	if page < 0:
		print 'get index'
		soup = getSoup(base_url)
		posts = scrapePage(soup)
	elif page > 0:
		print 'get page ' + str(page)
		soup = getSoup(base_url + '&paginacion=' + str(page))
		posts = scrapePage(soup)
	else:
		pages = getPages()
		for page_ in pages:
			soup = getSoup(base_url + '&paginacion=' + str(page_))
			tempPosts = scrapePage(soup)
			posts.extend(tempPosts)

	f = open('post.txt','w')
	for post in posts:
		f.write(('USERNAME: ' + post.username + ', ' + 'STATETOORFROM: ' + post.stateToOrFrom + ', ' + 'GENRE: ' + post.genre + ', ' + 'WEBSITE: ' + post.website + ', ' + 'EMAIL: ' + post.email + ', ' + 'PUBLICATIONDATE: ' + post.publicationDate + ', ' + 'MESSAGE: ' + post.message + '\n').encode("utf-8"))
	f.close()

def scrapePage(soup):
	posts = []
	for trs in soup.find_all('tr', bgcolor = ['#CCCCCC', '#FFFFFF']):
		
			post = Post()

			for span in trs.find_all('span'):
				if span.has_attr('class') and str(span['class'] == 'Mensaje'):

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
							post.publicationDate = strong.text

			posts.append(post);
	return posts

print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
scrape()
print datetime.now().strftime('%Y-%m-%d %H:%M:%S')



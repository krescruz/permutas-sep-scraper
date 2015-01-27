import requests
import bs4
import urlparse

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
response = None

def doRequest():
	global response
	response = requests.get(base_url)

def getSoup():
	if response is None:
		doRequest()
	return bs4.BeautifulSoup(response.text)

def getPages():
	soup = getSoup()

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

def scrape(page = 0):
	"If not page specified, the function will scrape the last page, ordered by publication date in a descendent order"

	
	posts = []

	if page > 0:
		base_url = base_url + '&paginacion=' + str(page)

	soup = getSoup()		

	for trs in soup.find_all('tr'):

		if trs.has_attr('bgcolor') and (str(trs['bgcolor']) == '#CCCCCC' or str(trs['bgcolor']) == '#FFFFFF'):

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
	# for post in posts:
	# 	print 'USERNAME: ' + post.username + ', ' + 'STATETOORFROM: ' + post.stateToOrFrom + ', ' + 'GENRE: ' + post.genre + ', ' + 'WEBSITE: ' + post.website + ', ' + 'EMAIL: ' + post.email + ', ' + 'PUBLICATIONDATE: ' + post.publicationDate + ', ' + 'MESSAGE: ' + post.message

print getPages()
print len(getPages())





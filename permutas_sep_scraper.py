import requests
import bs4

# response = requests.get('http://pyvideo.org/category/50/pycon-us-2014')
# soup = bs4.BeautifulSoup(response.text)
# links = soup.select('div.video-summary-data a[href^=/video]')

response = requests.get('http://www.tulibrodevisitas.com/libro.php?id=11014')
soup = bs4.BeautifulSoup(response.text)


posts = []
class Post:
	def __init__(self):
		self.username = ''
		self.stateToOrFrom =  ''
		self.genre = ''
		self.website = ''
		self.email = ''
		self.publicationDate = ''
		self.message = ''

counter = 0
for trs in soup.find_all('tr'):

	if trs.has_attr('bgcolor') and (str(trs['bgcolor']) == '#CCCCCC' or str(trs['bgcolor']) == '#FFFFFF'):
		
		counter = counter + 1
		print counter

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

for post in posts:
	print 'USERNAME: ' + post.username + ', ' + 'STATETOORFROM: ' + post.stateToOrFrom + ', ' + 'GENRE: ' + post.genre + ', ' + 'WEBSITE: ' + post.website + ', ' + 'EMAIL: ' + post.email + ', ' + 'PUBLICATIONDATE: ' + post.publicationDate + ', ' + 'MESSAGE: ' + post.message
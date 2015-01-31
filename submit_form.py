from PIL import Image
from StringIO import StringIO
from datetime import datetime
import requests
import bs4
import urllib2
import urllib
import cookielib
import sys

# Add a functionality to let the user only to enter the captha value

urlPost = 'http://www.tulibrodevisitas.com/accion_firma.php?accion=nueva'
urlForm = 'http://www.tulibrodevisitas.com/mensaje.php?id=11014'
urlImg = 'http://www.tulibrodevisitas.com/config/imagen_registro.php'

class Poster(object):

	def doPost(self, cookie, captcha, data = []):

		'''
			The following data was used for testing purposes.
			data = {
				'nombre':'yourname',
				'web':'www.example.com',
				'mail':'email@example.com',
				'sexo':'mujer', # 'mujer' | 'hombre' are the valid options
				'lugar':'yourCity',
				'mensaje':'yourMessage',
				'img': captcha,
				'id_libro':'11014'
			}			

		'''
		cookies = {
			'PHPSESSID': cookie
		}

		r = requests.post(urlPost, data = data, cookies=cookies)

	def getCookie(self):

	    # Create the first request for the form:
	    r = requests.get(urlForm)
	    cookie = str(r.cookies.get('PHPSESSID'))

	    # Create the second request for the captcha image
	    imgRequest = requests.get(urlImg, cookies = r.cookies)

	    # Save the image locally
	    i = Image.open(StringIO(imgRequest.content))
	    i.save(str(datetime.now().second) + str(datetime.now().microsecond) + ".png", "PNG")

	    return cookie


def main():
	cookie = getCookie()
	captcha = raw_input("Enter captcha: ")
	doPost(cookie, captcha)

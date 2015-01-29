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


def doPost(coookie_value, captcha):
	data = {
		'nombre':'Jose Hernandez',
		'web':'',
		'mail':'jose.hernandez@gmail.com',
		'sexo':'hombre',
		'lugar':'Nuevo Leon',
		'mensaje':'Hola,+soy+del+estado+de+Veracruz,+busco+moverme+a+Monterrey, Nuevo Leon.',
		'img': captcha,
		'id_libro':'11014'
	}
	
	cookie = {
		'PHPSESSID': coookie_value
	}

	r = requests.post(urlPost, data = data, cookies=cookie)
	print coookie_value
	print captcha

def getCookie():
    # Create the first request for the form:
    r = requests.get(urlForm)
    
    f = open('./cookies/' + str(r.cookies.get('PHPSESSID')) + '.txt','w')
    f.close()

    # Create the second request for the captcha image
    imgRequest = requests.get(urlImg, cookies = r.cookies)

    # Save the image locally
    i = Image.open(StringIO(imgRequest.content))
    i.save('./cookies/' + str(datetime.now().second) + str(datetime.now().microsecond) + ".png", "PNG")


if len(sys.argv) == 1:
	getCookie()

if len(sys.argv) == 3:
	doPost(sys.argv[1], sys.argv[2])
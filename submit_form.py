import requests
import bs4
import urllib2
import urllib
import cookielib
from PIL import Image
from StringIO import StringIO
from datetime import datetime

url = 'http://www.tulibrodevisitas.com/mensaje.php?id=11014'
imgUrl = 'http://www.tulibrodevisitas.com/config/imagen_registro.php'

for i in range(4):
    # Create the first request for the form:
    r = requests.get(url)

    # Create the second request for the captcha image
    imgRequest = requests.get(imgUrl, cookies = r.cookies)

    # Save the image locally
    i = Image.open(StringIO(imgRequest.content))
    i.save(str(datetime.now().second) + str(datetime.now().microsecond) + ".png", "PNG")
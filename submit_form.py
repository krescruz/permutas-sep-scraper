import requests
import bs4
import urllib2
import urllib
import cookielib
from PIL import Image
from StringIO import StringIO

url = 'http://www.tulibrodevisitas.com/mensaje.php?id=11014'
imgUrl = 'http://www.tulibrodevisitas.com/config/imagen_registro.php'

# Create the first request for the form:
r = requests.get(url)

# Create the second request for the captcha image
imgRequest = requests.get(imgUrl, cookies = r.cookies)

# Save the image locally
i = Image.open(StringIO(imgRequest.content))
i.save("img.png", "PNG")


for i in range(3):
    f = open('IMG' + str(i) + '.jpg','wb')
    url = 'http://www.tulibrodevisitas.com/config/imagen_registro.php'
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0' }
    cj = cookielib.LWPCookieJar()
    authinfo = urllib2.HTTPBasicAuthHandler()
    realm="realmName"
    username="userName"
    password="passWord"
    host="www.wherever.com"
    authinfo.add_password(realm, host, username, password)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), authinfo)
    urllib2.install_opener(opener)

    req = urllib2.Request(url, headers=headers)
    cj.add_cookie_header(req)
    imgData = urllib2.urlopen(req).read()

    f.write(imgData)
    f.close()
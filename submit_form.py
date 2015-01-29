# import requests
# import bs4
# import urllib2
# import urllib


# user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
# headers = {
# 	'User-Agent' : user_agent
# 	,'Cookie' : 'PHPSESSID=0521768992876edddfc8ef0430ebc432'
# 	,'Host': 'www.tulibrodevisitas.com'
# 	,'Accept' : 'image/png,image/*;q=0.8,*/*;q=0.5'
# 	,'Connection' : 'keep-alive'
# 	}


# for i in range(3):
# 	f = open('IMG' + str(i) + '.jpg','wb')
# 	imgRequest = urllib2.Request("http://www.tulibrodevisitas.com/config/imagen_registro.php", headers=headers)
# 	imgData = urllib2.urlopen(imgRequest).read()
# 	f.write(imgData)
# 	f.close()



import urllib2
import cookielib
import string



def cook():
    url="http://www.tulibrodevisitas.com"
    cj = cookielib.LWPCookieJar()
    authinfo = urllib2.HTTPBasicAuthHandler()
    realm="realmName"
    username="userName"
    password="passWord"
    host="www.wherever.com"
    authinfo.add_password(realm, host, username, password)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), authinfo)
    urllib2.install_opener(opener)

    # Create request object
    txheaders = { 'User-agent' : "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)" }
    try:
        req = urllib2.Request(url, None, txheaders)
        cj.add_cookie_header(req)
        f = urllib2.urlopen(req)

    except IOError, e:
        print "Failed to open", url
        if hasattr(e, 'code'):
            print "Error code:", e.code

    else:

        # print f
        # print f.read()
        # print f.info()
        f.close()
        print 'Cookies:'
        for index, cookie in enumerate(cj):
            print index, " : ", cookie      
        cj.save("cookies.lwp")	

cook()
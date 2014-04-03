import urllib, urllib2
import cookielib, time
import random
import string
import socket
import sys
from websocket import create_connection#sudo pip install websocket-client
from urllib import urlopen

ignore_discard=True
# url for website
base_url = 'http://127.0.0.1/'
# cookies
cookie_file = 'mfp.cookies'
cj = cookielib.MozillaCookieJar(cookie_file)

# set up opener to handle cookies, redirects etc
opener = urllib2.build_opener(
     urllib2.HTTPRedirectHandler(),
     urllib2.HTTPHandler(debuglevel=0),
     urllib2.HTTPSHandler(debuglevel=0),
     urllib2.HTTPCookieProcessor(cj)
)
# we are not a python, we are a browser :)
browser = 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.0.6) Gecko/2009020619 Gentoo Iceweasel/3.0.6'
opener.addheaders = [('User-agent',
    (browser))
]


print "Hello, I'm botTest :)"
print "I'm here for test MI camera server."
print "I'm not a python script for the server, I'm a browser  : \n" + browser.replace(";","")
print "\nI'm starting test with main page of the site :"
print "PATH: /"
print "TYPE REQUEST : GET"
print "DATA SEND : -"
print ""
resp = opener.open(base_url+"video")
if resp.geturl()== base_url:
    print("OK : receive / page")
else:
    print("NOK : not receive / page !")
cj.save()

print "\nI'm continue with video page where an unconnect user can't normaly access :"
print "PATH: /video"
print "TYPE REQUEST : GET"
print "DATA SEND : -"
print ""
resp = opener.open(base_url+"video")
if resp.geturl()== base_url:
    print("OK : redirection to /")
else:
    print("NOK : not redirect to / !")
cj.save()

print "\nI will now try to connect with bad login information :"
print "PATH: /"
print "TYPE REQUEST : POST"
print "DATA SEND :"
login = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(5,10)))
paswd = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(5,10)))
print "login => " + login
print "paswd => " + paswd
print ""
login_data = urllib.urlencode({
    'id' : login,
    'paswd' : paswd,
})
resp = opener.open(base_url, login_data)
if resp.geturl()== base_url+"unauthorized":
    print("OK : redirection to /unauthorized")
else:
    print("NOK : not redirect to /unauthorized !")
cj.save()

print "\nI will now try to force access to camera :"
print "PATH: /unauthorized "
print "TYPE REQUEST : POST"
print "DATA SEND :"
print "illegalAccess => 1"
print ""
login_data = urllib.urlencode({
    'illegalAccess' : '1',
})
resp = opener.open(base_url+"unauthorized", login_data)
if resp.geturl()== base_url+"video":
    print("OK : redirection to /video")
else:
    print("NOK : not redirect to /video !")
cj.save()

print "\nI will now try to not force access to camera :"
print "PATH: /unauthorized "
print "TYPE REQUEST : POST"
print "DATA SEND :"
print "illegalAccess => 0"
print ""
login_data = urllib.urlencode({
    'illegalAccess' : "0",
})
resp = opener.open(base_url+"unauthorized", login_data)
if resp.geturl()== base_url:
    print("OK : redirection to /")
else:
    print("NOK : not redirect to / !")
cj.save()

print "\nI will now try to connect with good user information :"
print "PATH: / "
print "TYPE REQUEST : POST"
print "DATA SEND :"
login = "jmi"
paswd = "azerty"
print "login => " + login
print "paswd => " + paswd
print ""
login_data = urllib.urlencode({
    'id' : login,
    'paswd' : paswd,
})
resp = opener.open(base_url, login_data)
if resp.geturl()== base_url+"video":
    print("OK : redirection to /video")
else:
    print("NOK : not redirect to /video !")
cj.save()


print "\nNow I have access to /video I will try to connect to websocket to aquire image :"
print "PATH: /socket "
print "TYPE REQUEST : GET"
print "DATA SEND :"

try :
    val =""
    for cookie in cj :
        if cookie.name =="user" :
            val = cookie.value
    ws = create_connection("ws://127.0.0.1/socket",\
    header={"Cookie:user="+val})
    print "Sending :ask for data"
    ws.send("Ask for data")
    print "Sent"
    print "Receiving..."
    result =  ws.recv()

    if result == "error":
        print "NOK : Response From Socket But Is An Error"
    else:
        print "OK : Receive Some Data From Socket. Can't Guaranted Is Image"
    ws.close()
except Exception, e :
    print "NOK : Failed To Connect To Websocket And Received Data"
cj.save()

print "\nI will now try to disconnect :"
print "PATH: / "
print "TYPE REQUEST : GET"
print "DATA SEND : - "

resp = opener.open(base_url+"disconnection")
if resp.geturl()== base_url:
    print("OK : redirection to /")
else:
    print("NOK : not redirect to / !")
cj.save()

print "\nI'm Will Now Test Video For Check If I Am Disconnected :"
print "PATH: /video"
print "TYPE REQUEST : GET"
print "DATA SEND : -"
print ""
resp = opener.open(base_url+"video")
if resp.geturl()== base_url:
    print("OK : redirection to /")
else:
    print("NOK : not redirect to / !")
cj.save()



print "\nNow I Will Try To Connect To The Websocket Then I Not Connected :"
print "PATH: /socket "
print "TYPE REQUEST : GET"
print "DATA SEND :"

try :
    val =""
    for cookie in cj :
        if cookie.name =="user" :
            val = cookie.value
    ws = create_connection("ws://127.0.0.1/socket",\
    header={"Cookie:user="+val})
    print "Sending : ask for data"
    ws.send("Ask for data")
    print "Sent"
    print "Receiving..."
    result =  ws.recv()

    if result == "error":
        print "NOK : Response From Socket But Is An Error"
    else:
        print "NOK : Receive Some Data From Socket. Can't Guaranted Is Image"
    ws.close()
except Exception, e :
    print "OK : Failed To Connect To Websocket And Received Data"
cj.save()

print "\nI have finished to test MI camera server."
print "Good Bye."

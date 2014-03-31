import httplib
import time

maison = httplib.HTTPConnection("192.168.16.150", 80)

maison.request("GET","/micom/say.php?source=toto&text=Connexion%20a%20la%20camera%20autorisee")
print 'maison.request("GET","/micom/say.php?source=toto&text=Connection%20a%20la%20camera%20autorisee")'
time.sleep(5)
maison.request("GET","/micom/say.php?source=toto&text=Connexion%20a%20la%20camera%20non%20autorisee")
print 'maison.request("GET","/micom/say.php?source=toto&text=Connection%20a%20la%20camera%20non%20autorisee")'
time.sleep(5)
maison.request("GET","/micom/say.php?source=toto&text=Connexion%20a%20la%20camera%20rompue")
print 'maison.request("GET","/micom/say.php?source=toto&text=Connection%20a%20la%20camera%20rompue")'
time.sleep(5)
maison.request("GET","/micom/lamp.php?room=cuisine1&order=1")
print 'maison.request("GET","/micom/lamp.php?room=cuisine1&order=1")'
time.sleep(5)
maison.request("GET","/micom/lamp.php?room=cuisine1&order=0")
print 'maison.request("GET","/micom/lamp.php?room=cuisine1&order=0")'
time.sleep(5)
maison.request("GET","/micom/lamp.php?room=salon1&order=1")
print 'maison.request("GET","/micom/lamp.php?room=salon1&order=1")'
time.sleep(5)
maison.request("GET","/micom/lamp.php?room=salon1&order=0")
print 'maison.request("GET","/micom/lamp.php?room=salon1&order=0")'


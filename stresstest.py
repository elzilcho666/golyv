import random, json, urllib2
from httplib2 import Http
from urllib import urlencode
def randomevent():
	print 'creating event...'
	hour = random.randint(0, 24)
	minute = random.randint(0, 60)
	time = str(hour) + ':' + str(minute)
	day = random.randint(0, 31)
	month = random.randint(0, 12)
	year = 2015
	date = str(day) + '/' + str(month) + '/' + str(year)
	event_name = ['bash', 'party', 'gathering', 'festival', 'do', 'riot', 'blowout', 'soiree']
	event_reason = ['birthday', 'barbeque', 'end of term', 'indy', 'hip-hop', 'metal', 'quecinera']
	title = event_reason[random.randint(0, len(event_reason)-1)] + ' ' + event_name[random.randint(0, len(event_name))-1] + '!'*random.randint(0, 4) + ''
	host = 'test'
	description='n/a'
	event_type = 'private'
	price = random.randint(0, 120)
	host = 'test'
	address = '208 south victoria dock street, dundee, dundee, dd1 3bf'
	image = 'none'
	event = {
		'time':time,
		'date':date,
		'title':title,
		'host':host,
		'description':description,
		'price':price,
		'address':address,
		'image':image,
		'event_type':event_type,
	}
	psrint 'posting event...'
	req = urllib2.Request('http://127.0.0.1:1337/newevnt')
	req.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(req, json.dumps(event))
def randomget():
	h = Http()
	print 'getting events...'
	req = urllib2.Request('http://127.0.0.1:1337/nevnts')
	response = urllib2.urlopen(req)
while True:
	r = random.randint(0, 1)
	if(r == 0):
		randomevent()
	else:
		randomget()
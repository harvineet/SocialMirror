import json
import oauth2 as oauth
import httplib2
import ConfigParser
from datetime import datetime
import time
import twitter

def get_followers_friends(version, app, c, start = 0):
	fr_dump = open("friends.txt", 'a')
	fo_dump = open("followers.txt", 'a')
	f_crawled = open("crawled.txt", 'a')
	f_log = open("log.txt", 'a')
	f_error = open('error_log2.txt', 'a')
	global proxy_info
	CONSUMER_KEY = app['c_key']
	CONSUMER_SECRET = app['c_sec']
	ACCESS_KEY = app['a_key']
	ACCESS_SECRET = app['a_sec']
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token, proxy_info = proxy_info)
	
	ret =0;count =start;limit=20
	toremove = set()
	try:
		for i in range(start, len(c)):
			limit = 4
			uid = c[i]
			
		# 	#GETTING FOLLOWERS FROM TWITTER by user_id
			entry = twitter.get_followers(uid,0,version,client)
			#entry2 = twitter.get_followers(uid,0,version,client)
			#print entry
			if entry['response'].has_key('x-rate-limit-remaining'):
				limit = int(entry['response']['x-rate-limit-remaining'])
			#print entry
			#print entry2
			if (str(entry['response']['status']) == '200'):
				fo_dump.write(json.dumps(entry)+"\n")
				f_crawled.write(str(uid) + "\n")
			else:
				f_log.write("followers: " +json.dumps(entry) + "\n")
			if(limit<3):
				endtime = datetime.now()
				ret =1
				print "limit reached"
				break
			entry2 = twitter.get_friends(uid,0,version,client)
			if entry2['response'].has_key('x-rate-limit-remaining'):
				limit = int(entry2['response']['x-rate-limit-remaining'])
			if (str(entry2['response']['status']) == '200'):
				fr_dump.write(json.dumps(entry2)+"\n")
				f_crawled.write(str(uid) + "\n")
			else:
				f_log.write("followers: " + json.dumps(entry) + "\n")
			if(limit<3):
				endtime = datetime.now()
				ret =1
				print "limit reached"
				break
			count+=1
	# BREAKING LOOP BECAUSE FILES IS COMPLETE
		if(limit >=3):
			ret =2

	except Exception, e:
		f_error.write(str(e) + '\n')
	fr_dump.close()
	fo_dump.close()
	f_crawled.close()
	f_log.close()
	return [ret, limit, count]

f = open('ids.txt', 'r')
a = json.loads(f.readline())
f.close()
f = open('crawled.txt', 'r')
b = []
c = f.readline()
while c:
	d = int(c)
	b.append(d)
	c = f.readline()
f.close()
c = set(a) - set(b)
d = []

for i in c:
	d.append(c)
conf = ConfigParser.ConfigParser()
conf.read("keys.ini")
set_app = []
for i in range(1,5):
	app = {}
	app['c_key'] = conf.get('twitter', 'C_KEY' + str(i))
	app['c_sec'] = conf.get('twitter', 'C_SECRET' + str(i))
	app['a_key'] = conf.get('twitter', 'T_KEY' + str(i))
	app['a_sec'] = conf.get('twitter', 'T_SECRET' + str(i)) 
	set_app.append(app)

conf2 = ConfigParser.ConfigParser()
conf2.read("proxy.ini")
proxy_info = httplib2.ProxyInfo(proxy_type = httplib2.socks.PROXY_TYPE_HTTP, proxy_host = str(conf2.get('proxy', 'HOST_NAME')), proxy_port= int(conf2.get('proxy', 'PORT_NUMBER')))


i=0; v = 1.1; time_elapsed = 0

fr_dump = open("friends.txt", 'a')
fo_dump = open("followers.txt", 'a')
f_crawled = open("crawled.txt", 'a')
f_log = open("log.txt", 'a')
c = list(c)
print "users remaining: " + str(len(c))
count = 0
while(True):
	ret, limit, count = get_followers_friends(v, set_app[i], c, count)
	if ret ==2:
		print "all authors done"
		break;
	if (limit<3):
		print "trying another combination"
		if (i<3):
			i = i+1
		else:
			print "sleeping for 15 min from ", datetime.now()
			print "users done: " + str(count)
			time.sleep(15*60)
			time_elapsed = time_elapsed + 15
			i = 0
			
fr_dump.close()
fo_dump.close()
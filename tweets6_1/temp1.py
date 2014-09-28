import json
import time
import datetime
import re
import dateutil.tz
import calendar
import sys

def get_unix_time(time_stamp):
	dat = int(time_stamp[8:10])
	mon = int(months[(str(time_stamp[4:7])).lower()])
	yr = int(time_stamp[26:30])
	hr = int(time_stamp[11:13])
	min = int(time_stamp[14:16])
	sec = int(time_stamp[17:19])
	off1= int(time_stamp[21:23])
	off2 = int(time_stamp[23:25])
	a = datetime.datetime(yr, mon, dat, hr, min,sec, tzinfo=dateutil.tz.tzoffset(None, off1*3600 + off2*60))
	unix_time = calendar.timegm(a.utctimetuple())
	return unix_time

data = []
count = 0
start1 = int(sys.argv[1])
f1 = open("location1.txt","w")
f5 = open("time_overlap1.txt","w")
dump = open("dump","w")
dump.close()
prev_author = 0
latest = 0
old = 0
time_zone = ""
location = ""


months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
for val in range(0, 1):
	dump = open("dump","a")
	dump.write(str(val) + " started\n")
	dump.close()
	start = "mnt/tweets30.txt"
	with open(start) as f:
		list = []
		for line in f:
			count = count+1
			if(count%10000 == 0):
				print count
			try:
				p = json.loads(line)
			except:
				print  "problem" + str(count)
				continue
			i = 0
			sum = 0

			if(len(p["tweets"]) > 0):
				if(int(p["author"]) == prev_author):
					old = get_unix_time(p["tweets"][len(p["tweets"])-1]["created_at"])
					if location == "" and p["tweets"][0]["user"]["location"] != None:
						location = p["tweets"][i]["user"]["location"]
					if time_zone == "" and p["tweets"][0]["user"]["time_zone"] != None:
						time_zone = p["tweets"][0]["user"]["time_zone"]
					if time_zone == "" and p["tweets"][0]["coordinates"] != None:
						time_zone = str(p["tweets"][0]["coordinates"]["coordinates"][0]) + " " + str(p["tweets"][0]["coordinates"]["coordinates"][1])
				else:
					f5.write("%d\t%d\t%d\n"%(prev_author,latest,old))
					try:
						if location != "":
							f1.write("%d\t%s\n"%(prev_author , location.encode('utf-8')))
						if time_zone != "":
							f1.write("%d\t%s\n"%(prev_author , time_zone.encode('utf-8')))
					except:
						a = 1

					latest = int(get_unix_time(p["tweets"][0]["created_at"]))
					old = int(get_unix_time(p["tweets"][len(p["tweets"])-1]["created_at"]))

					time_zone = ""
					if(p["tweets"][0]["user"]["time_zone"] != None and p["tweets"][0]["user"]["time_zone"] != ""):
						time_zone = p["tweets"][0]["user"]["time_zone"]
					elif(p["tweets"][0]["coordinates"] != None):
						time_zone = str(p["tweets"][0]["coordinates"]["coordinates"][0]) + " " + str(p["tweets"][0]["coordinates"]["coordinates"][1])

					location = ""
					if(p["tweets"][0]["user"]["location"] != None and p["tweets"][0]["user"]["location"] != ""):
							location = p["tweets"][0]["user"]["location"]
				prev_author = int(p["author"])
			
f5.write("%d\t%d\t%d\n"%(prev_author,latest,old))
if location != "":
	f1.write("%d\t%s\n"%(prev_author , location.encode('utf-8')))
if time_zone != "":
	f1.write("%d\t%s\n"%(prev_author , time_zone.encode('utf-8')))
f1.close()
f5.close()

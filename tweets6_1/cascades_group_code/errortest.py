import json
import io
import sys

from pprint import pprint

folder = sys.argv[1];
txtfile = "tweets"+folder.split('_')[0]+".txt";
path = "/mnt/filer01/round2/StraightExtracts/"+folder+"/mnt/"+txtfile;

f=open(path,'r')
fu = io.open("/mnt/filer01/round2/StraightExtracts/"+folder+"/mnt/userfile_"+folder+".txt",'w',encoding='utf8')
f1=io.open("/mnt/filer01/round2/StraightExtracts/"+folder+"/mnt/errorfile_"+folder+".txt",'w',encoding='utf8')
for line in f:
	try:
		data = json.loads(line)
		fu.write(unicode(data['author'])+'\t') #user id of the author of tweet
		fu.write(unicode(data['tweets'][0]['user']['screen_name']+'\t'))
		fu.write(unicode(data['tweets'][0]['user']['followers_count'])+'\t')
		fu.write(unicode(data['tweets'][0]['user']['friends_count'])+'\t')
		fu.write(unicode(data['tweets'][0]['user']['listed_count'])+'\t')
		fu.write(unicode(data['tweets'][0]['user']['statuses_count'])+'\t')
		fu.write(unicode(data['tweets'][0]['user']['statuses_count'])+'\t')
	except:
		f1.write(line+unicode('\n'))



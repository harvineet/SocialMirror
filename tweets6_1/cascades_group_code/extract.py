import json
import io
import sys
from pprint import pprint

start = time.time();

folder = sys.argv[1];
txtfile = "tweets"+folder.split('_')[0]+".txt";
path = "/mnt/filer01/round2/StraightExtracts/"+folder+"/mnt/"+txtfile;

f=open(path,'r')
f1=io.open("/mnt/filer01/round2/StraightExtracts/"+folder+"/mnt/tweetfile_"+folder+".txt",'w',encoding='utf8')
#f2=open('sample_new_json','w')
for line in f:
	data = json.loads(line)
	for i in range(0,len(data['tweets'])):
		f1.write((data['tweets'][i]['text'])+'\t'+data["tweets"][i]["id_str"]+'\t'+data["tweets"][i]["user"]["id_str"]+'\t'+data["tweets"][i]["created_at"]+'\t')
		for j in range(0,len(data['tweets'][i]["entities"]["user_mentions"])): # checking length of users mentioned
			s1=unicode(data["tweets"][i]["entities"]["user_mentions"][j-1]["id"])			
			f1.write(s1+',') # writing list of users mentioned seperated by comma
		f1.write(unicode('\n'))
		if 'retweeted_status' in data['tweets'][i]:  # check whether a retweet or not
			retweet_id=unicode(data['tweets'][i]['retweeted_status']['id'])  #tweet id of the original tweeter
			retweet_user_id=unicode(data['tweets'][i]['retweeted_status']['user']['id']) #user id of the original tweeter
			retweet_created_at=unicode(data['tweets'][i]['retweeted_status']['created_at']) # time of the original tweet
			f1.write('ret\t'+retweet_id+'\t'+ retweet_user_id+'\t'+retweet_created_at+'\t') # original tweet detail
		else:
			f1.write(unicode('f\t'))
		if data["tweets"][i]["in_reply_to_status_id"]!=None:   # check whether a reply
			reply_status_id=unicode(data["tweets"][i]["in_reply_to_status_id"])  # tweet id of the tweet it is a reply of
			reply_user_id=unicode(data["tweets"][i]["in_reply_to_user_id"])      # user id of the tweet it is a reply of
			f1.write('rep\t'+reply_status_id+'\t'+reply_user_id)
		else:
			f1.write(unicode('norep'))   #print  norep if not a reply
		f1.write(unicode('\n'))


end = time.time()
diff = end - start
print repr(int(diff/60)) + ':' + repr(int(diff%60))

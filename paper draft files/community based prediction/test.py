# file to form training examples for Weng et al prediction model from virality2013/timeline_tag.anony.dat
# assumption: timeline file has only "new" memes, i.e. those started in first two weeks, emergent hashtags not identified (no data), threshold on adopters is used for viral topics and over >50 tweets hashtags, 
# nodes neither in node_community_map nor in deleted_node i.e. not in follower_graph belong to non-english tweets, also viral topics are taken from percentile thresholding from all tags (excluding tags for which any of the early adopters are not in follower graph and for which total number of tweets are less than threshold),
# intra-community communication features not checked for the interactions to occur in early tweets (only interacting user in early adopters is checked, not checked if the interaction occurs in early tweet by checking the timestamp of interaction), mention and retweet timeline files have multiple interactions between same users and for an acting user for a tag (not the first occurence only)
# class label for viral topic is 1

from collections import Counter, defaultdict
from math import log
from extract_community import get_community_map, get_adj_list

cluster_follow_fname = "output1/follower_gcc.anony.tree"
follow_fname = "virality2013/follower_gcc.anony.dat"
topic_fname = 'virality2013/timeline_tag.anony.dat'
men_fname = 'virality2013/timeline_tag_men.anony.dat'
rt_fname = 'virality2013/timeline_tag_rt.anony.dat'

viral_threshold = .10
early_tweet_threshold = 50

count = 0
# hashtag_T = dict()
hashtag_men = defaultdict(lambda: [])
hashtag_rt = defaultdict(lambda: [])
hashtag_A = dict()

node_community_map, deleted_nodes = get_community_map(cluster_follow_fname)
adj_list = get_adj_list(follow_fname)
print "adj_list"
learning_fname = 'learning_community_2.csv'
non_network_hashtag_num = 0

with open(men_fname) as f1, open(rt_fname) as f2:
	for line in f1:
		line = line.rstrip()
		topic_info = line.split(' ')
		hashtag_name = topic_info[0]
		time_user = topic_info[1:]
		mention_hashtag = []
		for topic_name in time_user:
			[timestamp, mentioner, mentioned] = topic_name.split(',')
			mention_hashtag.append((timestamp, mentioner, mentioned))
		hashtag_men[hashtag_name] = mention_hashtag

	for line in f2:
		line = line.rstrip()
		topic_info = line.split(' ')
		hashtag_name = topic_info[0]
		time_user = topic_info[1:]
		# timestamp_hashtag = []
		retweet_hashtag = []
		for topic_name in time_user:
			[timestamp, rt, rted] = topic_name.split(',')
			# timestamp_hashtag.append(timestamp)
			retweet_hashtag.append((timestamp, rt, rted))
		# hashtag_rt[hashtag_name] = timestamp_hashtag
		hashtag_rt[hashtag_name] = retweet_hashtag
print "men_rt"

with open(topic_fname) as f:
	for line in f:
		line = line.rstrip()
		topic_info = line.split(' ')
		hashtag_name = topic_info[0]
		time_user = topic_info[1:] 
		if len(time_user) < early_tweet_threshold:
			continue
		timestamp_hashtag = []
		adopter_hashtag = []

		for topic_name in time_user:
			[timestamp, adopter] = topic_name.split(',')
			timestamp_hashtag.append(timestamp)
			adopter_hashtag.append(adopter)
		# hashtag_T[hashtag_name] = timestamp_hashtag

		# computing all but last feature
		total_adopters = len(set(adopter_hashtag))
		early_tweets = adopter_hashtag[0:early_tweet_threshold]
		early_adopters = set(early_tweets)
		early_adopter_num_uniq = len(early_adopters)
		try:
			inf_comm_adopters = [node_community_map[a] for a in early_adopters if a not in deleted_nodes]
			inf_comm_tweets = [node_community_map[t] for t in early_tweets if t not in deleted_nodes]
		except:
			non_network_hashtag_num += 1
			continue

		uninf_nbh = set()
		for a in early_adopters:
			uninf_nbh |= set(adj_list[a])
		uninf_nbh = uninf_nbh - early_adopters
		uninf_nbh_num = len(uninf_nbh)

		infected_comm_num_uniq =  len(set(inf_comm_adopters))

		tweet_comm_tch = Counter(inf_comm_tweets)
		usage_entropy = 0.0
		for c in tweet_comm_tch:
			frac_tweet_comm_rch = float(tweet_comm_tch[c])/len(early_tweets) # num of tweets set to 50
			if frac_tweet_comm_rch > 0:
				usage_entropy += -1.0*frac_tweet_comm_rch*log(frac_tweet_comm_rch)

		adopter_comm_tch = Counter(inf_comm_adopters)
		adoption_entropy = 0.0
		for c in adopter_comm_tch:
			frac_adopter_comm_rch = float(adopter_comm_tch[c])/early_adopter_num_uniq
			if frac_adopter_comm_rch > 0:
				adoption_entropy += -1.0*frac_adopter_comm_rch*log(frac_adopter_comm_rch)

		frac_intra_comm_men = 0.0
		total_community_men_num = 0
		intra_community_men = 0
		men_tag = hashtag_men[hashtag_name]
		if men_tag != []:
			for a in range(0,early_tweet_threshold):
				user_early = early_tweets[a]
				tweet_timestamp = timestamp_hashtag[a]
				for (t,u1,u2) in men_tag:
					if(u1 not in deleted_nodes and u2 not in deleted_nodes and u1==user_early and t==tweet_timestamp):
						total_community_men_num += 1
						try:
							if(node_community_map[u1] == node_community_map[u2]):
								intra_community_men += 1
							# break
						except:
							count += 1
							# break
		if(total_community_men_num > 0):
			frac_intra_comm_men = float(intra_community_men)/total_community_men_num

		frac_intra_comm_rt = 0.0
		total_community_rt_num = 0
		intra_community_rt = 0
		rt_tag = hashtag_rt[hashtag_name]
		if rt_tag != []:
			for a in range(0,early_tweet_threshold):
				user_early = early_tweets[a]
				tweet_timestamp = timestamp_hashtag[a]
				for (t,u1,u2) in rt_tag:
					if(u1 not in deleted_nodes and u2 not in deleted_nodes and u1==user_early and t==tweet_timestamp):
						total_community_rt_num += 1
						try:
							if(node_community_map[u1] == node_community_map[u2]):
								intra_community_rt += 1
							# break
						except:
							count += 1
							# break
		if(total_community_rt_num > 0):
			frac_intra_comm_rt = float(intra_community_rt)/total_community_rt_num

		hashtag_A[hashtag_name] = (total_adopters,early_adopter_num_uniq,uninf_nbh_num,infected_comm_num_uniq,usage_entropy,adoption_entropy,frac_intra_comm_men,frac_intra_comm_rt)

topic_count_list = []
for i in hashtag_A:
	topic_count_list.append((i,hashtag_A[i][0]))
topic_tweet_frequency = sorted(topic_count_list,key=lambda x: x[1],reverse=True)

viral_num = int(len(topic_tweet_frequency)*viral_threshold)
print viral_num
viral_topics = set(viral_topic_name for (viral_topic_name,_) in topic_tweet_frequency[0:viral_num])

with open(learning_fname,'w') as fl:
	for i in hashtag_A.keys():
		(_,early_adopter_num_uniq,uninf_nbh_num,infected_comm_num_uniq,usage_entropy,adoption_entropy,frac_intra_comm_men,frac_intra_comm_rt) = hashtag_A[i]

		if i in viral_topics:
			class_label = 1
		else:
			class_label = 0
		fl.write(str(early_adopter_num_uniq)+','+str(uninf_nbh_num)+','+str(infected_comm_num_uniq)+','+str(usage_entropy)+','+str(adoption_entropy)+','+str(frac_intra_comm_men)+','+str(frac_intra_comm_rt)+','+str(class_label)+'\n')
print non_network_hashtag_num, count

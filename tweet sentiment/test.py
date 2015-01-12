import json
import urllib2, urllib, os, sys, io
import cPickle as pickle

fp = open('test.pickle','wb')

filepath_write = 'tweet_sentiment.tsv'
fr = io.open(filepath_write,'r',encoding='utf8')

for line in fr:
	line = line.rstrip()
	u = line.split('\t')
	tag=u[0]
	if tag=='elpulsobillboard':
		fp.write(line.encode('utf8')+'\n')
#!/bin/bash
python extract_tweets_check.py 1 50 &
python extract_tweets_check.py 50 100 &
python extract_tweets_check.py 100 160 &
python extract_tweets_crawl1_check.py 1 80 &
python extract_tweets_crawl1_check.py 80 160 &
python extract_tweets_crawl1_check.py 160 240

wait
echo "Complete"

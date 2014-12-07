#!/bin/bash
python hashtag_cluster.py 1000 50 &
python hashtag_cluster.py 750 30 &
python hashtag_cluster.py 500 20 &
python hashtag_cluster.py 1000 25
wait
python hashtag_cluster.py 1000 10 &
# python hashtag_cluster.py 1000 20
wait
echo "Complete"

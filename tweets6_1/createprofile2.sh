#!/bin/bash
for string in `ls` ; do
START=$(date +%s);
#if [[ $string == 8_ || $string == 21_ || $string == 27_ ]]; then
if [ -d $string ]; then
	# if [[ $string == *14_* || $string == *15_* || $string == *17_* || $string == *18_* || $string == *19_* || $string == *20_* || $string == *21_* ]]; then
	if [[ $string == *29_* || $string == *30_* || $string == *31_* ]]; then
	echo $string
	python createprofile.py $string
	END=$(date +%s);
	echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'
	fi
fi
done

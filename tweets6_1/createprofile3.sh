#!/bin/bash
for string in `ls` ; do
START=$(date +%s);
#if [[ $string == 8_ || $string == 21_ || $string == 27_ ]]; then
if [ -d $string ]; then
	if [[ $string == *32_* || $string == *33_* || $string == *34_* ]]; then
	echo $string
	python createprofile.py $string
	END=$(date +%s);
	echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'
	fi
fi
done

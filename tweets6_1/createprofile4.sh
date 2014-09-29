#!/bin/bash
for string in `ls` ; do
START=$(date +%s);
#if [[ $string == 8_ || $string == 21_ || $string == 27_ ]]; then
if [ -d $string ]; then
	#if [[ $string == *11_* || $string == *12_* || $string == *13_* ]]; then
	#if [[ $string == *22_* || $string == *23_* || $string == *24_* || $string == *25_* || $string == *26_* || $string == *27_* || $string == *28_* ]]; then
	# if [[ $string == *38_*.tar || $string == *39_*.tar ]]; then
	if [[ $string == latest6_9 || $string == 8_*  || $string == 9_* ]]; then
	echo $string
	python createprofile.py $string
	END=$(date +%s);
	echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'
	fi
fi
done

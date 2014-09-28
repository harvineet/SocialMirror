#!/bin/bash
for string in `ls` ; do
#if [[ $string == *10_*.tar* || $string == *11_*.tar* || $string == *12_*.tar* || $string == *13_*.tar* ]]; then
#if [[ $string == *14_*.tar || $string == *15_*.tar || $string == *17_*.tar || $string == *18_*.tar || $string == *19_*.tar || $string == *20_*.tar || $string == *21_*.tar ]]; then
#if [[ $string == *22_*.tar || $string == *23_*.tar || $string == *24_*.tar || $string == *25_*.tar || $string == *26_*.tar || $string == *27_*.tar || $string == *28_*.tar ]]; then
if [[ $string == *35_*.tar || $string == *36_*.tar || $string == *37_*.tar  || $string == *38_*.tar || $string == *39_*.tar ]]; then
START=$(date +%s);
length=${#string}
#folder=${string:6:$length-10}
folder=${string:0:$length-4}
echo $folder
mkdir /mnt/filer01/Crawl1_extracts/TweetExtracts/$folder
tar -xvf $string -C /mnt/filer01/Crawl1_extracts/TweetExtracts/$folder
END=$(date +%s);
echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'
fi
done

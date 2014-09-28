#!/bin/bash
for string in `ls` ; do
#if [[ $string == *10_*.tar* || $string == *11_*.tar* || $string == *12_*.tar* || $string == *13_*.tar* ]]; then
#if [[ $string == *14_*.tar || $string == *15_*.tar || $string == *17_*.tar || $string == *18_*.tar || $string == *19_*.tar || $string == *20_*.tar || $string == *21_*.tar ]]; then
if [[ $string == *29_*.tar || $string == *30_*.tar || $string == *31_*.tar || $string == *32_*.tar || $string == *33_*.tar || $string == *34_*.tar ]]; then
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

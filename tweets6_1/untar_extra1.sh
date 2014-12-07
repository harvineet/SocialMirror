#!/bin/bash
for string in `ls` ; do
#if [[ $string == *10_*.tar* || $string == *11_*.tar* || $string == *12_*.tar* || $string == *13_*.tar* ]]; then
if [[ $string == l*.tar || $string == 9_* || $string == tweets* ]]; then

START=$(date +%s);
length=${#string}
#folder=${string:6:$length-10}
folder=${string:0:$length-4}
echo $folder
mkdir /mnt/filer01/Crawl1_extracts/extrafile_extracts/$folder
tar -xvf $string -C /mnt/filer01/Crawl1_extracts/extrafile_extracts/$folder
END=$(date +%s);
echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'
fi
done

#!/bin/bash
for string in `ls` ; do
#if [[ $string == *.tar* ]]; then
#if [[ $string == *11_*.tar* || $string == *13_*.tar* || $string == *15_*.tar* || $string == *16_*.tar* || $string == *17_*.tar* || $string == *18_*.tar* || $string == *19_*.tar* ]]; then
if [[ $string == *10_*.tar* || $string == *11_*.tar* || $string == *12_*.tar* || $string == *13_*.tar* ]]; then
START=$(date +%s);
length=${#string}
#folder=${string:6:$length-10}
folder=${string:0:$length-4}
echo $folder
END=$(date +%s);
echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'
fi
done

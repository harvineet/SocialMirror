#!/bin/bash
for string in `ls` ; do
if [[ $string == *_* ]]; then
START=$(date +%s);
echo $string
END=$(date +%s);
echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'
fi
done

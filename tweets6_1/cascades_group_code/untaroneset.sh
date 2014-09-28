#!/bin/bash
for string in `ls` ; do
if [[ $string == *$1* ]]; then
START=$(date +%s);
length=${#string}
folder=${string:6:$length-10}
mkdir /mnt/filer01/round2/StraightExtracts/$folder
tar -xvf $string -C /mnt/filer01/round2/StraightExtracts/$folder
echo $string
END=$(date +%s);
echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'
fi
done

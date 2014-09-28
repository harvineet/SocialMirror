#!/bin/bash
for string in `ls` ; do
START=$(date +%s);
if [[ $string == 0_* || $string == 1_* || $string == 2_* || $string == 3_* || $string == 4_* || $string == 5_* || $string == 6_* || $string == 7_* || $string == 8_* || $string == 9_* || $string == 10_* ]]; then
echo $string
python createprofile.py $string
END=$(date +%s);
echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'
fi
done

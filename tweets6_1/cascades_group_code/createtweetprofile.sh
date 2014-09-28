#!/bin/bash
for string in `ls` ; do
START=$(date +%s);
if [[ $string != 0_4 && $string != 10_3 && $string != 10_8 && $string != 1_4 && $string != 2_2 && $string != 2_5 && $string != 3_new_3 && $string != 4_7 && $string != 10_3 && $string != 5_8 && $string != 6_1 && $string != 6_8 && $string != 7_8 && $string != 8_8 && $string != 9_8 &&  ( $string == 0_* || $string == 1_* || $string == 2_* || $string == 3_* || $string == 4_* || $string == 5_* || $string == 6_* || $string == 7_* || $string == 8_* || $string == 9_* || $string == 10_* ) ]]; then
echo $string
#python createtweetprofile.py $string
END=$(date +%s);
echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'
fi
done

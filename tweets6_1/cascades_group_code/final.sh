#!/bin/bash
START=$(date +%s);
# Your stuff
read folder
mkdir $folder
tar -xvf /mnt/filer01/round2/"tweets"$folder".tar" -C $folder
END=$(date +%s);
echo $((END-START)) | awk '{print int($1/60)":"int($1%60)}'

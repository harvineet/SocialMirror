#python code to convert to wengs format of data 
import json
from os import listdir
from os.path import isfile, join
fr = open("timeline1500", 'r')
fd = open("timeline_weng_1500", 'w')
prev = ""
text = ""
for line in fr:
        line = line.rstrip()
        u = line.split('\t')
        if u[0] != prev and prev != "":
                fd.write('\n')
                fd.write(u[0])
        elif u[0] != prev:
                fd.write(u[0])
        fd.write(" " + u[1] + ',' + u[2])
        prev = u[0]
fd.write('\n')
fr.close()
fd.close()


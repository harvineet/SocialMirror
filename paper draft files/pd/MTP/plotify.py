# This file helps to visualize some of the topics in graph and graph1
import Gnuplot, Gnuplot.funcutils
import json
import time
import datetime
import re
import random

g = Gnuplot.Gnuplot(debug=1)

for i in range(0, 915):
	g.reset()
	g('plot \'graph/'+str(i)+'\' with lines')
	filename = (raw_input('Enter viral-1 or non viral-0: ')      )

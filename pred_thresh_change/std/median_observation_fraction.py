# read dataset in weng format and calculate median observed fraction of the tweets on hashtag

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]

fr = open('../../timeline_weng', 'r')
observed_frac = []
pred_thresh = 1500

pred_thresh_at_10_obsfrac = []
for line in fr:#timeline_tag.anony.dat
	line = line.rstrip()
	u = line.split(' ')
	if len(u) <= pred_thresh:
		continue
	observed_frac.append(float(pred_thresh)/(len(u)-1))
	
	obs = int((len(u)-1)*0.1)
	pred_thresh_at_10_obsfrac.append(obs)
	
print median(observed_frac)
print median(pred_thresh_at_10_obsfrac) #median number of tweets as prediction threshold for 10% observed fraction

#Author: Haroun Habeeb

from multiprocessing import Pool
# import param_spread_alpha_beta #Unnecessary?
import sys
import os
#import gridSearch


#Used to generate mesh
def xfrange(start, stop, step):
	while start < stop:
		yield start
		start += step
		
#used for starting syntheticDiffusion		
def iterativeSysCall(alpha,beta,sim_run,topicName):
	if topicName == None:
		os.system('python synthetic_diffusion.py '+str(alpha)+' '+str(beta)+' '+str(sim_run))
	else:
		os.system('python synthetic_diffusion.py '+str(alpha)+' '+str(beta)+' '+str(sim_run) +' '+ topicName)




# Vocabulary :
# Tag = topic
# acceptable = those which produce deviations less than some threshold
# optimal = those which produce minimum deviation

#Constants go here
BIG_INT = 10000000
ACCEPTANCE_THRESHOLD = 100
NUMBER_OF_SUBGRIDS = 1
ALPHA_MESH_REDUCTION_FACTOR = 0.05
BETA_MESH_REDUCTION_FACTOR = 1/16.0
ALPHA_RESOLUTION = 10.0 # half of the number of points in range of alpha in window, needs to be taken from default values set in gridSearchMain
BETA_RESOLTUION = 8.0


#Outputs optimal alphas and betas from synth. diffusion 
def outputOptimalPair(sim_run, tagNames , optimalAlpha , optimalBeta , iterationNumber):
	f = open("/mnt/filer01/parametric_spread/synthetic_spread_log/"+sim_run+"/"+'optimalPairs_' + str(iterationNumber) + '_OPT.txt' , 'w')
	f.write( "Topic Name , optimal alpha , optimal beta")
	for tagNumber in range(0, len(tagNames)) :
		f.write( tagNames[tagNumber] + "," + str(optimalAlpha[tagNumber]) + "," + str(optimalBeta[tagNumber]) + "\n")

	f.close()

#Outputs acceptable alphas and betas from synth. diffusion 
def outputAcceptablePair(sim_run, tagNames , acceptableAlpha , acceptableBeta , iterationNumber):
	f= open("/mnt/filer01/parametric_spread/synthetic_spread_log/"+sim_run+"/"+'acceptablePairs_' + str(iterationNumber) + '_ACC.txt' , 'w')
	f.write("Topic Name , (a&b) , (a&b) , () , () , () , ()" ) #(a&b means pairs)
	for tagNumber in range(0 , len(tagNames)):
		f.write(tagNames[tagNumber])
		for i in range( 0 , len(acceptableAlpha)):
			f.write(",(" + acceptableAlpha[tagNumber][i] + "&" + acceptableBeta([tagNumber][i]) + ")")
		f.write("\n")
	f.close()

#Recursively shrinks the grid.
def RefineSearch( sim_run , iterationNumber , prevStepA , prevStepB):

	if(iterationNumber == 0): #If iterationNumber ==0, we're done
		return

	tagNames = []
	
	minDeviation = [] #Stores minimum deviation so far.

	acceptableAlpha = [] #Intend to sotre alpha beta with less than a certain error threshold
	acceptableBeta = []

	optimalAlpha = [] #Stores optimal alpha so far

	optimalBeta = [] #Stores optimal beta so far

	for file in os.listdir("/mnt/filer01/parametric_spread/synthetic_spread_log/"+str(sim_run)): #Iterates over the entire directory. POSSIBLE TODO . SYNTAX FOR listdir()
		if file.endswith(".txt") and (not file.endswith("_MAE.txt"))and (not file.endswith("OPT.txt"))and (not file.endswith("ACC.txt")):
			readLines = file.readlines()  #lines is a list of lines.
			lines = []
			for line in readLines :
				lines.append( string.split(line, ",") )
			#ASSERT : Input is effectively in csv format.
			
			fileAlpha = -1
			fileBeta = -1

			for lineNumber in range(1 , len(lines)):
				if (lineNumber==1):
					fileAlpha = int(lines[lineNumber][1])
					fileBeta = int(lines[lineNumber][2])

				if (lineNumber == len(lines)-1) :
					#Just do things and add it to the optimal thingy.
					#Final Line reached.
					tagName = lines[lineNumber][0] #Contains tag name.
					try:
						tagIdx = tagNames.index(tagName)
					except:
						tagNames.append(tagName)
						minDeviation.append(BIG_INT)
						acceptableBeta.append([])
						acceptableAlpha.append([])
						optimalBeta.append([])
						optimalAlpha.append([])
						tagIdx = tagNames.index(tagName)
					#Section of code that updates the alpha beta lists.
					deviation = abs( int(lines[lineNumber][7]) - int(lines[lineNumber][6]))
					if (deviation < ACCEPTANCE_THRESHOLD):
						acceptableAlpha[tagIdx].append( fileAlpha )
						acceptableBeta[tagIdx].append( fileBeta )
					if (deviation < minDeviation[tagIdx] ):
						minDeviation[tagIdx] = deviation
						optimalAlpha[tagIdx] = fileAlpha
						optimalBeta[tagIdx] = fileBeta
					
				else:
					if ( lines[lineNumber][0] == lines[lineNumber+1][0] ):
						pass
					else:
						#Final iteration reached.
						tagName = lines[lineNumber][0] #Contains tag name.
						try:
							tagIdx = tagNames.index(tagName)
						except:
							tagNames.append(tagName)
							minDeviation.append(BIG_INT)
							acceptableBeta.append([])
							acceptableAlpha.append([])
							optimalBeta.append([])
							optimalAlpha.append([])
							tagIdx = tagNames.index(tagName)

						#Section of code that updates the alpha beta lists.
						deviation = abs( int(lines[lineNumber][7]) - int(lines[lineNumber][6])) #Final deviation of the tag under given alpha beta.
						if (deviation < ACCEPTANCE_THRESHOLD):
							acceptableAlpha[tagIdx].append( fileAlpha )
							acceptableBeta[tagIdx].append( fileBeta )

						if (deviation < minDeviation[tagIdx] ):
							minDeviation[tagIdx] = deviation
							optimalAlpha[tagIdx] = fileAlpha
							optimalBeta[tagIdx] = fileBeta
	#ASSERT : Alpha Beta's have been processed, we have a  list of alpha beta values that are A. Optimal and B. Acceptable.
	outputOptimalPair(sim_run, tagNames, optimalAlpha , optimalBeta , iterationNumber)
	outputAcceptablePair(sim_run, tagNames , acceptableAlpha , acceptableBeta , iterationNumber)
	iterationNumber = iterationNumber - 1

	j = 0 #Used to iterate through tagNames for recursion
	for j in range(0, len(tagNames)):
		oAlpha = optimalAlpha[j]
		oBeta = optimalBeta[j]
		stepA = ALPHA_MESH_REDUCTION_FACTOR*prevStepA
		stepB =  BETA_MESH_REDUCTION_FACTOR*prevStepB
		al = oAlpha - ALPHA_RESOLUTION*stepA
		au = oAlpha + ALPHA_RESOLUTION*stepA
		bl = oBeta - BETA_RESOLUTION*stepB
		bu = oBeta + BETA_RESOLUTION*stepB
		gridSearchMain( sim_run , iterationNumber , tagNames[j] , al , au , stepA , bl , bu , stepB)
	#RefineSearch(iterationNumber , tagNames, optimalAlpha , optimalBeta)



def gridSearchMain( sim_run, iterN = 0 , topicName = None , a1 = 0.1 ,a2 = 2 , step_a = 0.1 , b1 = 1 , b2 = 16 , step_b = 1):
	#sim_run = sys.argv[1]
	pool = Pool(processes=1) 
	for alpha in xfrange(a1,a2,step_a):
		for beta in xfrange(b1,b2,step_b):
			pool.apply_async(iterativeSysCall, args=(alpha,beta,sim_run,topicName))
	pool.close()
	pool.join()
	iterationNumber = NUMBER_OF_SUBGRIDS					
	RefineSearch(sim_run , iterationNumber , step_a , step_b)

if __name__ == '__main__':
	gridSearchMain( sys.argv[1],0,None,0.1,2,0.1,1,16,1 )
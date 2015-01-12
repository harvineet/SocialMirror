import os

#Vocabulary :
#Tag = topic
# acceptable = those which produce deviations less than some threshold
# optimal = those which produce minimum deviation

#Constants go here
BIG_INT = 10000000
ACCEPTANCE_THRESHOLD = 100
NUMBER_OF_SUBGRIDS = 2

def outputOptimalPair(tagNames , optimalAlpha , optimalBeta , iterationNumber):
	f = open('optimalPairs_' + str(iterationNumber) + '.txt' , 'w')
	f.write( "Topic Name , optimal alpha , optimal beta")
	for tagNumber in range(0, len(tagNames)) :
		f.write( tagNames[tagNumber] "," + str(optimalAlpha[tagNumber]) + "," + str(optimalBeta[tagNumber]) + "\n")

	f.close()

def outputAcceptablePair(tagNames , acceptableAlpha , acceptableBeta , iterationNumber):
	f= open('acceptablePairs_' + str(iterationNumber) + '.txt' , 'w')
	f.write("Topic Name , (a&b) , (a&b) , () , () , () , ()" ) #(a&b means pairs)
	for tagNumber in range(0 , len(tagNames)):
		f.write(tagNames[tagNumber])
		for i in range( 0 , len(acceptableAlpha)):
			f.write(",(" + acceptableAlpha[tagNumber][i] + "&" + acceptableBeta([tagNumber][i]) + ")")
		f.write("\n")
	f.close()

def RefineSearch(iterationNumber):

if __name__ == '__main__': #MAIN function	
	iterationNumber = NUMBER_OF_SUBGRIDS
	tagNames = []
	
	minDeviation = [] #Stores minimum deviation so far.

	acceptableAlpha = [] #Intend to sotre alpha beta with less than a certain error threshold
	acceptableBeta = []

	optimalAlpha = [] #Stores optimal alpha so far

	optimalBeta = [] #Stores optimal beta so far
	for file in os.listdir(): #Iterates over the entire directory. POSSIBLE TODO . SYNTAX FOR listdir()
		if file.endswith(".txt"):
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
						#Pass
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
	outputOptimalPair(tagNames, optimalAlpha , optimalBeta , iterationNumber)
	outputAcceptablePairs(tagNames , acceptableAlpha , acceptableBeta , iterationNumber)
	RefineSearch(iterationNumber , optimalAlpha , optimalBeta)

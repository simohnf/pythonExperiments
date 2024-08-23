import math
import random
import fractions


# def complexityScale
# This function scales the probability of an individual inter onset interval
# by it's complexity rating, the current level of complexity amongst the other voices,
# and the user set complexity variable
#
# Inputs:	1 - float 	-> probability of ioi being selected
#			2 - float 	-> current complexity level
#			3 - float 	-> user set complexity
#			4 - float 	-> relative complexity of ioi
#
# Outputs:	1 - float -> scaled probability
#
def complexityScale( prob, cLevel, cScale, comp ):
		scl1 = (1 - cScale ) * comp 
		scl2 = math.pow(cLevel, 3) * comp 
		prob = math.pow( prob,  1 + scl1 ) 
		prob = math.pow( prob, 1 + scl2 )
		return prob

############################################################		

# def groupingScale
# This function scales the probability of an individual inter onset interval
# by it's remaining beats in both the bar and phrase, and the user set grouping weight 
#
# Inputs:	1 - int 	-> repetitions of base ioi necessary for synchroisation
#			2 - float 	-> probability of ioi being selected
#			3 - float 	-> user set grouping weigth
#			4 - list 	-> beat groupings remaining in current bar
#
# Outputs:	1 - float -> scaled probability
#	
def groupingScale( bReps, prob, gScale, groups ):
		groups = groups[:]
		c = 0
		l = float( len(groups) )
		# count through beats of groups
		for i in range( len(groups) ):
			c += groups[i]
			# if ioi == grouping scale up most, break
			if bReps == c:			
				scl = 1.0 - ( gScale * ( len(groups) - i )/len(groups) )
				prob = math.pow( prob, scl )
				break
			# if ioi < grouping scale up a bit, break
			elif bReps < c:
				scl = 1.0 - ( gScale * gScale * ( len(groups) - i )/len(groups) )
				prob = math.pow( prob, scl )
				break			
			# if ioi > grouping scale down a bit
			else:
				scl = 1.0 + ( gScale * gScale * gScale * (len(groups) - i ) / len(groups) )
				prob = math.pow(prob, scl)
		return prob

############################################################
     
# def ioiChooser
# This function randomly selects new inter onset intervals
# the choices are limited by the number of beats left in the phrase and
# the complexity of the output of the other voices
#
# Inputs: 	1 - int 	-> beats remaining in the phrase
#			2 - float 	-> current Level of Complexity
#			3 - float 	-> complexity Scale (0 - 1)
#			4 - float 	-> extent of group scaling (0 - 1)
#			5 - list 	-> remaining beat grouping in current bar
#			6 - list 	-> possible ioi's[base repetitions, ioi repetitions]
#			7 - list 	-> probabilities for each ioi
#
# Outputs: 	1 - list -> repetitions of base
#						repetitions of ioi
#
def ioiChooser( bRemaining, cLevel, cScale, gScale, groups, ioi, probs ):
		# copy so originals aren't changed
		ioi = ioi[:]
		probs = probs[:]
		groups = groups[:]
		#################################################
		# make sure length of ioi == length of probs
		###### shouldn't actually be necessary... #######
		if len(ioi) > len(probs):
			probs += [0.0] * (len(ioi) - len(probs))
		elif len(probs) > len(ioi):
			probs = probs[0:len(ioi)]
		#################################################
		# output base ioi if no complexity allowed
		if cScale == 0 or cLevel >= 1:
			return [1, 1, 0.0]
		# change probabilities for overlength and complex ioi's
		indices = []
		for x in range( len(ioi) ):
			# remove overlength ioi's
			if ioi[x][0] > bRemaining :
				probs[x] = 0.0
			# scale by complexity values
			else:
				probs[x] = complexityScale( probs[x], cLevel, cScale, ioi[x][2] )
			# if probability is 0 then add to list for later removal
			if probs[x] == 0.0:
				indices.append(x)
			# otherwise scale by grouping
			elif gScale > 0.0:
				probs[x] = groupingScale(bRemaining, probs[x], gScale, groups)
		# create list of possible ioi's and their probs
		indices.reverse() # reverse to avoid index shifting
		for i in indices:
			del probs[i]
			del ioi[i]
		# if there are no possible ioi's under current conditions output base ioi
		if len(ioi) == 0:
			return [1, 1, 0.0]
		# randomly select new ioi from remaining possibilities
		# gen random number and scale to total of probs
		r = random.random() * sum(probs)
		# change probs to position along number line for random decision
# 		p = probs[:]
		for x in range(1, len(probs) ):
			probs[x] = probs[x] +  probs[x-1]
		c = 0
		while probs[c] <= r:
			c += 1
		return ioi[c]

############################################################
############################################################
############################################################
############################################################
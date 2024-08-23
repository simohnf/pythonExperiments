import math
import random
import fractions

############################################################

# def factor
# This function determines the prime factors of an integer
#
# Inputs:	1 - int 	-> integer to be factored
#
# Outputs:	1 - list 	-> prime factors
#
def factor(n):
		if n == 1: return [1]
		i = 2
		limit = math.pow(n, 0.5)
		while i <= limit:
				if n % i == 0:
					ret = factor(n/i)
					ret.append(i)
					return ret
				i += 1
		return [n]		
############################################################
      
# def determineComplexity
# This function determines the complexity of a given 
# inter onset interval
#
# Inputs: 	1 - list 	-> inter onset interval as : [base repetitions, ioi repetitions]
#			
# Outputs: 	1 - int 	-> complexity
#
def determineComplexity(ioi):
		comp = []
		F = factor(ioi[0])
		F = list(set( F ))
		comp += F

		F = factor(ioi[1])
		F = list(set( F ))
		F = [ x for x in F ]
		comp += F
		comp = sum(comp) - 2
		return comp

############################################################

# def ioiMaker
# This function generates a list of possible inter-onset-intervals
# 
# Inputs: list of up to 3 integers denoting
#			1 - int 	-> depth of recursion
#			2 - int 	-> maximum base repetitions
#			3 - int 	-> maximum ioi repetitions
#
# Outputs: 	1 - list 	-> ioi's as [# Base Repetitions for synchronisation,
#							 # ioi repetitions, complexity level]
#
def ioiMaker( *vars ) :
        d = 8 # depth
        mBR = 1 # max base repetitions == d * mBR
        mIR = 1 # max ioi repetitions == d * mIR
        if len( vars ) >= 1 and vars[0] > 0 : d = vars[0]
        if len( vars ) >= 2 and vars[1] > 0 : mBR = vars[1]
        if len( vars ) >= 3 and vars[2] > 0 : mIR = vars[2]
        ioi = [] # list of ioi's as decimals for easy sorting
        out = [] # list of ioi's as fractions (i.e. ['base repetitions', 'ioi repetitions'])
        # nested for loops
        for x in range( 1, d + 1 ) :
            for y in range( 1, d + 1 ) :
                for z in range( 1, d + 1 ) :
                    z = float(z) # ensure maths will use decimals
                    delta = z / (x * y) # ioi as decimal
                    # limit ioi's by depth
                    if delta not in ioi and (( 1.0 / d ) <= delta <= d ) :
                        ioi.append( delta )
                    delta = (z * x) / y
                    if delta not in ioi and (( 1.0 / d ) <= delta <= d ) :
                        ioi.append( delta )
        # sort ioi's in descending order
        ioi.sort()
        ioi.reverse()
        # convert decimal ioi's to fractions
        for f in ioi:
            f = fractions.Fraction(f).limit_denominator()
            f = [f.numerator, f.denominator]
            # limit ioi's by maximum base and ioi repetitions
            if f[0] <= d * mBR and f[1] <= d * mIR : 
                out.append(f)
        # determine complexity of each ioi
        comps = []
        for d in range( len( out ) ):
        	comps.append(determineComplexity(out[d]))
        comps = [ float(x)/max(comps) for x in comps ]
        for x in range(len( out ) ):
        	out[x].append(comps[x])
        return out

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
############################################################
############################################################
############################################################

IOI = ioiMaker()
PROBS = []
import indispensability
bRemaining = 8

GROUPS = indispensability.genGrouping(bRemaining)
for x in IOI:
	if x[0] == 1 and x[1] == 1:
		PROBS.append(0.7)
	else:
		PROBS.append(0.7)

scales = []
lnth = 9
for x in range(lnth):
	scales.append(float(x)/ (lnth - 1) )

for s in scales:
	for l in scales:	
		cScale = s
		gScale = 0
		cLevel = l
		print '.................................'
		print 'cScale %.3f' % cScale,
		print 'cLevel %.3f' % cLevel,	
		test = IOI[:]
		test = [ [0] + x for x in test ]
		mlt = 1000
		lnth = mlt * len(test)
		for x in range(lnth):
			z = ioiChooser(bRemaining, cLevel, cScale, gScale, GROUPS, IOI, PROBS)
			test[IOI.index(z)][0] += 1

		test = zip(*test)
		test = zip(*test)
		test.sort()
		test.reverse()
		fHComp = 0.0
		sHComp = 0.0
		basePos = 0
		for x in range( len(test) ):
			if x <= len(test) / 2:
				fHComp += test[x][-1]
			else:
				sHComp += test[x][-1]
		fHComp = fHComp/( len(test) / 2 )
		sHComp = sHComp/( len(test) - ( len(test) / 2 ) )
		print 'max %.3f' % test[0][-1], 'min %.3f' % test[-1][-1], 
		print 'diff', (test[0][0] - test[-1][0]),
		if test[0][0] < lnth:
			print '	', 'avg comp: ', '%.3f' % fHComp, '|| %.3f' % sHComp,
		print ''
	print '..................................................................'
print '...................................................................................................'


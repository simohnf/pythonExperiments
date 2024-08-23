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
		if ioi[0] == 1:
			comp += [0]
		else:
			F = factor(ioi[0])
			F = list(set( F ))
			comp += F
		if ioi[1] == 1:	
			comp += [0]
		else:	
			F = factor(ioi[1])
			F = list(set( F ))
			F = [ x for x in F ]
			comp += F
		comp = sum(comp)
		print ioi, comp
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
        d = 6 # depth
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
        return out # base reps, ioi reps, comp

############################################################


print ioiMaker()
print len(ioiMaker()), "items"
import ioiMaker
import ioiChooser

IOI = ioiMaker.ioiMaker()
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
			z = ioiChooser.ioiChooser(bRemaining, cLevel, cScale, gScale, GROUPS, IOI, PROBS)
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


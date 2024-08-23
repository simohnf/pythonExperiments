def chromaticMedian(melody, nAllow):
	notes = sorted( list( set( [ n  for n in melody ] ) ) )
	scale = sorted( list( set( [ n  for n in nAllow ] ) ) )
	sprd = notes[-1] - notes[0]
	med = notes[0] + sprd/2
	if med in scale:
		return med
	else:
		for i in range(1, 6):
			if (med +i) in scale:
				med = med + i
				break
			elif (med -i) in scale:
				med = med + i
				break
	return med

def convert2Indices(melody, nAllow):
	indcs = []
	for n in melody:
		indcs.append( nAllow.index( n ) )
	return indcs
		
def tonal_Inversion(melody, nAllow):
	median = chromaticMedian(melody, nAllow)
	median = nAllow.index( median )
	indcs = convert2Indices(melody, nAllow)
	invrtd = []
	for n in indcs:
		invrtd.append( nAllow[median + ( median - n )] )
	return invrtd

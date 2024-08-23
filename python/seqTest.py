def convert2Indices( melody, nAllow ):
	indcs = []
	for n in melody:
		indcs.append( nAllow.index( n ) )
	return indcs
def expansion( mel, pcs, exp ):
	pcs = [p%12 for p in pcs]
	for p in mel:
		if (p%12) not in pcs:
			pcs.append(p)
	pcs = sorted(list(set(pcs)))
	posN = pcs[:]
	count = 1
	while min(mel) < min(posN):	
		posN += [ (n - (12*count)) for n in pcs ]
		count += 1
		posN = sorted(list(set(posN)))
	count = 1
	while max(mel) > max(posN):	
		posN += [ (n + (12*count)) for n in pcs ]
		count += 1
	posN = sorted(list(set(posN)))
	indcs = convert2Indices( mel, posN )
	indcsN = [ ((i -indcs[0])*exp) + indcs[0] for i in indcs ]
	while max(indcsN) >= len(posN):
		posN += [ (n + (12*count)) for n in pcs ]
		count += 1
		posN = sorted(list(set(posN)))
	print indcsN
	expOut = [posN[i] for i in indcsN]
	return expOut
cell = [ 5, 0, 7 ]
mel = [ 5, 0, 7, 5, 7, 8, 10 ]
pcs = [0, 2, 3, 5, 7, 8, 10]
# pcs = []
print
exp = 2
expansion( mel, pcs, exp )

print
exp = 3
expansion( mel, pcs, exp )
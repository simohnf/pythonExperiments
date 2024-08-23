import math
import time
import random

class stepSeq( object ):
		def __init__( self ):
			self.seq = []
			self.pTime = time.clock() * 10000
			self.seqState = False
			self.droneState = True
			self.Step = 0
			self.droneStep = 0
			self.seq_pTime = 0
			self.minTouches = 6

####################################################
		def sensorPress( self, b, state ):
			# record button on's
			if state > 0 :
				self.droneState = True
				bTime = time.clock() * 10000
				if len( self.seq ) == 0 :
					self.seq.append([b, 0])
					self.pTime = bTime
				else:
					tm = bTime - self.pTime
					# make first 2 inter onset intervals the same
					if len(self.seq) == 1:
						self.seq[0][1] = tm 
					self.seq.append([b, ( tm ) ] )
					self.pTime = bTime
			# record button off's
			else:
				for x in range( len( self.seq ) ) :
					if self.seq[x][0] == b:
						print self.droneState,'				kill', self.seq[x]
						del self.seq[x]
						break
			if len( self.seq ) >= self.minTouches:
				if self.seqState == False:
					self.seqState = True
					self.Step = 0
					self.seq_pTime = bTime
			else:
				if self.seqState == True:
					self.seqState = False
					self.droneState = True
					self.droneStep = 0


####################################################
		def runSequence( self ):
			if self.Step > len(self.seq):
				self.Step = 0
			if self.seqState == False:
				if self.droneState == True:
					if len(self.seq) == 0: return
					currentTime = time.clock() * 10000
					actualIndex = (self.Step + self.droneStep) % len(self.seq)
					nextStep = self.seq[actualIndex - 1][1] + self.seq_pTime
					if currentTime >= nextStep:
						print '		dron', self.seq[actualIndex - 1]
						self.seq_pTime = currentTime
						self.droneStep += 1
					if self.droneStep >= len(self.seq):
						self.droneState = False
# 				print "kill notes"
			else:
				currentTime = time.clock() * 10000
				nextStep = self.seq[self.Step - 1][1] + self.seq_pTime
				if currentTime >= nextStep:
					print '			note', self.seq[self.Step - 1], len(self.seq)
					self.seq_pTime = currentTime
					self.Step += 1
					self.Step % len(seq.seq)
			
####################################################					
seq = stepSeq()	



pTime = (time.clock() * 10000)
run4 = 100
for x in range(run4):
		while ( time.clock() * 10000 - pTime ) < 1000:
			seq.runSequence()
		if x >= ( run4 - len( seq.seq ) ):
			b = seq.seq[-1][0]
			st = 0
		else:
			b = random.randrange(0, 20)
			st = 1
			for x in seq.seq:
				if x[0] == b:
					st = 0
					break
		seq.sensorPress(b, st)
		pTime = (time.clock() * 10000)
print '..........................................'

for x in range(run4):
		while ( time.clock() * 10000 - pTime ) < 1000:
			seq.runSequence()
		if x >= ( run4 - len( seq.seq ) ):
			b = seq.seq[-1][0]
			st = 0
		else:
			b = random.randrange(0, 20)
			st = 1
			for x in seq.seq:
				if x[0] == b:
					st = 0
					break
		seq.sensorPress(b, st)
		pTime = (time.clock() * 10000)

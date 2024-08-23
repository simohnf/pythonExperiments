from __future__ import division
from fractions import Fraction

try:
        import pyext
except:
        print "ERROR: This script must be loaded by the PD/Max pyext external"

import math
import time
import random

class stepSeq( pyext._class ):
		print 'Sequencer.....'
		_inlets = 1
		_outlets = 1
		def __init__( self, *args ):
			self.seq = []
			self.tScale = 1000
			self.pTime = time.clock() * self.tScale
			self.seqState = False
			self.droneState = False
			self.Step = 0
			self.droneStep = 0
			self.seq_pTime = 0
			self.minTouches = 3
			if len(args) > 0 and args[0] > 1:
				self.minTouches = args[0]
			self.nextStep = 0
			self.killnotes = []
			self.releaseTimes = []


####################################################
		def button_1( self, b, state ):
			# record button on's
			if state > 0 :
				bTime = time.clock() * self.tScale
				if len( self.seq ) == 0 :
					self.seq.append([b, 0, 0])
					self.pTime = bTime
				else:
					tm = bTime - self.pTime
					if len(self.seq) > 1:
						mx = max(zip(*self.seq)[1])
						if tm > mx * 3.0:
							tm = mx * 3.0
					# make first 2 inter onset intervals the same
					if len(self.seq) == 1:
						self.seq[0][1] = tm 
						self.seq[0][2] = tm 
					# append note to sequence
					print 'tm', tm
					self.seq.append( [ b, tm, tm ] )
					# rewrite lnth and delta times to allow chords
					if len(self.seq) >= 2:
						if 100 > self.seq[-1][2] < self.seq[-2][2] * 0.25:
							self.seq[-1][2] = self.seq[-2][2]
							tmp = self.seq[-2][1]
							self.seq[-2][1] = self.seq[-1][1]
							self.seq[-1][1] = tmp
# 					self.seq[-2][1] = tm
					self.pTime = bTime
				# play notes
				if self.seqState == False:
					if len(self.seq) >= (self.minTouches - 1):
						self._outlet( 1, 'noteon', b, tm)
					else:
						self._outlet( 1, 'noteon', b )
			# record button off's
			else:
				# if sequencer is off just kill note 
				if self.seqState == False:
					indx = zip( *self.seq)[0].index(b)
					self._outlet( 1, 'noteoff', self.seq[indx] )
				# otherwise add to list to kill later
				else:
					indx = zip( *self.seq)[0].index(b)
					self.killnotes.append(self.seq[indx])
				# delete note from sequence
				for x in range( len( self.seq ) ) :
					if self.seq[x][0] == b:
						del self.seq[x]
						break
			# Turn sequencer on or off
			# If minimum touches reached turn on sequencer
			if len( self.seq ) >= self.minTouches:
				if self.seqState == False:
					for x in self.seq[0:-1]:
						self._outlet( 1, 'noteoff', x[0], x[1] )
					self.seqState = True
					self.Step = 0
					self.nextStep = self.seq[- 1][1] + time.clock() * self.tScale
					self.seq_pTime = bTime
			# otherwise turn sequencer off
			else:
				if self.seqState == True:
					self.seqState = False
					self.droneState = True
					self.droneStep = 0
			# for safety kill notes
			if len(self.seq) == 0:
				for x in range(8):
					self._outlet( 1, 'noteoff', x )

####################################################
		def run_1( self ):
			if self.seqState == False:
				if self.droneState == True:
					if len(self.seq) == 0: return
					currentTime = time.clock() * self.tScale
					actualIndex = (self.Step + self.droneStep + 1) % len(self.seq)
					nextStep = self.seq[actualIndex - 1][1] + self.seq_pTime
					if currentTime >= nextStep:
						self.seq_pTime = currentTime
						self.droneStep += 1
						self._outlet( 1 , 'noteon', self.seq[actualIndex - 1][0], self.seq[actualIndex - 1][2] )
						# remove any hanging notes
						for x in self.killnotes:
							self._outlet( 1, 'noteoff', x[0], x[1] )	
						self.killnotes = []
					if self.droneStep >= len(self.seq):
						self.droneState = False
			else:
				currentTime = time.clock() * self.tScale
				if len(self.releaseTimes) >= 1:
					for x in range( 1, (len(self.releaseTimes)) + 1 ):
						pos = len(self.releaseTimes) - x
						if self.releaseTimes[ pos ][0] <= currentTime:
							self._outlet( 1 , 'noteoff', self.releaseTimes[ pos ][1], self.releaseTimes[ pos ][3] )
							del self.releaseTimes[ pos ]
				if self.Step >= len(self.seq):
					self.Step = 0
				if currentTime >= self.nextStep:
					# remove any hanging notes
					for x in self.killnotes:
						self._outlet( 1, 'noteoff', x[0], x[1] )	
					self.killnotes = []	
					self._outlet( 1, 'noteon', self.seq[self.Step][0], self.seq[self.Step][2] )
					tm = currentTime + self.seq[self.Step][2]
					rls = [tm] + self.seq[self.Step]
					self.releaseTimes.append(rls)
					self.seq_pTime = currentTime
					self.Step += 1
					self.Step = self.Step % len(self.seq)
					self.nextStep = self.seq[self.Step - 1][1] + self.seq_pTime
			
####################################################					
# seq = stepSeq()	
# 
# 
# 
# pTime = (time.clock() * 10000)
# run4 = 100
# for x in range(run4):
# 		while ( time.clock() * 10000 - pTime ) < 1000:
# 			seq.runSequence()
# 		if x >= ( run4 - len( seq.seq ) ):
# 			b = seq.seq[-1][0]
# 			st = 0
# 		else:
# 			b = random.randrange(0, 20)
# 			st = 1
# 			for x in seq.seq:
# 				if x[0] == b:
# 					st = 0
# 					break
# 		seq.sensorPress(b, st)
# 		pTime = (time.clock() * 10000)
# print '..........................................'
# 
# for x in range(run4):
# 		while ( time.clock() * 10000 - pTime ) < 1000:
# 			seq.runSequence()
# 		if x >= ( run4 - len( seq.seq ) ):
# 			b = seq.seq[-1][0]
# 			st = 0
# 		else:
# 			b = random.randrange(0, 20)
# 			st = 1
# 			for x in seq.seq:
# 				if x[0] == b:
# 					st = 0
# 					break
# 		seq.sensorPress(b, st)
# 		pTime = (time.clock() * 10000)

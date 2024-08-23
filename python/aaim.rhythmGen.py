import math
import random
import indispensability
import ioiMaker
import fractions
print "AAIM performance system"
print "	simonjohnfay 2015"

class rGenAgent( object ):
 		def __init__(self, ref, *args):
				self.parent = ref
				self.nBeats = self.parent.nBeats
				self.nBars = self.parent.nBars
				self.complexity = 0.0
				self.rests = 0.0 # probability of rests being included
				self.tempo = 1.0 # tempo as scale of global tempo
				self.deviation = 0.0 # micro deviations in timing from global timing
				self.gPenalty = 0.0 # scaling of probabilities according to underlying grouping
				self.grouping = self.parent.grouping # underlying grouping
				self.barWeight = 1.0 # overall indispensability of beats in bar according to phrase
				self.probs = [0.0 for x in self.ioi] # probability of inter onset intervals
				for x in range( len(self.ioi) ):
						if self.parent.ioi[x] == [1,1]:
								self.probs[x] = 1.0
								self.currentIOI = self.parent.ioi[x]
				self.state = False # turn voice off
				# currentPosition in bar & phrase
				self.currentBar = 0	
				self.pPosition = 0.0
		
		def position( self, p ):
				p = (p * self.tempo) + (self.deviation * self.parent.deviation) 
				p = p % (self.nBeats * self.nBars)
				# record when "phase" loops
				if p < self.pPosition:
					self.currentBar = (self.currentBar + 1) % self.nBars
				self.pPosition = p	
				return 			
		def chooseNewIOI( self, p ):
				rBeats = ( self.nBeats * self.nBars ) - p
				tempProbs = self.probs
				complexCount = 0
				for a in self.parent.agents:
					# count complex ioi's in use
					if a.currentIOI[0] > 2 or a.currentIOI[1] > 2:
						complexCount += 1				
				maxComplexity = self.parent.nVoices * self.complexity
				# remove overlength ioi's
				for x in len(tempProbs):
					if self.parent.ioi[x][0] > rBeats:
						tempProbs[x] = 0.0
					# remove complex ioi's in case of over complexity
					if complexCount >= maxComplexity:
						if self.parent.ioi[x][0] > 2 or self.parent.ioi[x][1] > 2:
							tempProbs[x] = 0.0					
class rhythmGen( object ):
		def __init__( self, *args ):
				print "AAIM.rhythmGen"
				print "	simonjohnfay 2015"
				# set number of beats in bar
				self.nBeats = 16
				if len(args) > 1 and args[1] >= 1:
					self.nBeats = args[1] 	
				self.nBars = 4
				if len(args) > 2 and args[2] >= 1:
					self.nBars = args[2] 
				self.complexity = 0.0 # global complexity level
				self.deviation = 0.0 # extent of deviations
				self.rests = 0.0 # probability of rests being included
				self.grouping = indispensability.genGrouping( self.nBeats )
				self.barIndis = indispensability.indis( self.nBars ) # overall indispensability of beats in bar according to phrase
				self.ioi = ioiMaker.ioi() # list of possible inter onset intervals
				# set number of agents/rhythmic voices
				self.nVoices = 1 
				if len(args) > 0 and args[0] >= 1:
					self.nVoices = args[0] 	
				# initialise agents		
				self.agents = []
				for x in range( self.nVoices ):
					self.agents.append( rGenAgent(self) )
				# currentPosition in bar & phrase
				self.currentBar = 0	
				self.pPosition = 0.0
		# functions for changingVariables
		def beats( self, n ):
				if n > 0:
					self.nBeats = n
					self.grouping = indispensability.genGrouping( self.nBeats ) # underlying grouping
					for a in self.agents:
						a.nBeats = n
						a.grouping = self.grouping
		def bars( self, n ):
				if n > 0:
					self.nBars = n
					for a in self.agents:
						a.nBars = n
					self.barIndis = indispensability.indis( self.nBars )
		def globalComplexity( self, n ):
				if n < 0.0: n = 0.0
				elif n > 1.0: n = 1.0
				n = float(n)
				self.complexity = n
				for a in self.agents:
					a.complexity = self.complexity * a.complexity
		def voiceComplexity( self, v, n ):
				if n < 0.0: n = 0.0
				elif n > 1.0: n = 1.0
				n = float(n) * self.complexity
				if v <= 0 or v > len( self.agents ) + 1:
					for a in self.agents:
						a.complexity = n 
				else:
					self.agents[v - 1].complexity = n	
		def globalRests( self, n ):
				if n < 0.0: n = 0.0
				elif n > 1.0: n = 1.0
				n = float(n)
				self.rests = n
		def voiceRests( self, v, n ):
				if n < 0.0: n = 0.0
				elif n > 1.0: n = 1.0
				n = float(n)
				if v <= 0 or v > len( self.agents ) + 1:
					for a in self.agents:
						a.rests = n
				else:
					self.agents[v - 1].rests = n	
		def globalGrouping( self, *n ):
				n = list(n)
				if len(n) > 0 and sum( n ) >= 1:
					self.nBeats = sum( n )
					for a in self.agents:
						a.nBeats = sum( n )
						a.grouping = n
		def voiceTempo( self, v, n ):
				if n <= 0: return
				n = float(n)
				if v <= 0 or v > len( self.agents ) + 1:
					for a in self.agents:
						a.tempo = n
				else:
					self.agents[v - 1].tempo = n
		def globalDeviation( self, n ):
				if n < 0.0: n = 0.0
				elif n > 1.0: n = 1.0
				n = float(n)
				self.deviation = n
		def voiceDeviation( self, v, n ):
						if n <= -0.5: n = -0.5
						elif n >= 0.5: n = 0.5
						n = float(n)
						if v <= 0 or v > len( self.agents ) + 1:
							for a in self.agents:
								a.deviation = n
						else:
							self.agents[v - 1].deviation = n
		def voiceState( self, v, n ):
						if n < 1: n = False
						elif n >= 1: n = True
						if v <= 0 or v > len( self.agents ) + 1:
							for a in self.agents:
								a.state = n
						else:
							self.agents[v - 1].state = n
		def voiceProbs( self, v, n ):
				# ensure min probability is 0
				for i in range(len(n)):
					if n[i] < 0.0: n[i] = 0.0
				# normalise if max prob > 1
				if max(n) > 1.0:
					n = [(x/max(n)) for x in n]
				if v <= 0 or v > len( self.agents ) + 1:
					for a in self.agents:
						for i in range(len(n)):
							if i <= len(a.probs):
								a.probs[i] = n[i]
				else:
					for i in range(len(n)):
						if i <= len(self.agents[v - 1].probs):
							self.agents[v - 1].probs[i] = n[i]	
		# function to do the magic						
		def position( self, p ):
			p = p % self.nBeats
			# count progression of bars
			if p < self.pPosition:
				self.currentBar = (self.currentBar + 1) % self.nBars
				for a in self.agents:
					a.barWeight = self.barIndis[self.currentBar]
			# randomly choose starting voice to prevent over variation in one voice
			r = random.randrange(self.nVoices)
			for a in range(self.nVoices):
				x = (a + r) % self.nVoices
				self.agents[x].position( p + (self.currentBar * self.nBeats))
			self.pPosition = p
 				
x = rhythmGen(2, 8, 4)
x.position(0.1)

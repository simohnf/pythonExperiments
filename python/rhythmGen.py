from __future__ import division
from fractions import Fraction

try:
        import pyext
except:
        print "ERROR: This script must be loaded by the PD/Max pyext external"

import math
import numpy
import random
import MARKOV




class rhythmGen(pyext._class):
        print "hello Max this is my rhythm generator"
        # number of inlets and outlets
        _inlets=1
        _outlets=2

        def __init__(self, *args):
                nVoices = 1
                if len(args) == 1 :
                    nVoices = max( int(args[0]), 1 )
                                        ## holds :[note length in comparison to pulse,
                self.noteLengths = []	##			number of repetitions OF BASE before sync,
                                        ##			probability,]
                self.voices = []
                for x in range(nVoices):
                        self.voices.append(MultiTrigger(self))
                        self.voices[x].noteLengths = self.noteLengths
                self.globalMarkov = MARKOV.markov()
                self.maxComplexity = 0.1
                self.lastPos = -1
                self.numBars = 1
                self.nBeats = 8
                self.baseRhythm = 1
                self.currentBar = 0
                self.nBars = 1
                self.probs = []
                self.noteLengthSetup(4, 5, 2)
                self.numBeats_1(8)
                self.determineLengthNames(2)
                
                # this sets what action to take when there is no possible delta choice
                # 0 -> do nothing; 1 -> choose base rhythm; 2 -> use user set probabilities
                self.noChoiceAction = 0 
        def numVoices_1( self , nVoices ) :
                if nVoices < 1:
                    nVoices = 1
                if nVoices == len(self.voices):
                        pass
                elif nVoices > len(self.voices):
                        newVoices = nVoices - len(self.voices)
                        self.voices = self.voices + [MultiTrigger(self) for x in range(newVoices)]
                        for x in range(newVoices):
                                self.voices[ - (x + 1) ].noteLengths = self.noteLengths
                else:
                        self.voices = self.voices[0:nVoices]
        def changeProbs(self, beatsLeft, voiceX):
                count = 0
                self.probs = [row[2] for row in self.noteLengths]
                for x in self.noteLengths:
                        if x[1] > beatsLeft:
                                self.probs[count] = 0
                        count = count + 1
                totalProbs = sum(self.probs)
                if totalProbs == 0:
                        if self.noChoiceAction == 0: pass
                        elif self.noChoiceAction == 1:
                                for x in range( 0, len(self.noteLengths ) ) :
                                        if self.noteLengths[x][0] == 1:
                                                self.probs[x] = 1
                        elif self.noChoiceAction == 2:
                                self.probs = [row[2] for row in self.noteLengths]
                        return
        # limits the probabilities of fast IOI's or 'arhythmic' IOI's
        # when too many are already being played
                ### if the overall complexity level is set to 0
                ### only allow 1.0 times the beat
                if self.maxComplexity == 0 or self.voices[voiceX].complexityScaler == -1:
                        for x in range(len(self.noteLengths)):
                                if self.noteLengths[x][0] == 1:
                                        self.probs[x] = 1
                                else:
                                        self.probs[x] = 0
                        return
                count = 0
                count2 = 0
                for child in self.voices:
                        if self.noteLengths[child.choiceIndex][0] < 0.5:
                                count = count + 1
                        # get rid of "arhythmic" values if other 
                        for y in range(0, 10):
                                if ( ( (self.noteLengths[child.choiceIndex][3]._numerator * pow(2, y)) / self.noteLengths[child.choiceIndex][3]._denominator ) % 1) == 0:
                                        count2 += 1
                                        break
                count2 = len(self.voices) - count2
                currentComplexity = count / len(self.voices)
                currentComplexity = max(0, min(currentComplexity - self.voices[voiceX].complexityScaler, 1)) 
                if currentComplexity > self.maxComplexity:
                        for i in range(len(self.noteLengths)):
                                if self.noteLengths[i][0] < 0.5:
                                        self.probs[i] = 0

                currentComplexity = count2 / len(self.voices)
                currentComplexity = max(0, min(currentComplexity - self.voices[voiceX].complexityScaler, 1)) 
                if currentComplexity > self.maxComplexity:
                        for i in range(len(self.noteLengths)):
                                c = 0
                                for y in range(0, 10):
                                        if ( ( (self.noteLengths[i][3]._numerator * pow(2, y)) / self.noteLengths[i][3]._denominator ) % 1) == 0:
                                                c = 1
                                                break
                                if c == 0:
                                        self.probs[i] = 0
                # check if there are still possible delta choices
                # if not make decision on what to do
                if sum(self.probs) == 0:
                        if self.noChoiceAction == 0: pass
                        elif self.noChoiceAction == 1:
                                for x in range( 0, len(self.noteLengths ) ) :
                                        if self.noteLengths[x][0] == 1:
                                                self.probs[x] = 1
                        elif self.noChoiceAction == 2:
                                self.probs = [row[2] for row in self.noteLengths]
                        return;
        def float_1(self, f):
#                 check if beat has changed and if so determine probabilities
                if int( f ) != self.lastPos:
                        if int( f ) == 0:
                                self.currentBar = ( self.currentBar + 1 ) % self.nBars
                                self._outlet( 2 , 'rhythBar', self.currentBar)
                        beatsLeft =  (self.nBeats) * ( self.nBars - self.currentBar) - int( f ) 
                for x in range (len(self.voices)):
                        if int ( f ) != self.lastPos:
                            self.changeProbs( beatsLeft, x )
                        result = self.voices[x].beatInput( f )
                        outTime = result[0]
                        division = result[1]
                        if outTime >= 0:
                                self._outlet( 1, x , outTime , division);
                self.lastPos = int( f )
        def noteLengthLogic_1( self , maxDivision, nLevels, baseRhythm):
                self.noteLengthSetup(maxDivision, nLevels, baseRhythm)
                names = self.determineLengthNames(baseRhythm)
                self._outlet(2, "lengthNames", names)
                self._outlet(2, "probabilities", self.probs)
        def numBeats_1(self, nBeats):
                if nBeats <= 1:
                        nBeats = 1
                self.nBeats = int(nBeats)
                for x in self.voices:
                        x.nBeats = self.nBeats
        def noteLengthSetup(self, maxDivision, nLevels, baseRhythm):
                oldBase = self.baseRhythm
                oldLengths = self.noteLengths[:]
                self.baseRhythm = baseRhythm
                self.noteLengths = []
                for x in range(0, nLevels):
                        for y in range(0, maxDivision):
                                if y == 0:
                                        newDivision = (2.0/math.pow(2, x)) * baseRhythm
                                        if newDivision not in self.noteLengths:
                                                self.noteLengths.append(newDivision)
                                elif y == 1:
                                        newDivision = (1.5/math.pow(2, x)) * baseRhythm 
                                        if newDivision not in self.noteLengths:
                                                self.noteLengths.append(newDivision)
                                else:
                                        if y > 3:
                                                newDivision = ((8.0/(y+1))/math.pow(2, x)) * baseRhythm
                                        else:
                                                newDivision = ((4.0/(y+1))/math.pow(2, x)) * baseRhythm
                                        if newDivision not in self.noteLengths:
                                                self.noteLengths.append(newDivision)
                self.noteLengths.sort(reverse = True)
                for x in range(0, len(self.noteLengths)):
                        if (self.noteLengths[x] % 1.0) == 0:
                            self.noteLengths[x] = [self.noteLengths[x], self.noteLengths[x]]
                        else:
                                check = self.noteLengths[x]
                                for count in range(1, 1000):
                                        check = self.noteLengths[x] * count
                                        if check % 1.0 == 0:
                                                break
                                self.noteLengths[x] = [self.noteLengths[x], check]
                        if self.noteLengths[x][0] == 1:
                                self.noteLengths[x] = self.noteLengths[x]+[1]
                        else:
                                self.noteLengths[x] = self.noteLengths[x]+[0]
                # transfer probabilities from previous settings
                # to current
                for x in oldLengths:
                        for i in self.noteLengths:
                                if x[0] *(self.baseRhythm / oldBase) == i[0]:
                                        i[2] = x[2]
                self.probs = [row[2] for row in self.noteLengths]
        def determineLengthNames(self, baseRhythm):
                lengthNames = []
                for x in range(0, len(self.noteLengths)):
                        testVal  = (int(float(self.noteLengths[x][1]/self.noteLengths[x][0]) * 4)) * baseRhythm
                        tVal = int(self.noteLengths[x][1])
                        thisName = Fraction(tVal, testVal)
                        lengthNames.append(str(thisName))
                        self.noteLengths[x].append(thisName)
#                         print self.noteLengths[x]
#                         print self.noteLengths[x][-1], self.noteLengths[x][-1]._denominator
                return lengthNames;
        def rhythmProbabilities_1(self, *probs):
                ### probabilities should be given as 
                ### just the list of probs	
                for x in range(0, len(probs)):
                        self.noteLengths[x][2] = probs[x]
        def numBars_1(self, nBars):
                if nBars < 1: self.nBars = 1
                else: self.nBars = nBars
        def setComplexity_1(self, complexity):
                if 0 <= complexity <= 1:
                        self.maxComplexity = complexity
                else: self.maxComplexity = 0
        def currentBar_1(self, bar):
                self.currentBar = (bar % self.nBars)
        def voiceComplexity_1(self, voice, complexityScaler):
                if -1 <= complexityScaler <= 1:
                    self.voices[voice].complexityScaler = complexityScaler
        def noDeltaChoice_1(self, action):
            if 0 <= action <= 2:
                self.noChoiceAction = action;
        def reloadModules_1(self):
            import math
            import numpy
            import random
            import MARKOV

#
# MultiTrigger - multiple-evenly spaced phase triggers
#
class MultiTrigger(object):
    def __init__( self, reference, *args ) :
        self.parent = reference
        self.nThresholds = 1
        if len(args) == 1 :
            self.nThresholds = max( int(args[0]), 1 )
        self.thresholds = [ float(i) / float(self.nThresholds) for i in range(self.nThresholds) ]
        self.last = 0.0
        self.beginning = 0
        self.end = 1
        self.divider = 1
        self.nBeats = 8
        self.choiceIndex = 0
        self.complexityScaler = 0
        self.markov = MARKOV.markov()
    def beatInput( self , f ) :
        # decide whether or not to choose a new ioi length
        # and if so reset nThresholds, beginningPoint, endPoint
        # divider, and choiceIndex
        if f >= (self.end) :
                ioiChoice = self.choose_IOI(self.parent.probs)
#                 print 'greater than, chose ', ioiChoice
        elif self.end >= self.nBeats:
                if 0 <=f < 1:
                        ioiChoice = self.choose_IOI(self.parent.probs)
#                         print 'greater than, chose ', ioiChoice
        try:
            self.choiceIndex = ioiChoice
            self.beginning = math.floor( f )
            self.divider = self.parent.noteLengths[self.choiceIndex][1]
            self.end = ( self.parent.noteLengths[self.choiceIndex][1] ) + self.beginning
            self.ndiv( self.parent.noteLengths[self.choiceIndex][1] / self.parent.noteLengths[self.choiceIndex][0])
        except: pass
        
        phaseSinceStart = (f - self.beginning)
        phaseSinceStart = (phaseSinceStart / self.divider) % 1.0
        out = self.float(phaseSinceStart) # returns -1 if no note, other wise threshold count
        if out >= 0: 
                return [(out * self.parent.noteLengths[self.choiceIndex][0]) + self.beginning, self.parent.noteLengths[self.choiceIndex][0]];
        else: return [out, -1]
    def float( self, f ) :
        outPut = -1
        # assume f increases every call, except for wrap
        if f > self.last :
#             print "first One"
            # f has increased
            for i in range(len(self.thresholds)) :
                if self.last < self.thresholds[i] <= f :
                    # last and f bracket the threshold, so outlet something
                    outPut = i ;
        elif (self.last -f) < 0.5 :
            # phase decreased, but not because of phase wrap, do nothing
            pass
        else :
            # must have had phase wrap so if f and last do not bracket then outlet
            for i in range(len(self.thresholds)) :
                if not f <= self.thresholds[i] < self.last :
                    outPut = i ;
        self.last = f
        return outPut
    def choose_IOI( self, probs ) : 
        probInfo = probs[:]
        rand = random.random() * sum(probInfo)
        count = 0
        for x in range(0, len(probInfo)):
                count += probInfo[x]
                if rand < count:
                        return x
        return 0
    def ndiv( self, f ) :
        self.nThresholds = max( int(f), 1 )
        self.thresholds = [ float(i) / float(self.nThresholds) for i in range(self.nThresholds) ]
    def dump( self ) :
            return self.thresholds ;















class rhythmGenOLD(pyext._class):
        print "hello Max this is my rhythm generator"
        # number of inlets and outlets
        _inlets=1
        _outlets=2
    
        def __init__(self):
    # 				print 'breakPoint __init__ rhythm'
                                        ## holds :[note length in comparison to pulse,
                self.noteLengths = []	##			number of repetitions OF BASE before sync,
                                        ##			probability,]
                self.voices = [[0, 1, 1, 0]] 	## holds: [beginning, syncPoint, value, previousState]
                self.patternList = [8]
                self.maxDivisions = 5
                self.numLevels = 4
                self.baseRhythm = 1
                self.overallComplexity = 0.1
                self.lastPos = -1
                self.numBars = 1
                self.numBeats = 8
                self.noteLengthSetup(4, 5, 2)
                self.numVoices_1(10)

        def generateNewNotelength(self, *probs):
    # 				print 'BREAKPOINT!!! RhythmGen generateNewNotelength'
                rand = random.random()
                probInfo = probs[:]
                probInfo = probInfo[0]
                count = 0
                for x in range(0, len(probInfo)):
                        count += probInfo[x]
                        if rand < count:
                                return x
                return 0

        ### takes the number of beats left
        ### and gives back a list of probabilities 
        ### for possible note lengths
        def changeProbabilities(self, numBeatsLeft):
                self.noteLengths
                changedNoteLengthProbs = self.noteLengths[:]
                probs = [row[2] for row in self.noteLengths]
                totalProbs = 0
                for x in range(0, len(changedNoteLengthProbs)):
                        if self.noteLengths[x][1] > numBeatsLeft:
                                probs[x] = 0
                        totalProbs += probs[x]
                newCount = 0
                if totalProbs > 0:
                        for x in range(0, len(changedNoteLengthProbs)):
                                probs[x] = probs[x]/totalProbs
                                newCount += probs[x]
                else:
                        for x in range(0, len(self.noteLengths)):
                                if self.noteLengths[x][0] == 1:
                                        probs[x] = 1
                return probs

        #### this takes the voice number to be checked
        #### looks at all the other voices and if a certain 
        #### percentage of them already creating a notelength
        #### grouping under half the baseRhythm don't allow anything
        #### less than half the base rhythm
        def limitVoiceProbabilities(self, voiceNumber, *originalProbabilities):
    # 				print 'BREAKPOINT!!! RhythmGen limitVoiceProbabilities'
                voiceProbs = originalProbabilities[0][:]
                ### if the overall complexity level is set to 0
                ### only allow 1.0 times the beat
                if self.overallComplexity == 0:
                    for x in range(0, len(self.noteLengths)):
                            if self.noteLengths[x][0] == 1:
                                    voiceProbs[x] = 1
                            else:
                                    voiceProbs[x] = 0	
    
                else:
                        count = 0
                        ### go through each voice and count how many are playing 'fast'
                        ### notes
                        for x in range(0, len(self.voices)):
                                if x != voiceNumber:
                                        if self.voices[x][2] < 0.5:
                                                count += 1
                        ### compare the number of voices playing fast beats
                        ### to the stated limit and if too many voices are 
                        ### already playing fast notes don't let this voice
                        currentSpeedRating = float(count/len(self.voices))
                        if currentSpeedRating > self.overallComplexity:
                                adder = 0
                                for x in range(0, len(voiceProbs)):
                                        if self.noteLengths[x][0] < 0.5:
                                                voiceProbs[x] = 0
                                        adder += voiceProbs[x]
                                if adder > 0:
                                        for x in range(0, len(voiceProbs)):
                                                voiceProbs[x] = voiceProbs[x]/adder
                                else:
                                        for x in range(0, len(self.noteLengths)):
                                                if self.noteLengths[x][0] == 1:
                                                        voiceProbs[x] = 1 
                        count = 0
                        ### go through each voice and count how many are playing 
                        ### note lengths which are 'arhythmic'
                        for x in range(0, len(self.voices)):
                                if x != voiceNumber:
                                        voiceValue = self.voices[x][2]
                                        minicount = 0
                                        for y in range(0, 6):
                                                if (voiceValue * pow(2, y) % 1) == 0:
                                                        if minicount == 0:
                                                                count += 1
                                                                minicount = 1
                        ### compare the number of voices playing "complex" beats
                        ### to the stated limit and if too many voices are 
                        ### already playing fast notes don't let this voice
                        currentComplexityRating = float((len(self.voices)-1-count)/len(self.voices))
                        if currentComplexityRating > self.overallComplexity:
                                adder = 0
                                for x in range(0, len(self.noteLengths)):
                                        if (self.noteLengths[x][0] * pow(2, 6) % 1) != 0:
                                                voiceProbs[x] = 0
                                        adder += voiceProbs[x]
                                if adder > 0:
                                        for x in range(0, len(voiceProbs)):
                                                voiceProbs[x] = voiceProbs[x]/adder
                                else:
                                        for x in range(0, len(self.noteLengths)):
                                                if self.noteLengths[x][0] == 1:
                                                        voiceProbs[x] = 1 
                return voiceProbs

        def noteLengthSetup(self, mxDivision, noLevels, bRhythm):
    # 				print 'BREAKPOINT!!! RhythmGen noteLengthSetup'
                self.maxDivisions = mxDivision
                self.numLevels = noLevels
                self.baseRhythm = bRhythm
                x = 0
                self.noteLengths = []
                for x in range(0, len(self.noteLengths)):
                        self.noteLengths.pop(x)
                x = 0
                for x in range(0, self.numLevels):
                        y = 0
                        for y in range(0, self.maxDivisions):
                                if y == 0:
                                        newDivision = 2.0/math.pow(2, x)
                                        newDivision = newDivision * self.baseRhythm
                                        if newDivision not in self.noteLengths:
                                                self.noteLengths.append(newDivision)
                                elif y == 1:
                                        newDivision = 1.5/math.pow(2, x) 
                                        newDivision = newDivision * self.baseRhythm
                                        if newDivision not in self.noteLengths:
                                                self.noteLengths.append(newDivision)
                                else:
                                        if y > 3:
                                                newDivision = (8.0/(y+1))/math.pow(2, x)
                                                newDivision = newDivision * self.baseRhythm
                                        else:
                                                newDivision = (4.0/(y+1))/math.pow(2, x)
                                                newDivision = newDivision * self.baseRhythm
                                        if newDivision not in self.noteLengths:
                                                self.noteLengths.append(newDivision)
                self.noteLengths.sort(reverse = True)
                lengthNames = []
                x = 0
                modulo = 1.0
                for x in range(0, len(self.noteLengths)):
                        if (self.noteLengths[x] % modulo) == 0:
                            self.noteLengths[x] = [self.noteLengths[x], self.noteLengths[x]]
                        else:
                                check = self.noteLengths[x]
    # 								print "self.noteLengths[x]", self.noteLengths[x]
                                for count in range(1, 1000):
                                        check = self.noteLengths[x] * count
                                        if check % 1.0 == 0:
                                                break
    # 							    count = 1
    # 								while check % 1.0 != 0 :
    # 										count += 1
    # 										check = self.noteLengths[x] * count
                                self.noteLengths[x] = [self.noteLengths[x], check]
                        if self.noteLengths[x][0] == 1:
                                self.noteLengths[x] = self.noteLengths[x]+[1]
                        else:
                                self.noteLengths[x] = self.noteLengths[x]+[0]
                        testVal = int(float(self.noteLengths[x][1]/self.noteLengths[x][0]) * 4) * bRhythm
                        tVal = int(self.noteLengths[x][1])
                        thisName = str(Fraction(tVal, testVal))
                        lengthNames.append(thisName)
    # 				print "there are now", len(self.noteLengths), 'note lengths available:'
    # 				print '      from', self.noteLengths[0][0], 'to', self.noteLengths[-1][0], 'times the base rhythm'
                return lengthNames

            
        def setComplexity_1(self, value):
    # 				print 'BREAKPOINT!!! RhythmGen complexity'
                if value <= 0:
                        self.overallComplexity = 0.
                else:
                        self.overallComplexity = value


        #### set the number of voices(rhythmic patterns)
        #### to be created
        def numVoices_1(self, numVoices):
    # 				print 'BREAKPOINT!!! RhythmGen numVoices'
                voice2create = numVoices - len(self.voices)
                if voice2create > 0:
                        for x in range(0, voice2create):
                                self.voices.append([0, 1, 1, 0])
                elif voice2create < 0:
                        for x in range(0, -1*voice2create):
                                index = (x*-1)-1
                                self.voices.pop(0)

        def timeSignature_1(self, numBeatsEntered):
                self.numBeats = numBeatsEntered
                            
        #### takes current position (beatcount as a float)
        #### and generates a rhythm for each of the active
        #### voices
        def beatProgression_1(self, stepProgression, barNumber, timeSignature):
                count = 0
                count2 = 0
    # 				print len(self.voices), count
                for x in range(0, len(self.voices)):
                        prog = (stepProgression - self.voices[x][0]) % self.voices[x][2]
                        prog = prog / self.voices[x][2]
    # 				        print stepProgression, self.voices[x], prog
                        if prog < 0.5 and self.voices[x][3] == 0:
                                count += 1
    # 				                print '!!!!!!!!!!!!!!! count'
                        if self.voices[x][3] == 1:
                                count2 += 1
    # 				print 'count', count, 'count2', count2
                if count == 0 and count2 == 0: 
    # 				        print 'closed'
                        return
    # 				print '!!!!!!!!!!!!!!!!!! hey'
                for x in range(barNumber, len(self.patternList)):
                        self.patternList[x] = timeSignature
                self.numBeats = sum(self.patternList)
                beatsDone = 0
                for x in range(0, barNumber):
                        beatsDone += self.patternList[x]
                position = math.floor(stepProgression % timeSignature) + beatsDone
                barPosition = math.floor(stepProgression % timeSignature)
                ## first check if postion(beat) has changed
                if barPosition != self.lastPos:
                        leftInBar = self.numBeats - position
                        ## get rid of noteLengths that wont sync
                        newProbabilities = self.changeProbabilities(leftInBar)
                        x = 0
                        ## I added this so any completed rhythmic groupings are
                        ## automatically removed and as such don't effect next
                        ## descision
                        for x in range(0, len(self.voices)):
                                if self.voices[x][1] == position:
                                        self.voices[x][2] = 1
                        ## the random offset just makes sure that the first voice isn't 
                        ## preferenced over others when choosing new divisions
                        ## --without offset the first voice would always get first choice of 
                        ## --fast/arhythmic notes because of the loop 
                        randomOffset = random.random()*len(self.voices)
                        randomOffset = int(math.floor(randomOffset))
                        ## look through voices
                        for x in range(0, len(self.voices)):
                                ## ensure the index stays within the bounds of
                                ## self.voices
                                x = (x + randomOffset)% len(self.voices)
                                ## choose new rhythms(note lengths) where necessary
                                if self.voices[x][1] == position:
                                        individualVoiceProbabilities = newProbabilities[:]
                                        individualVoiceProbabilities = self.limitVoiceProbabilities(x, individualVoiceProbabilities)
                                        ### i dont know why i can't pass a list without having it treated like a set
                                        newChoice = self.generateNewNotelength(individualVoiceProbabilities)
                                        self.voices[x][2] = self.noteLengths[newChoice][0]
                                        self.voices[x][0] = position
                                        self.voices[x][1] = (position + (self.noteLengths[newChoice][1]))%self.numBeats
                ### look through all voices
                for x in range(0, len(self.voices)):
                        ## determine progress of voice through its own
                        ## cycle
                        progress = (stepProgression - self.voices[x][0]) % self.voices[x][2]
                        progress = progress / self.voices[x][2]
                        if progress >= 0.5 and self.voices[x][3] != 0:
                                self.voices[x][3] = 0
    # 								print 'BREAKPOINT!!! Value changed rhythmGenbeatProg', x
                        elif progress < 0.5 and self.voices[x][3] == 0:
                                self.voices[x][3] = 1
                                outputTime = round((stepProgression - self.voices[x][0]) / self.voices[x][2])
                                outputTime = self.voices[x][0] + outputTime * self.voices[x][2]
                                self._outlet(1, x, outputTime, self.voices[x][2], position)	
    # 								print 'BREAKPOINT!!! Value outputted/read rhythmGenbeatProg', x, outputTime, self.voices[x][2], position 
                self.lastPos = barPosition
    # 				print 'BREAKPOINT!!! RhythmGen beatProg finished', self.lastPos
                    
                    
        def barsPerPhrase_1(self, numberOfBars):
    # 				print 'BREAKPOINT!!! RhythmGen barsPerPhrase'
                if numberOfBars < 1:
                        self.numBars = 1
                else:
                        self.numBars = numberOfBars
                newBars = self.numBars - len(self.patternList)
                if newBars < 0:
                        for x in range(0, abs(newBars)):
                                self.patternList.pop(0)
                elif newBars > 0:
                        for x in range(0, newBars):
                                self.patternList.append(self.patternList[-1])
    # 				print "now", self.numBars, 'bars', 'self.patternList',self.patternList
            
            

        def reloadModules_1(self):
                print "modules reloaded"
                    
        ### this completely changes the stored noteLengths list
        ### but copies over any old probabilities that still
        ### apply
        def reloadNoteLengths_1(self, maxDivision, noLevels, baseRhythm):
    # 				print 'BREAKPOINT!!! RhythmGen reLoadNotes'
                pbaseRhythm = self.baseRhythm 	# new baseRhythm/old gives the multiplier to check
                                                # new noteLength[x][0] values against old and copy
                                                # probabilities
                temp = []
                for x in range(0, len(self.noteLengths)):
                        temp.append([self.noteLengths[x][0], self.noteLengths[x][2]])
                if maxDivision < 1:
                        maxDivision = 1
                if noLevels < 1:
                        noLevels = 1
                if baseRhythm == 0:
                        baseRhythm = 1
                ### this not only sets up list values
                ### for note lengths etc
                ### but also gives out the names of the 
                ### available note lengths
                lengthNames = self.noteLengthSetup(maxDivision, noLevels, baseRhythm)
                self._outlet(2, 'lengthNames', lengthNames)

                # this checks to see if new note lengths (self.noteLengths[x][0])
                # are equivalent to old and if so copies probabilities
                baseRhythmChange = self.baseRhythm/pbaseRhythm
                for x in range(0, len(temp)):
                        for y in range (0, len(self.noteLengths)):
                                if self.noteLengths[y][0] == temp[x][0]*baseRhythmChange:
                                        self.noteLengths[y][2] = temp[x][1]
                lengths = [row[0] for row in self.noteLengths]
                noteprobs = [row[2] for row in self.noteLengths]
                self._outlet(2, 'probabilities', noteprobs)
            
            
        ### this changes the base rhythm that the 
        def baseRhythm_1(self, value):
    # 				print 'BREAKPOINT!!! RhythmGen baseRhythm'
                pbaseRhythm = self.baseRhythm 	# new baseRhythm/old gives the multiplier to check
                                                # new noteLength[x][0] values against old and copy
                                                # probabilities
                temp = []
                for x in range(0, len(self.noteLengths)):
                        temp.append([self.noteLengths[x][0], self.noteLengths[x][2]])
                self.noteLengthSetup(self.maxDivisions, self.numLevels, value)

                # this checks to see if new note lengths (self.noteLengths[x][0])
                # are equivalent to old and if so copies probabilities
                baseRhythmChange = self.baseRhythm/pbaseRhythm
                for x in range(0, len(temp)):
                        for y in range (0, len(self.noteLengths)):
                                if self.noteLengths[y][0] == temp[x][0]*baseRhythmChange:
                                        self.noteLengths[y][2] = temp[x][1]
            
        def rhythmProbabilities_1(self, *probs):
    # 				print 'BREAKPOINT!!! RhythmGen rhythmProbabilities'
                ### probabilities should be given as 
                ### just the list of probs	
                x = 0
                for x in range(0, len(probs)):
                        self.noteLengths[x][2] = probs[x]

                
            

    
#f = open( "scc.txt", "r")
#l = f.readlines()
#data = [ [ int(val) for val in line.split()] for line in l]
#g = {}
#for edge in data:
#	if edge[ 0 ] in g:
#		g[ edge[ 0 ] ] = g[ edge[ 0 ] ] + [ edge[ 1 ] ]
#	else:
#		g[ edge[ 0 ] ] = [ edge[ 1 ]]
#
#
#import sys
#print(sys.getrecursionlimit())
#sys.setrecursionlimit(1500000)
#print(sys.getrecursionlimit())
#
#import kosarju as kos
#kos.getTopFiveSccs( g )
#
#
#kos.getTopFiveSccsREC( g )
#
#
#


#f = open( "Dijkstra_input.txt", "r")
#l = f.readlines()
#data = {}
#for line in l:
#    tuple = {}
#    for t in line.split()[ 1: ]:
#        t = t.split(",")
#        tuple[ int( t[ 0 ] ) ] = int( t[ 1 ] )
#    data[ int( line.split()[ 0 ] )] = tuple
##data = { line.split()[ 0 ] : [ tuple[ 0 ], tuple[ 1 ] for tuple in line.split()[ 1: ] ] for line in l }
#
#import Dijkstra as dy
#
#sp = dy.sPath( data, 1 )
#indicies = [ 7,37,59,82,99,115,133,165,188,197 ]
#res = [ sp[ i ] for i in indicies ]
#print( res )

#
#f = open( "median.txt", "r")
#l = f.readlines()
#data = [ int(line) for line in l ]
##print( data )
#import sjf_heap
#
#heapLow = sjf_heap.sjf_heap()
#heapHigh = sjf_heap.sjf_heap()
#
#first = data[ 0 ]
#data = data[ 1: ]
#heapLow.insert( -1*first )
#median = [ first ]
#k = 1
#lst = [ first ]
#med2 = [ first ]
#for i in data:
#    lst.append( i )
#    lst.sort()
#    if i < -1* heapLow.getMin():
#        heapLow.insert( -1*i )
#    else:
#        heapHigh.insert( i )
#    lenLow = heapLow.getLength()
#    lenHigh = heapHigh.getLength()
#    if abs( lenLow - lenHigh ) > 1:
#        if lenLow > lenHigh:
#            newLow = heapLow.popMin()
#            #print( "NEWLow", newLow )
#            heapHigh.insert( -1*newLow )
#        else:
#            newHigh = heapHigh.popMin()
#            #print( "NEWHIGH", newHigh )
#            heapLow.insert( -1*newHigh )
#    k += 1
#    lenLow = heapLow.getLength()
#    lenHigh = heapHigh.getLength()
#    m = 0
#    if ( k%2 ) == 0:
#        m = -1* heapLow.getMin()
#        mid = k/2
#    else:
#        if lenLow > lenHigh:
#            m = -1* heapLow.getMin()
#        else:
#            m = heapHigh.getMin()
#        mid = (k + 1) / 2
#    median.append( m )
#    med2.append( lst[ int(mid) -1 ] )
#    if ( med2[ -1 ] != median[ -1 ] ):
#        print(" WARNING!!!!!! ")
#        print( k, mid, "LOW", heapLow.getMin(), heapLow.getLength(), "HIGH", heapHigh.getMin(), heapHigh.getLength(), "me", median[ -1 ], "lst", med2[ -1 ], )
#        heapLow.printArray()
#        heapHigh.printArray()
#        print()
##    print( heapLow.getLength(), -1*heapLow.getMin(), "******", heapHigh.getLength(), heapHigh.getMin(), "___", "me", median[ -1 ], "lst", med2[ -1 ], "+++++", k )
#
#total = sum( median )
#tot2 = sum( med2 )
#print( "RESULT", total, total % 10000, tot2, tot2 % 10000 )

f = open( "twoSumTest.txt", "r")
l = f.readlines()
data = [ int(line) for line in l ]
#print( data )
#x = range( -10, 11)
#for i in x:
#    print( i )

#print()
import twoSum as ts

ts.twoSum( data )

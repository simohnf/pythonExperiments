import random as rnd

def swap( numbers, x1, x2 ):
    temp = numbers[ x2 ]
    numbers[ x2 ] = numbers[ x1 ]
    numbers[ x1 ] = temp
    
def partition( numbers, left, right ):
    # print("parition", numbers[ left: right+1] )
    pivot = numbers[ left ]
    i = left+1
    for j in range( left+1, right+1 ):
        if ( numbers[ j ][ 0 ] > pivot[ 0 ] ):
            swap( numbers, i, j )
            i += 1
        elif( numbers[ j ][ 0 ] == pivot[ 0 ] and numbers[ j ][ 1 ] > pivot[ 1 ] ):
            swap( numbers, i, j )
            i += 1
    swap( numbers, i-1, left )
    return  i-1
    
def quickSort( numbers, pivotType = 0, left = 0, right = -1000 ):
    if right == -1000: right = len(numbers) - 1
    if ( left >= right ): return 0
    swap( numbers, left, rnd.randint( left, right ) )
    count = right - left
    piv = partition( numbers, left, right )
    count += quickSort( numbers, pivotType, left, piv -1 )
    count += quickSort( numbers, pivotType, piv+1, right )
    return count
    


def schedByDiff( jobs ):
    # [ [ weight, length ] ]
    for j in range( len( jobs )):
        diff = jobs[ j ][ 0 ] - jobs[ j ][ 1 ]
        jobs[ j ] = [ diff ] + jobs[ j ]
    quickSort( jobs )
    time = 0
    wct = 0
    for j in jobs:
        time += j[ 2 ]
        wct += j[ 1 ]*time
    print( wct )


def schedByRatio( jobs ):
    # [ [ weight, length ] ]
    for j in range( len( jobs )):
        ratio = jobs[ j ][ 0 ] / jobs[ j ][ 1 ]
        jobs[ j ] = [ ratio ] + jobs[ j ]
    quickSort( jobs )
    time = 0
    wct = 0
    for j in jobs:
        time += j[ 2 ]
        wct += j[ 1 ]*time
    print( wct )


def swap( numbers, x1, x2 ):
    temp = numbers[ x2 ]
    numbers[ x2 ] = numbers[ x1 ]
    numbers[ x1 ] = temp 
 
def partition( numbers, left, right ):
    # print("parition", numbers[ left: right+1] )
    pivot = numbers[ left ]
    i = left+1
    for j in range( left+1, right+1 ):
        if ( numbers[ j ] <= pivot ):
            swap( numbers, i, j )
            i += 1
    swap( numbers, i-1, left )
    # print("parition", numbers[ left: right+1] )
    return  i-1
    
def chooseRandomPivot( numbers, left, right ):
    swap( numbers, left, rnd.randint( left, right ) )

def chooseFirstAsPivot( numbers, left, right ):
    swap( numbers, left, left )

def chooseLastAsPivot( numbers, left, right ):
    swap( numbers, left, right )

def chooseMedianPivot( numbers, left, right ):
    m = int((right - left )/2) + left
    # print( "left", numbers[ left ], "right", numbers[ right ], "middle", numbers[ m ] )
    inds = [left, right, m ]
    vals = [ numbers[left], numbers[right], numbers[m] ]
    for i in range( 3 ):
        if vals[ i ] < vals[ 0 ]:
            swap( vals, i, 0 )
            swap( inds, i, 0 )
        elif vals[ i ] > vals[ 2 ]:
            swap( vals, i, 2 )
            swap( inds, i, 2 )
    swap(numbers, inds[ 1 ], left )
    
        
def quickSort( numbers, pivotType = 0, left = 0, right = -1000 ):
    if right == -1000: right = len(numbers) - 1
    if ( left >= right ): return 0 
    # print( "QS", numbers[left:right+1])
    if ( pivotType == 0 ):
        chooseFirstAsPivot( numbers, left, right )
    elif( pivotType == 1 ):
        chooseLastAsPivot( numbers, left, right )
    elif( pivotType == 2 ):
        chooseMedianPivot( numbers, left, right )
    elif( pivotType == 3 ):
        chooseRandomPivot( numbers, left, right )
    count = right - left
    piv = partition( numbers, left, right )
    # print( "PIV POS ", piv, numbers )
    count += quickSort( numbers, pivotType, left, piv -1 )
    count += quickSort( numbers, pivotType, piv+1, right )
    return count
    

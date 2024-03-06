def localMin( numbers, n = -1000, rowT = 0, rowB = -10000, colL = 0, colR = -10000 ):
    if n == -1000: n = len( numbers )
    if ( rowB == -10000 ): rowB = len( numbers ) - 1
    if ( colR == -10000 ): colR = len( numbers ) - 1
    if n <= 1:
        return ( numbers[ rowT ][ colL ], rowT, colL )
    hn = int(n/2)
    colL = max( 0, colL )
    colR = min( len( numbers ) - 1, colR )
    rowT = max( 0, rowT )
    rowB = min( len( numbers ) - 1, rowB )
    midCol = int( ( colR - colL ) / 2 ) + colL
    midRow = int( ( rowB - rowT ) / 2 ) + rowT
    minc = colL
    maxCR = len( numbers )
    for col in range( colL, colR + 1 ):
        if ( numbers[ midRow ][ col ] < numbers[ midRow ][ minc ] ):
            minc = col
    minr = 0
    row = hn + rowT
    if numbers[ midRow - 1 ][ minc ] < numbers[ midRow + 1 ][ minc ]:
        minr = midRow - 1
    else: minr = midRow + 1
    if numbers[ midRow ][ minc ] < numbers[ minr ][ minc ]:
        return numbers[ midRow ][ minc ], midRow, minc
    rowT = minr - int( hn / 2 )
    rowB = minr + int( hn / 2 ) 
    colL = minc - int( hn / 2 )
    colR = minc + int( hn / 2 )
    return localMin( numbers, hn, rowT, rowB, colL, colR )


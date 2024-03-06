def twoSum( vals ):
    d = {}
    for i in vals:
        d[ i ] = i
    test = set()
    for j in range( -10000, 10001 ):
        for i in list( d.keys() ):
            if ( j - i ) in d:
                test.add( j )
    print( len(test) )

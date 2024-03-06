def sPath( g, start ):
    # INPUT:
    # g --> dictionary
    #       --> { vertex : { head : length } }
    # start --> starting vertex
    
    # OUTPUT:
    # list --> shotest path to each vertex
    TOOBIG = 1000000000000
    ln = max ( list( g.keys() ) )
    X = set()
    X.add( start )
    A = [ TOOBIG ] * ( ln + 1 )
    A[ start ] = 0
    while( len( X ) != len( g ) ):
        greedyLen = TOOBIG
        edges = {}
        tail = -1
        head = -1
        for t in list( X ):
            sp = A[ t ]
            for h in list( g[ t ].keys() ):
                if h not in X:
                    lvw = sp + g[ t ][ h ]
                    if lvw < greedyLen:
                        greedyLen = lvw
                        tail = t
                        head = h
        X.add( head )
        A[ head ] = greedyLen
    return A
            

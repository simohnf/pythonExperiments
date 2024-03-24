
def prim( graph, v  ):
    X =  { v }
    T = [ ]
    totCost = 0
    while len( X ) != len( graph ):
        posEdges = []
        # calculate cheapest edge from each tail
        cheapEdge = None
        for tail in X:
            heads = list( graph[ tail ].keys() )
            
            heads = [ h for h in heads if h not in X ]
            if len( heads ) > 0:
                head = heads[ 0 ]
                cost = graph[ tail ][ head ]
                if cheapEdge == None:
                    cheapEdge = [ tail, head, cost ]
                for h in heads:
                    if graph[ tail ][ h ] < cheapEdge[ 2 ]:
                        head = h
                        cost = graph[ tail ][ h ]
                        cheapEdge = [ tail, h, cost ]
        X.add( cheapEdge[ 1 ] )
        T.append( cheapEdge )
        totCost += cheapEdge[ 2 ]
    print( totCost )
        
        
    

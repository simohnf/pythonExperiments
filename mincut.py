import random as rnd

def minCut( graph ):
    while len( graph ) > 2:
        edgeH = rnd.choice( list( graph ) )
        edgeT = graph[ edgeH ][ rnd.randint( 0, len( graph[ edgeH ] ) - 1 ) ] 
        graph[ edgeT ] += graph[ edgeH ]
        graph.pop( edgeH )
        graph[ edgeT ] = [ i for i in graph[ edgeT ] if i != edgeH ]
        graph[ edgeT ] = [ i for i in graph[ edgeT ] if i != edgeT ]
        for i in list( graph ):
            for j in range( len( graph[ i ] ) ):
                if graph[ i ][ j ] == edgeH:
                    graph[ i ][ j ] = edgeT 
    remaining = list( graph )
    if len( graph[ remaining[ 0 ] ] ) != len( graph[ remaining [ 1 ] ] ):
        print( "HELP", graph )
    return len( graph[ remaining[ 0 ] ] ), graph
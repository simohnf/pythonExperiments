
def revGraph( g ):
    # graph --> dictionary
        # { vertex : [ edge heads ] }
    gRev = {}
    for ve in g:
        for eh in g[ ve ]:
            if eh in gRev:
                gRev[ eh ].append( ve )
            else:
                gRev[ eh ] = [ ve ]
    return gRev


#====================#====================#====================#====================
#====================#====================#====================#====================
#====================#====================#====================#====================
#====================#====================#====================#====================
def DFS_rec1( g, explored, start, fs, current_label ):
#    print( "REC_START", start )
    explored[ start ] = True
    if start in g:
        for i in g[ start ]:
            if i not in explored:
                current_label = DFS_rec1( g, explored, i, fs, current_label )
    fs[ current_label ] = start
#    print( "DFS_rec1", start, current_label )
    current_label -= 1
    return current_label
    
def DFS_rec2( g, explored, start, leader, scc ):
    explored[ start ] = True
    if leader in scc:
        scc[ leader ].append( start )
    else:
        scc[ leader ] = [ start ]
    if start in g:
        for i in g[ start ]:
            if i not in explored:
                DFS_rec2( g, explored, i, leader, scc )
    
def kosarju_scc_rec( g ):
    gRev = revGraph( g )
    m = max( max( g.keys() ), max( gRev.keys() ) )
    explored = {}
    fs = [ -1 ] * ( m + 1 )
    v = m
    current_label = m
    while v > 0:
        if v not in explored:
#            print( current_label )
            current_label = DFS_rec1( gRev, explored, v, fs, current_label )
        v -= 1
#    print( "FS_REC" )
#    print( fs )
    explored = {}
    scc = {}
    for leader in fs[ 1: ]:
        if leader not in explored:
            DFS_rec2( g, explored, leader, leader, scc )
    return scc
   
def getTopFiveSccsREC( g ):
    res = kosarju_scc_rec( g )
#    print( "rec res", res )
    sccs = [ len( res[ i ] ) for i in res ]
    sccs.sort( reverse = True )
    if len( sccs ) > 5:
        sccs = sccs[ : 5 ]
    else:
        while len( sccs ) < 5:
            sccs.append( 0 )
    print( sccs )

#====================#====================#====================#====================
#====================#====================#====================#====================
#====================#====================#====================#====================
#====================#====================#====================#====================
def DFS_it1( g, explored, start, fs, current_label ):
    stack = [ start ]
    seen = set()
    sink = []
    while len( stack ) > 0:
#        print( "STACK PRE POP", stack )
        v = stack.pop()
#        print( "DFS_it1", v )
        if v not in explored:
            sink.append( v )
            explored[ v ] = v
            if v in g:
                for i in g[ v ]:
#                    print( v, g[ v ] )
                    if i not in explored and i not in seen:
                        stack.append( i )
#                        print( "add", i )
                        seen.add( i )
#                    else:
#                        print( "already done", i )
#                print( "STACK", stack )
    ln = len( sink )
    test = [ i for i in sink ]
    sink.reverse()
    for i in sink:
        fs[ current_label ] = i
        current_label -= 1
    return current_label
    
def DFS_it2( g, explored, start, leader, scc ):
    stack = { start }
    while len( stack ) > 0:
        v = stack.pop()
        if leader in scc:
            scc[ leader ].append( v )
        else:
            scc[ leader ] = [ v ]
        if v not in explored:
            explored[ v ] = v
            if v in g:
                for i in g[ v ]:
                    if i not in explored and i not in stack:
                        stack.add( i )

def kosarju_scc( g ):
    # # 1 --> Grev = reversed g
    # # 2 --> compute DFS on Grev and keep track of finishing times
    # # 2 --> use finishing times to determine order to compute DFS on original graph
    # # fs = DFS_loop( revGraph( g ) )
    gRev = revGraph( g )
    m = max( max( g.keys() ), max( gRev.keys() ) )
    explored = { }
    fs = [ -1 ] * ( m + 1 )
    v = m
    current_label = m
    while v > 0 and current_label > 0:
        if v not in explored:
#            print( current_label )
            current_label = DFS_it1( gRev, explored, v, fs, current_label )
        v -= 1
#    print( "FS_IT")
#    print( fs )
    explored = { }
    scc = {}
    for leader in fs[ 1: ]:
        if leader not in explored:
            DFS_it2( g, explored, leader, leader, scc )
    return scc

    
def getTopFiveSccs( g ):
#    print( revGraph( g ) )
    res = kosarju_scc( g )
#    print( "it res", res )
    sccs = [ len( res[ i ] ) for i in res ]
    sccs.sort( reverse = True )
    if len( sccs ) > 5:
        sccs = sccs[ : 5 ]
    else:
        while len( sccs ) < 5:
            sccs.append( 0 )
    print( sccs )


#====================#====================#====================#====================
#====================#====================#====================#====================
#====================#====================#====================#====================
#====================#====================#====================#====================

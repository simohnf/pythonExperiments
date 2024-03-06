class sjf_heap:
    # INDICES ARE FUCKED :( :(
    def __init__( self ):
        self.arr = []
    
    def swap(self, x, y ):
        temp = self.arr[ x ]
        self.arr[ x ] = self.arr[ y ]
        self.arr[ y ] = temp

    def insert( self,  x ):
        self.arr.append( x )
        #print( "ARRAY INSERT", x, self.arr )
        pos = len( self.arr ) - 1
        parent = int( (pos + 1) / 2 ) - 1
        #print( pos, parent )
        while parent >= 0 and ( self.arr[ parent ] > self.arr[ pos ] ):
            #print( pos, parent, self.arr[ parent ], self.arr[ pos ]  )
            self.swap( parent, pos )
            pos = parent
            parent = int( ( pos + 1 ) / 2 ) - 1
        #print( "ARRAY INSERT END", self.arr )
        #print()

    def getMin( self ):
        return self.arr[ 0 ]
    
    def popMin( self ):
        if len( self.arr ) == 0:
            return None
        if len( self.arr ) == 1:
            return self.arr.pop( )
        #print( "POPMIN", self.arr )
        last = len( self.arr ) - 1
        self.swap( 0, last )
        x = self.arr.pop()
        self.bubbleDown( 0 )
        #print( self.arr )
        #print()
        return x
    
    def delete( self, x ):
        pos = -1
        for i in range( len( self.arr ) ):
            if self.arr[ i ] == x:
                pos = i
                break
        pos = self.bubbleDown( pos )
        x = self.arr.pop( pos )
        return x

    def bubbleDown( self, pos ):
        #print( "BUBBLE", pos , self.arr )
        child2 = ( ( pos + 1 ) * 2 )
        child1 = child2 - 1
        while child1 < len( self.arr ):
            childPos = child1
            if ( child2 < len( self.arr ) ):
                #print( pos, "c1", child1, self.arr[ child1 ], "c2", child2, self.arr[ child2 ] )
                if ( self.arr[ child2 ] < self.arr[ child1 ] ):
                    childPos = child2
            #print( "cPOS", childPos )
            if self.arr[ pos ] > self.arr[ childPos ]:
                self.swap( pos, childPos )
                pos = childPos
            else:
                return pos
            child2 = ( (pos + 1) * 2 )
            child1 = child2 - 1
        return pos
        
    def getLength(self ):
        return len( self.arr )
        
    def getArray():
        return self.arr
        
    def printArray( self ):
        print( "HEAP", self.arr )

    def printTree( self ):
        if len( self.arr ) == 0:
            print( self.arr )
            return
        tree = []
        tree.append( [ self.arr[ 0 ] ] )
        i = 1
        l = 0
        sofar = pow( 2, l )
        while sofar <= len( self.arr ):
            level = []
            next = sofar+ pow( 2, l + 1 )
            while i < next and i < len( self.arr ) :
                level.append( self.arr[ i ] )
                i += 1
            l += 1
            sofar += pow( 2, l )
            tree.append( level )
        print( tree )



class sjf_bstNode:
    value = None
    upPtr = None
    lPtr = None
    rPtr = None
    def __init__( self, value ):
        self.value = value
    
    def __repr__( self ):
        return "bstNode -->%s" % self.value
        
class sjf_bst:
    def __init__( self, value = None ):
        if value != None:
            self.root = sjf_bstNode( value )
        else:
            self.root = None
        
    def __findNode( self, value ):
        pos = self.root
        if pos.value == value:
            return pos, False
        node = pos
        while pos != None:
            node = pos
            if value <= pos.value:
                pos = pos.lPtr
            else:
                pos = pos.rPtr
        isParent = True
        if node.value == value:
            isParent = False
        return node, isParent
        
    def search( self, value ):
        node, isParent = self.__findNode( value )
        if isParent:
            return None
        return node
        
    def insert( self, value ):
        if self.root == None:
            self.root = sjf_bstNode( value )
            return
        parent, isParent = self.__findNode( value )
        if value <= parent.value:
            newNode = sjf_bstNode( value )
            newNode.upPtr = parent
            parent.lPtr = newNode
        else:
            newNode = sjf_bstNode( value )
            newNode.upPtr = parent
            parent.rPtr = newNode
    
    def getMin( self ):
        value = float('-inf')
        parent, isParent = self.__findNode( value )
        return parent.value
    
    def getMax( self ):
        value = float('inf')
        parent, isParent = self.__findNode( value )
        return parent.value
    
    def getPredecessor( self, value ):
        node, isParent = self.__findNode( value )
        if node.lPtr != None:
            return node.lPtr
        while node.value >= value:
            node = node.upPtr
            if node == None:
                return None
        return node

    def getSuccessor( self, value ):
        node, isParent = self.__findNode( value )
        if node.rPtr != None:
            return node.rPtr
        while node.value <= value:
            node = node.upPtr
            if node == None:
                return None
        return node
    
    def __traverse( self, pos ):
        if pos == None:
            return
        self.__traverse( pos.lPtr )
        print( pos )
        self.__traverse( pos.rPtr )
        
    def inOrderTraverse( self ):
        self.__traverse( self.root )


'''
Created on 26/lug/2014

@author: michele
'''

class Set(object):
    """Union find Tarjan implementation"""
    def __init__(self, contex=None):
        self._contex = contex
        self._parent = None
    
    def _find_impl(self):
        r = self
        while r._parent:
            r = r._parent
        return r
    
    def find(self):
        """Return the set that contain self"""
        return self._find_impl()
    
    def _union_impl(self, other):
        """The implementation of union : it must return 
        the set that represent the union of the sets.
        self and other MUST be SET and not just Node
        (i.e. node without _parent).
        """
        self._parent = other
        return other
    
    def union(self, other, contex=None):
        """Union the set of self and the set of other
        @param other: a node
        @param contex: the context of the new node
        @return the new set 
        """
        if type(self) != type(other):
            raise ValueError("You can do union only on set of the same type")
        S = self._find_impl()
        O = other._find_impl()
        if not S is O:
            S = S._union_impl(O)
        S.contex = contex
        return S
    
    @property
    def contex(self):
        return self._find_impl()._contex

    @contex.setter
    def contex(self, contex):
        self._find_impl()._contex = contex


'''
The algorithm's performance, given m union/find operations of any ordering, on
n elements has been shown to take log* time per operation, where log* is
pronounced log-star, and is the INVERSE of what is known as the Ackerman
function, which is given below:
A(0) = 1
A(n) = 2**A(n-1)
'''

class UnionFind_by_rank(Set):
    """The union by rank and halving implementation that collapse to the root one over two node in
    the path to the root"""
    def __init__(self, context=None):
        '''Create an empty union find data structure.'''
        super(UnionFind_by_rank,self).__init__(context)
        self._rank = 1

    def _find_impl(self):
        stk = []
        root = self
        while root._parent is not None and root._parent._parent is not None :
            stk.append(root)
            root = root._parent._parent
        if root._parent is not None:
            root = root._parent
        for p in stk:
            p._parent = root
        return root
    
    def _union_impl(self, other):
        '''Implement union by set the greater rank as root: mantain rank invariant'''
        root = self
        if self._rank < other._rank:
            root = other
            other = self
        other._parent = root
        root._rank += other._rank
        return root

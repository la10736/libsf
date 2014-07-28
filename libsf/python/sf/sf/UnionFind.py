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

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
unionfind.py

A class that implements the Union Find data structure and algorithm.  This
data structure allows one to find out which set an object belongs to, as well
as join two sets.

The algorithm's performance, given m union/find operations of any ordering, on
n elements has been shown to take log* time per operation, where log* is
pronounced log-star, and is the INVERSE of what is known as the Ackerman
function, which is given below:
A(0) = 1
A(n) = 2**A(n-1)

I include the functions to be complete.  Note that we can be 'inefficient'
when performing the inverse ackerman function, as it will only take a maximum
of 6 iterations to perform; A(5) is 65536 binary digits long (a 1 with 65535
zeroes following).  A(6) is 2**65536 binary digits long, and cannot be
represented by the memory of the entire universe.


The Union Find data structure is not a universal set implementation, but can
tell you if two objects are in the same set, in different sets, or you can
combine two sets.
ufset.find(obja) == ufset.find(objb)
ufset.find(obja) != ufset.find(objb)
ufset.union(obja, objb)


This algorithm and data structure are primarily used for Kruskal's Minimum
Spanning Tree algorithm for graphs, but other uses have been found.

August 12, 2003 Josiah Carlson
'''

class UnionFind_by_rank(Set):
    def __init__(self, context=None):
        '''Create an empty union find data structure.'''
        super(UnionFind_by_rank,self).__init__(context)
        self._rank = 1
        '''Trick good find implementation'''
        self._parent = self 

    def _find_impl(self):
        stk = [self]
        root = self._parent
        '''root is the last element in the stack => Cycle found => the root'''
        while root is not stk[-1]:
            stk.append(root)
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

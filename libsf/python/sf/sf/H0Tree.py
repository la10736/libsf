'''
Created on 06/lug/2014

@author: michele
'''
from SizeGraph import SizeGraph, SizeNode
import weakref

class H0Node(SizeNode):
    
    def __init__(self, *args, **kwargs):
        self._parent = None
        super(H0Node,self).__init__(*args, **kwargs)
    
    @property
    def parent(self):
        if self._parent is None:
            return None
        return self._parent()
    
    def _set_parent(self, p):
        self._connect(p)
        self._parent = weakref.ref(p)
        
    @parent.setter
    def parent(self, p):
        if self.phy >= p.phy:
            raise ValueError("Cannot set the parent : the measuring function MUST be greater")
        self._set_parent(p)
        
    def connect(self, other):
        self._check_node(other)
        if self.phy < other.phy:
            return self._set_parent(other)
        elif self.phy > other.phy:
            return other._set_parent(self)
        raise ValueError("Cannot coonect two node with the same measuring function value")
        
    def _add_child(self,c):
        if self.phy <= c.phy:
            raise ValueError("Cannot set the children : the measuring function MUST be lower")
        c.parent = self
        
    def add_children(self, *args):
        for c in args:
            self._add_child(c)
    @property
    def children(self):
        return set([n for n in self.connected if n != self.parent])
        

class H0Tree(SizeGraph):
    '''
    The H0Tree class. It a tree (or a forest of H0Tree) of size nodes.
    Every node can have a parent and some children.
    For every node the size value of the parent must be greater.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(H0Tree,self).__init__(nodes_factory=H0Node)
        
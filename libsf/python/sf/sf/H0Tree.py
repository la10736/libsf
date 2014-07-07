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
    @parent.setter
    def parent(self, p):
        if self.phy >= p.phy:
            raise ValueError("Cannot set the parent : the measuring function MUST be greater")
        self._connect(p)
        self._parent = weakref.ref(p)

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
        
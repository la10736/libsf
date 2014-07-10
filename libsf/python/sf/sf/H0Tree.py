'''
Created on 06/lug/2014

@author: michele
'''
from SizeGraph import SizeGraph, SizeNode
from SizeFunction import SizeFunction
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
    
    @property
    def is_leaf(self):
        return not self.children
    
    @property
    def leafs(self):
        els = [self]
        ret = []
        while els:
            ret += [e for e in els if e.is_leaf]
            n = []
            for e in els:
                if not e.is_leaf:
                    n += e.children
            els = n
        return ret
    
    @property
    def root(self):
        r = self
        while r.parent:
            r = r.parent
        return r

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
    
    @property
    def leafs(self):
        return [l for l in self.nodes if l.is_leaf]
    
    def get_sf(self):
        leafs = sorted(self.leafs, key=lambda n:n.phy, reverse=True)
        sf = SizeFunction()
        map_ssf={}
        for l in leafs:
            n = l
            ssf = map_ssf.get(n, None)
            while ssf is None and n is not None:
                n = n.parent
                ssf = map_ssf.get(n, None)
            if n is None:
                r = l.root
                cl = min(map(lambda n:n.phy, r.leafs))
                ssf = sf.new_ssf(cl,r.phy)
            n = l
            while n is not None and not map_ssf.has_key(n):
                map_ssf[n] = ssf
                n = n.parent
            if n is not None and map_ssf[n] != ssf:
                raise RuntimeError("BUG: More than ssf on the same connected component")
            n = l.parent
            while n is not None:
                if any(map(lambda c:not map_ssf.has_key(c),n.children)):
                    """Found the end point of corner point"""
                    break
                n = n.parent
            if n is not None:
                ssf.add_point(l.phy,n.phy)
        return sf

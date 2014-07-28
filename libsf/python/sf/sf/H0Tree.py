'''
Created on 06/lug/2014

@author: michele
'''
from SizeGraph import SizeGraph, SizeNode
from SizeFunction import SizeFunction
import weakref
from UnionFind import Set
from operator import attrgetter

class H0Node(SizeNode):
    
    def __init__(self, *args, **kwargs):
        self._parent = None
        self.__leafs = None
        super(H0Node,self).__init__(*args, **kwargs)
    
    @property
    def parent(self):
        if self._parent is None:
            return None
        return self._parent()
    
    def _invalidate_leafs(self):
        p = self
        while p:
            p.__leafs = None
            p = p.parent
    
    def _set_parent(self, p):
        self._connect(p)
        self._parent = weakref.ref(p)
        p._invalidate_leafs()
        
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
        if self.__leafs is not None:
            return self.__leafs
        elif self.is_leaf:
            ret = [self]
        else:
            ret = [e for e in self.children if e.is_leaf]
            for e in self.children:
                if not e.is_leaf:
                    ret += e.leafs
        self.__leafs = ret
        return ret
    
    @property
    def root(self):
        r = self
        while r.parent:
            r = r.parent
        return r
    
    def get_min(self):
        """Should return self if the node is a leaf
        or has more than one child; otherwise
        return the first child that is a leaf or has
        more than one child"""
        _cc = self.children
        if not _cc or len(_cc)>1:
            return self
        return _cc.pop().get_min()
    
    def equal_subtree(self, other):
        """Return true if the sub tree with self as root is equal
        to the sub tree with the root in other
        @param other: The other H0Node used as root for the other tree
        @raise ValueError: if other is not an instance of H0Node
        """
        if not isinstance(other, H0Node):
            raise ValueError("other must be a H0Node")
        if self.phy != other.phy:
            return False
        scc,occ = self.children,other.children
        if len(scc) != len(occ):
            return False
        for sc in scc:
            f = None
            for oc in occ:
                if sc.get_min().equal_subtree(oc.get_min()):
                    f = oc
                    break
            if f is None:
                return False
            occ.remove(f)
        return True
            
        


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
    
    def _init_context(self):
        for n in self.nodes:
            n._context = [len(n.children),None]
    
    def get_sf(self):
        leafs = sorted(self.leafs, key=lambda n:n.phy, reverse=True)
        self._init_context()
        sf = SizeFunction()
        for l in leafs:
            n = l
            ssf = n._context[1]
            while n is not None and n._context[1] is None:
                n = n.parent
            if n is None:
                r = l.root
                cl = min(map(lambda n:n.phy, r.leafs))
                ssf = sf.new_ssf(cl,r.phy)
            else:
                ssf = n._context[1]
            n = l
            while n is not None and n._context[1] is None:
                n._context[1] = ssf
                n = n.parent
            if n is not None and n._context[1] != ssf:
                raise RuntimeError("BUG: More than one ssf on the same connected component")
            n = l.parent
            while n is not None:
                if n._context[0] > 1:
                    """Found the end point of corner point"""
                    break
                n = n.parent
            if n is not None:
                n._context[0] -= 1
                ssf.add_point(l.phy,n.phy)
        return sf
        
    def same(self, other):
        if other is None or not isinstance(other, H0Tree):
            raise ValueError("You can compare H0Tree only")
        sroots = set([n for n in self.nodes if n.parent is None])
        oroots = set([n for n in other.nodes if n.parent is None])
        if len(sroots) != len(oroots):
            return False
        for rs in sroots:
            found = None
            for ro in oroots:
                if rs.equal_subtree(ro):
                    found = ro
                    break
            if found is not None:
                oroots.remove(ro)
            else:
                return False
        return True

def compute_H0Tree(g):
    """Compute the H0Tree from the SizeGraph G. 
    @param g: a SizeGraph
    @return the H0Tree of the size graph
    @raise ValueError if g is not a SizeGraph
    """
    if g is None:
        return None
    if not isinstance(g, SizeGraph):
        raise ValueError("g Should be a SizeGraph")
    h = H0Tree()
    """For each nodes (sorted by phy)"""
    for n in sorted(g.nodes,key=attrgetter('phy')):
        """Use contex to store unioin-find set"""
        sn = n._context = Set()
        """The node of h associate to the set of n... it is None"""
        hn = None
        """Connetions to "lower" node: aka the nodes already computed"""
        nodes = [m for m in n._connected if m._context is not None]
        for m in nodes:
            sm = m._context
            """The node of h associate to the set of m"""
            hm = sm.contex
            if n.phy == m.phy :
                sm.union(sn)
                hn = hm
            elif hn != hm:
                if hn is None:
                    """I need to create a new node""" 
                    hn = sn.contex = h.add_node(n.phy)
                """hm is the parent of hm"""
                hm.parent = hn
        if hn is None:
            """Create a new node for the leafs""" 
            sn.contex = h.add_node(n.phy)
    return h
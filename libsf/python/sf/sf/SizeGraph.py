'''
Created on 29/giu/2014

@author: michele
'''
import weakref

class SizeNode(object):
    """A node of size graph"""
    def __init__(self, sg, phy=0.0, *args):
        """Create a node of the SizeGraph sg
        @param sg: The SizeGraph that contain the node
        @param phy: The Value of the measuring function on the node. 
        @param *args: The nodes that are connected to self 
        """
        self._sg = weakref.ref(sg)
        more = None
        if isinstance(phy, SizeNode):
            more = phy
            phy = 0.0
        for n in args:
            if not isinstance(n, SizeNode):
                raise ValueError("The args must be _SizeNodes only ")
        self._connected = weakref.WeakSet()
        for n in args:
            self._connect(n)
        if more is not None:
            self._connect(more)
        self.phy = phy
    
    @property
    def sg(self):
        """The SizeGraph that contain the node"""
        return self._sg()
    
    def _connect(self,other):
        self._connected.add(other)
        other._connected.add(self)
    
    def _check_node(self, other):
        if type(self) != type(other):
            raise ValueError("Nodes must be of the same type")
        if self._sg != other._sg:
            raise ValueError("The SizeNode must be in the same SizeGraph")
    
    def connect(self,other):
        """Connect from self to the other SizeNode 
        @param other: other SizeNode
        """
        self._check_node(other)
        self._connect(other)
        
    @property
    def connected(self):
        """The set of the nodes that are connected to self"""
        return self._connected.copy()
    
    @property
    def phy(self):
        return self._phy
    
    @phy.setter
    def phy(self, val):
        if not isinstance(val, (int, long, float)):
            raise ValueError("Phy can be just a number")
        self._phy = val
    
class SizeGraph(object):
    default_nodes_factory = SizeNode
    
    """The SizeGraph base object"""
    def __init__(self, nodes_factory=None):
        self._nodes = set()
        if nodes_factory is None:
            nodes_factory = self.default_nodes_factory
        fake = nodes_factory(self)
        if not isinstance(fake, SizeNode):
            raise ValueError("The factory should create instances of SizeNode")
        self._nodes_factory = nodes_factory
    
    def add_node(self,*args,**kwargs):
        """Create a new node of the SizeGraph"""
        n = self._nodes_factory(self,*args,**kwargs)
        self._nodes.add(n)
        return n
    
    @property
    def nodes_factory(self):
        return self._nodes_factory
    
    @property
    def nodes(self):
        return weakref.WeakSet(self._nodes)
    
    def get_connections(self):
        ret = set()
        for n in self.nodes:
            for m in n.connected:
                if id(n) < id(m):
                    ret.add((n,m))
                else:
                    ret.add((m,n))
        return ret
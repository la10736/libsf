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

        self._phy = None
        """Type checkin"""
        self.phy = phy
        self._context = None

    @property
    def sg(self):
        """The SizeGraph that contain the node"""
        if self._sg is None:
            return None
        return self._sg()

    def _connect(self, other):
        self._connected.add(other)
        other._connected.add(self)

    def _check_node(self, other):
        if type(self) != type(other):
            raise ValueError("Nodes must be of the same type")
        if self._sg != other._sg:
            raise ValueError("The SizeNode must be in the same SizeGraph")

    def connect(self, other):
        """Connect from self to the other SizeNode 
        @param other: other SizeNode
        """
        self._check_node(other)
        self._connect(other)

    def _disconnect(self, other):
        self._connected.remove(other)
        other._connected.remove(self)

    def disconnect(self, other):
        """Disconnect from self to the other SizeNode 
        @param other: other SizeNode
        """
        self._check_node(other)
        if other in self._connected:
            self._disconnect(other)

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

    def add_node(self, *args, **kwargs):
        """Create a new node of the SizeGraph"""
        n = self._nodes_factory(self, *args, **kwargs)
        self._nodes.add(n)
        return n

    def remove_node(self, n):
        if n is None:
            raise ValueError("Invalid node")
        if n.sg != self:
            raise ValueError("Node from other graph")
        for m in n.connected:
            n._disconnect(m)
        self._nodes.remove(n)
        n._sg = None

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
                    ret.add((n, m))
                else:
                    ret.add((m, n))
        return ret

    def clean_context(self):
        for n in self.nodes:
            n._context = None

    def _obj(self):
        return self.__class__(self.nodes_factory)

    def copy(self):
        ret = self._obj()
        for n in self.nodes:
            n._contex = ret.add_node(n.phy)
        for n in self.nodes:
            for m in n.connected:
                n._contex.connect(m._contex)
        self.clean_context()
        return ret

    def dump(self, f, legacy=False, comments=True):
        if legacy:
            comments = False
        if comments:
            f = _check_and_write(f, "# Size Graph File\n")

        nn = [n for n in self.nodes]
        if not nn:
            if comments:
                f.write("# Empty\n")
            return
        if comments:
            f.write("# Nodes:\n")
        f = _check_and_write(f, "%d\n" % len(nn))
        if not legacy:
            if comments:
                f.write("# Measuring Function\n")
            f.write("MS\n")
            for n in nn:
                f.write(str(n.phy) + "\n")
        cc = self.get_connections()
        if not cc:
            if comments:
                f.write("# No Edges\n")
            return
        if comments:
            f.write("# Edges:\n")
        for i, n in enumerate(nn):
            n._context = i
        f.write("%d\n" % len(cc))
        for c in cc:
            f.write("%d %d\n" % (c[0]._context, c[1]._context))
        if comments:
            f.write("# End Graph\n")
        self.clean_context()


def _check_and_write(f, m):
    try:
        f.write(m)
    except AttributeError:
        """Try to use it as path"""
        f = file(str(f), "w")
        f.write(m)
    return f


def _rl(l):
    l = l.strip()
    if l.startswith("#"):
        return ''
    return l


def _next_l(f):
    l = f.readline()
    while l:
        l = _rl(l)
        if l:
            break
        l = f.readline()
    return l


def readsg(f, ms=None):
    """Read a size graph from f and, eventually, apply the measuring function
    ms. The format is simple:
    1) lines that starts by # or empty will be ignored
    2) the first no empty line is the number of nodes N
    3) if the next items is the string MS the next N valid lines will be used as 
    measuring function
    4) the next valid items will be the number of edges E and E couples of
    index "n m" that are the edges where n is the index of the starting node
    and m the ending node
     
    @param f: the open file (a object with readline() function) where is the graph.
    if is not a file will try to use it as a path for the file where reading.
    @param ms: the measuring function where the phy of n-th node will be ms[n]
    @return the SizeGraph
    """
    try:
        l = _next_l(f)
    except AttributeError:
        """Try to use it as path"""
        f = file(str(f))
        l = _next_l(f)
    g = SizeGraph()
    if not l:
        return g
    n = int(l)
    l = _next_l(f)
    if l == "MS":
        fms = [float(_next_l(f)) for _ in xrange(n)]
        if ms is None:
            ms = fms
        l = _next_l(f)
    if ms is None:
        ms = [0 for _ in xrange(n)]
    elif len(ms) < n:
        raise ValueError("Not enough values for ms (%d<%d)" % (len(ms), n))
    nn = [g.add_node(ms[i]) for i in xrange(n)]
    if not l:
        """No Edges"""
        return g
    m = int(l)
    for _ in xrange(m):
        n0, n1 = map(lambda x: nn[int(x)], _next_l(f).split(" "))
        n0.connect(n1)
    return g
'''
Created on 06/lug/2014

@author: michele
'''
import unittest
from sf.H0Tree import H0Tree as H, H0Node
from sf.H0Tree import H0Node as N
from sf.SizeFunction import SizeFunction as SF
import sys


class Test_H0Tree(unittest.TestCase):
    """Test cases for H0Tree class.
    """

    def test_Costructor(self):
        h = H()
        self.assertIs(h.nodes_factory, N)
    
    def test_add_node(self):
        h = H()
        n = h.add_node()
        self.assertIsInstance(n, N)
        self.assertIs(h, n.sg)
        self.assertEqual(0.0, n.phy)
        n = h.add_node(2.0)
        self.assertEqual(2.0, n.phy)
        
class Test_H0Node(unittest.TestCase):
    """Like a SizeNode you can use connect() function to connect
    two node but non all connection are legal:
    1) the phy value must be different
    2) if the phy vale of connected node is grater so the node will be the parent,
    otherwise wille be a children
    3) a node can have only a parent
    """
    
    def test_Costructor(self):
        h = H()
        n = N(h)
        self.assertIs(h, n.sg)
        self.assertEqual(0.0, n.phy)
        n = N(h,1.0)
        self.assertIs(h, n.sg)
        self.assertEqual(1.0, n.phy)
        
    
    @staticmethod
    def _parent_wrap(n,p):
        n.parent = n
    
    def test_parent(self):
        h = H()
        n = h.add_node()
        self.assertIsNone(n.parent)
        n.parent = h.add_node(1.0)
        c = n.connected
        self.assertEqual(1,len(c))
        nn=c.pop()
        self.assertEqual(1.0,nn.phy)
        self.assertIs(nn, n.parent)
        n2 = h.add_node(2.0)
        self.assertRaises(ValueError, self._parent_wrap, n, n2)
        n3 = h.add_node(2.0)
        n4 = h.add_node(1.5)
        n5 = h.add_node(2.5)
        self.assertRaises(ValueError, self._parent_wrap, n2, n3)
        self.assertRaises(ValueError, self._parent_wrap, n2, n4)
        """Sanity Check"""
        n2.parent = n5
    
    def test__add_child(self):
        h = H()
        n = h.add_node()
        n._add_child(h.add_node(-1.0))
        c = n.connected
        self.assertEqual(1,len(c))
        nn=c.pop()
        self.assertEqual(-1.0,nn.phy)
        n2 = h.add_node()
        n3 = h.add_node(1)
        self.assertRaises(ValueError, n._add_child, n2)
        self.assertRaises(ValueError, n._add_child, n3)
        """Sanity check"""
        n._add_child(h.add_node(-1.0))
    
    
    def test_add_children(self):
        h = H()
        n = h.add_node()
        """Argomento singolo"""
        n.add_children(h.add_node(-1.0))
        c = n.connected
        self.assertEqual(1,len(c))
        nn=c.pop()
        self.assertEqual(-1.0,nn.phy)
        """Aggiunta multipla"""
        n = h.add_node()
        n.add_children(h.add_node(-2.0),h.add_node(-2.0),h.add_node(-2.0),h.add_node(-2.0),h.add_node(-2.0))
        self.assertEqual(5, len(n.connected))
        
    def test_children(self):
        h = H()
        n = h.add_node()
        n.add_children(h.add_node(-2.0),h.add_node(-2.0),h.add_node(-2.0),h.add_node(-2.0),h.add_node(-2.0))
        children = n.children
        self.assertEqual(5, len(children))
        n.add_children(h.add_node(-2.0),h.add_node(-2.0))
        self.assertEqual(7, len(n.children))
    
    def test_connected_equal_children_plus_parent(self):
        h = H()
        n = h.add_node()
        n.add_children(h.add_node(-2.0),h.add_node(-2.0),h.add_node(-2.0),h.add_node(-2.0),h.add_node(-2.0))
        n.parent = h.add_node(1)
        self.assertEqual(5, len(n.children))
        self.assertEqual(6, len(n.connected))
        for nn in n.children.union([n.parent]):
            self.assertIn(nn,n.connected)
    
    def test_parent_children_dual(self):
        h = H()
        n = h.add_node()
        n.parent = h.add_node(1)
        self.assertEqual(1, len(n.parent.children))
        self.assertIs(n, n.parent.children.pop())
        n.add_children(h.add_node(-2.0),h.add_node(-2.0),h.add_node(-3.0),h.add_node(-1.5),h.add_node(-1.0))
        for nn in n.children:
            self.assertIs(nn.parent, n)
    
    def _connect(self,n,m):
        n.connect(m)
    
    def test_connect(self):
        h = H()
        n = h.add_node()
        """Cannot connect equal nodes"""
        self.assertRaises(ValueError, self._connect, n, h.add_node())
        """n<m => m a child of n and n a parent of m"""
        m = h.add_node(1.0)
        n.connect(m)
        self.assertIn(n, m.children)
        self.assertIs(m, n.parent)
        m = h.add_node(-1.0)
        n.connect(m)
        self.assertIn(m, n.children)
        self.assertIs(n, m.parent)
    
    def test_is_leaf(self):
        h = H()
        n = h.add_node()
        self.assertTrue(n.is_leaf)
        n.parent = h.add_node(1.0)
        self.assertTrue(n.is_leaf)
        self.assertFalse(n.parent.is_leaf)
        h.add_node(-1.0).parent = n
        self.assertFalse(n.is_leaf)
        self.assertTrue(n.children.pop().is_leaf)

    def test_leafs(self):
        h = H()
        n = h.add_node()
        self.assertEqual(1, len(n.leafs))
        self.assertIn(n, n.leafs)
        nn = [h.add_node(-1.0) for _ in xrange(3)]
        for nnn in nn:
            nnn.parent=n
        leafs = n.leafs
        self.assertEqual(len(nn), len(leafs))
        for nnn in nn:
            self.assertIn(nnn, leafs)
            h.add_node(-2.0).parent = nnn
            h.add_node(-2.0).parent = nnn
        leafs = n.leafs
        self.assertEqual(2*len(nn), len(leafs))
        for nnn in leafs:
            self.assertIs(n, nnn.parent.parent)
        h.add_node(-2.0).parent = n
        self.assertEqual(2*len(nn)+1, len(n.leafs))
        
    def test_root(self):
        h = H()
        n = h.add_node()
        self.assertIs(n,n.root)
        m = h.add_node(1.0)
        self.assertIs(m,m.root)
        n.parent = m
        self.assertIs(m,n.root)
        self.assertIs(m,m.root)
        nn = h.add_node(-1.0)
        nn.parent = n
        self.assertIs(m,nn.root)
        nn = h.add_node(-1.0)
        nn.parent = n
        self.assertIs(m,nn.root)
    
    def test__contex(self):
        """Try to set and get node _contex"""
        h = H()
        n = h.add_node()
        self.assertIsNone(n._context)
        n._context = "paperino"
        self.assertEqual("paperino",n._context)
        n._context = None
        self.assertIsNone(n._context)
        
    def test_get_min(self):
        """Should return self if the node is a leaf
        or has more than one child; otherwise
        return the first child that is a leaf or has
        more than one child"""
        h = H()
        n = h.add_node()
        self.assertIs(n, n.get_min())
        m = h.add_node(-1)
        m.parent = n
        self.assertIs(m, n.get_min())
        self.assertIs(m, m.get_min())
        o = h.add_node(-1)
        o.parent = n
        self.assertIs(n, n.get_min())
        self.assertIs(m, m.get_min())
        self.assertIs(o, o.get_min())
        p = h.add_node(1)
        n.parent = p
        self.assertIs(n, n.get_min())
        self.assertIs(n, p.get_min())
        self.assertIs(m, m.get_min())
        self.assertIs(o, o.get_min())
        g = h.add_node(-2)
        g.parent = m
        self.assertIs(n, n.get_min())
        self.assertIs(n, p.get_min())
        self.assertIs(g, m.get_min())
        self.assertIs(g, g.get_min())
        self.assertIs(o, o.get_min())
    
    def test_equal_subtree(self):
        h = H()
        n0 = h.add_node()
        n1 = h.add_node()
        self.assertTrue(n0.equal_subtree(n1))
        m = h.add_node(-1)
        self.assertFalse(n0.equal_subtree(m))
        self.assertFalse(n1.equal_subtree(m))
        m.parent = n0
        self.assertFalse(n0.equal_subtree(n1))
        m1 = h.add_node(-1)
        m1.parent = n1
        self.assertTrue(n0.equal_subtree(n1))
        qq = [h.add_node(-1) for _ in xrange(3)]
        for q in qq:
            q.parent = n0
        self.assertFalse(n0.equal_subtree(n1))
        qq = [h.add_node(-1) for _ in xrange(3)]
        for q in qq:
            q.parent = n1
        self.assertTrue(n0.equal_subtree(n1))
        for c in n0.children:
            s=c
            for i in xrange(4):
                v = h.add_node(c.phy-1-i)
                v.parent = s
                s = v
            for v in [h.add_node(s.phy-1)]:
                v.parent = s
        self.assertFalse(n0.equal_subtree(n1))
        for c in n1.children:
            s=c
            for i in xrange(8):
                v = h.add_node(c.phy-0.5-(i/2.0))
                v.parent = s
                s = v
            for v in [h.add_node(s.phy-1)]:
                v.parent = s
        self.assertTrue(n0.equal_subtree(n1))

    def test_equal_subtree_3_trunc(self):
        h0 = H()
        h1 = H()
        n0 = h0.add_node()
        self.assertFalse(h0.same(h1))
        self.assertTrue(h0.same(h0))
        n1 = h1.add_node()
        self.assertTrue(h0.same(h1))
        self.assertTrue(h0.same(h0))
        n00 = h0.add_node(-2)
        n01 = h0.add_node(-2)
        n02 = h0.add_node(-1.5)
        n00.parent = n01.parent = n02.parent = n0
        self.assertFalse(h0.same(h1))
        self.assertTrue(h0.same(h0))
        n10 = h1.add_node(-2)
        n11 = h1.add_node(-2)
        n12 = h1.add_node(-1.5)
        n10.parent = h1.add_node(-1)
        n11.parent = h1.add_node(-0.8)
        n12.parent = h1.add_node(-1.0)
        n10.parent.parent = n11.parent.parent = n12.parent.parent = n1 
        self.assertTrue(n0.equal_subtree(n1))
        i = 2
        for d in [n00,n01,n02,n10,n11,n12]:
            a = d.sg.add_node(-100.0)
            aa = d.sg.add_node(-100.0/i)
            i += 1
            b = d.sg.add_node(-100.0)
            bb = d.sg.add_node(-100.0/i)
            i += 1
            a.parent = aa 
            b.parent = bb 
            aa.parent = bb.parent = d
            
        self.assertTrue(n0.equal_subtree(n1))

    def test_equal_subtree_raise(self):
        """Test if the function raise the true exception"""
        h = H()
        n = h.add_node()
        self.assertRaises(ValueError, n.equal_subtree, None)
        self.assertRaises(ValueError, n.equal_subtree, "pippo")
        self.assertRaises(ValueError, n.equal_subtree, 12)
        
        
        
        
        
class Test_X_H0Tree_More(unittest.TestCase):
    
    def test_leafs(self):
        h = H()
        self.assertEqual(0, len(h.leafs))
        n = h.add_node()
        self.assertEqual(1, len(h.leafs))
        self.assertIn(n, h.leafs)
        nn = [h.add_node(-1.0) for _ in xrange(3)]
        for nnn in nn:
            nnn.parent=n
        leafs = h.leafs
        self.assertEqual(len(nn), len(leafs))
        for nnn in nn:
            self.assertIn(nnn, leafs)
            h.add_node(-2.0).parent = nnn
            h.add_node(-2.0).parent = nnn
        leafs = h.leafs
        self.assertEqual(2*len(nn), len(leafs))
        for nnn in leafs:
            self.assertIs(n, nnn.parent.parent)
        h.add_node(-2.0).parent = n
        self.assertEqual(2*len(nn)+1, len(h.leafs))
    
    def test_clean_contex(self):
        h = H()
        for x in xrange(20):
            h.add_node()._context = x
        h.clean_context()
        for n in h.nodes:
            self.assertIsNone(n._context)
        
        def test_same_components(self):
            h0 = H()
            h1 = H()
            self.assertTrue(h0.same(h1))
            self.assertRaises(ValueError, h0.same, None)
            self.assertRaises(ValueError, h0.same, "pippo")
            self.assertRaises(ValueError, h0.same, 2)
            n0 = h0.add_node()
            self.assertFalse(h0.same(h1))
            self.assertTrue(h0.same(h0))
            n1 = h1.add_node()
            self.assertTrue(h0.same(h1))
            n0.parent = h0.add_node(1)
            n0.parent.parent = h0.add_node(2)
            self.assertFalse(h0.same(h1))
            self.assertTrue(h0.same(h0))
            n1.parent = h1.add_node(2)
            self.assertTrue(h0.same(h1))
            self.assertTrue(h0.same(h0))
            n0 = h0.add_node()
            self.assertFalse(h0.same(h1))
            self.assertTrue(h0.same(h0))
            n1 = h1.add_node()
            self.assertTrue(h0.same(h1))
            self.assertTrue(h0.same(h0))
            n0 = h0.add_node()
            self.assertFalse(h0.same(h1))
            self.assertTrue(h0.same(h0))
            n1 = h1.add_node()
            self.assertTrue(h0.same(h1))
            self.assertTrue(h0.same(h0))
            n00 = h0.add_node(-2)
            n01 = h0.add_node(-2)
            n02 = h0.add_node(-1.5)
            n00.parent = n01.parent = n02.parent = n0
            self.assertFalse(h0.same(h1))
            self.assertTrue(h0.same(h0))
            n10 = h1.add_node(-2)
            n11 = h1.add_node(-2)
            n12 = h1.add_node(-1.5)
            n10.parent = h1.add_node(-1)
            n11.parent = h1.add_node(-0.8)
            n12.parent = h1.add_node(-1.0)
            n10.parent.parent = n11.parent.parent = n12.parent.parent = n1 
            self.assertTrue(h0.same(h0))
            self.assertTrue(h0.same(h1))
        
        
def _add_node(h,phy=0, children=None, parent=None):
    m = h.add_node(phy)
    if children is not None:
        try:
            m.add_children(children)
        except TypeError:
            m.add_children([children])
    if parent is not None:
        m.parent = parent
    return m

def _add_nodes(h, *args):
    return [_add_node(h, *a) for a in args]

class Test_XX_H0Tree_ComputeSF(unittest.TestCase):
        
        def test_void(self):
            h = H()
            self.assertEqual(h.get_sf(), SF())
        
        def test_dot(self):
            h = H()
            h.add_node()
            sf=h.get_sf()
            o_sf=SF()
            o_sf.new_ssf(0.0,0.0)
            self.assertEqual(sf, o_sf)

        def test_dots(self):
            h = H()
            h.add_node()
            h.add_node(-1)
            h.add_node(1)
            h.add_node(1)
            h.add_node(1)
            sf=h.get_sf()
            o_sf=SF()
            o_sf.new_ssf(0.0,0.0)
            o_sf.new_ssf(-1.0,-1.0)
            o_sf.new_ssf(1.0,1.0)
            o_sf.new_ssf(1.0,1.0)
            o_sf.new_ssf(1.0,1.0)
            self.assertEqual(sf, o_sf)
        
        def test_ReverseV(self):
            h = H()
            n=h.add_node()
            h.add_node(-1).parent = n
            h.add_node(-2).parent = n
            sf=h.get_sf()
            o_sf=SF()
            o_sf.new_ssf(-2,0.0).add_point(-1,0)
            self.assertEqual(sf, o_sf)
            h = H()
            n=h.add_node()
            m = h.add_node(-0.5)
            m.parent = n
            h.add_node(-1).parent = m
            m = h.add_node(-1)
            m.parent = n
            h.add_node(-2).parent = m
            m = h.add_node(1)
            n.parent = m
            sf=h.get_sf()
            o_sf=SF()
            o_sf.new_ssf(-2,1.0).add_point(-1,0)
            print "#######################"
            sf.dump(sys.stdout)
            print "#######################"
            o_sf.dump(sys.stdout)
            self.assertEqual(sf, o_sf)
        
        def test_I(self):
            h = H()
            nn = _add_nodes(h,(0,),(1,),(2,),(3,),(4,),(5,))
            for i in xrange(len(nn)-1):
                nn[i].parent = nn[i+1]
            o_sf=SF()
            o_sf.new_ssf(0,5)
            self.assertEqual(h.get_sf(), o_sf)
        
        def test_complex_case(self):
            '''Complex'''
            h = H()
            nn = _add_nodes(h,(0,),(0.2,),(0.1,),(1,),(1,),
                            (2,),(2,),(3,),(4,))
            nn[0].parent = nn[5]
            nn[1].parent = nn[5]
            nn[5].parent = nn[7]
            nn[7].parent = nn[8]
            nn[2].parent = nn[7]
            nn[3].parent = nn[6]
            nn[4].parent = nn[6]
            nn[6].parent = nn[8]
            o_sf=SF()
            ssf = o_sf.new_ssf(0,4)
            ssf.add_point(1,2)
            ssf.add_point(1,4)
            ssf.add_point(0.1,3)
            ssf.add_point(0.2,2)
            sf = h.get_sf()
            print "#######################"
            sf.dump(sys.stdout)
            print "#######################"
            o_sf.dump(sys.stdout)
            self.assertEqual(sf, o_sf)

        def test_Multi(self):
            h = H()
            '''dot'''
            h.add_node()
            '''Reverse V'''
            nn = _add_nodes(h,(1,),(2,),(3,))
            nn[0].parent = nn[2]
            nn[1].parent = nn[2]
            '''I'''
            nn = _add_nodes(h,(0,),(1,),(2,),(3,),(4,),(5,))
            for i in xrange(len(nn)-1):
                nn[i].parent = nn[i+1]
            '''Complex'''
            nn = _add_nodes(h,(0,),(0.2,),(0.1,),(1,),(1,),
                            (2,),(2,),(3,),(4,))
            nn[0].parent = nn[5]
            nn[1].parent = nn[5]
            nn[5].parent = nn[7]
            nn[7].parent = nn[8]
            nn[2].parent = nn[7]
            nn[3].parent = nn[6]
            nn[4].parent = nn[6]
            nn[6].parent = nn[8]
            o_sf=SF()
            o_sf.new_ssf(0,0)
            o_sf.new_ssf(0,5)
            ssf = o_sf.new_ssf(1,3)
            ssf.add_point(2,3)
            ssf = o_sf.new_ssf(0,4)
            ssf.add_point(1,2)
            ssf.add_point(1,4)
            ssf.add_point(0.1,3)
            ssf.add_point(0.2,2)
            sf = h.get_sf()
            print "#######################"
            sf.dump(sys.stdout)
            print "#######################"
            o_sf.dump(sys.stdout)
            self.assertEqual(sf, o_sf)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
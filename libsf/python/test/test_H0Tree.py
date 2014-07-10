'''
Created on 06/lug/2014

@author: michele
'''
import unittest
from sf.H0Tree import H0Tree as H
from sf.H0Tree import H0Node as N
from sf.SizeFunction import SizeFunction as SF


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
            self.assertEqual(sf, o_sf)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
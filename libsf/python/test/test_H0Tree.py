'''
Created on 06/lug/2014

@author: michele
'''
import unittest
from sf.H0Tree import H0Tree as H
from sf.H0Tree import H0Node as N

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
        self.assertEqual(0.0, n.phy)
        
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
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on 29/giu/2014

@author: michele
'''
import unittest
from sf.SizeGraph import SizeGraph as SG
from sf.SizeGraph import SizeNode as SN

class Test_000_SizeGraph(unittest.TestCase):

    def test_000_create(self):
        self.assertIsNotNone(SG())
    
    def test_010_add_node(self):
        sg = SG()
        n = sg.add_node()
        self.assertIsNotNone(n)
        self.assertEqual(sg, n.sg)
    
    def test_020_nodes(self):
        sg = SG()
        nodes = [sg.add_node() for _ in xrange(10)]
        nn = sg.nodes
        self.assertEqual(len(nodes), len(nn))
        for n in nodes:
            self.assertIn(n, nn)
            
class Test_010_SizeNode(unittest.TestCase):
    
    def test_000_create(self):
        sg0 = SG()
        sg1 = SG()
        n1 = SN(sg0)
        n2 = SN(sg0)
        n3 = SN(sg1)
        n4 = SN(sg1)
        self.assertIs(n1.sg,n2.sg)
        self.assertIsNot(n1.sg,n3.sg)
        self.assertIs(n3.sg,n4.sg)
    
    def test_010_connect(self):
        sg0 = SG()
        sg1 = SG()
        n1 = SN(sg0)
        n2 = SN(sg0)
        n3 = SN(sg1)
        n1.connect(n2)
        self.assertRaises(ValueError, n1.connect, n3)
        self.assertRaises(ValueError, n1.connect, sg0)
        self.assertRaises(ValueError, n1.connect, None)
    
    def test_020_connected(self):
        sg0 = SG()
        n1 = SN(sg0)
        n2 = SN(sg0)
        n3 = SN(sg0)
        n1.connect(n2)
        nn = n1.connected
        nnn = n2.connected
        self.assertIsNot(nn, n1._connected)
        self.assertEqual(1, len(nn))
        self.assertEqual(1, len(nnn))
        self.assertIn(n2, nn)
        self.assertIn(n1, nnn)
        n1.connect(n3)
        nn = n1.connected
        nnn = n2.connected
        nnnn = n3.connected
        self.assertEqual(2, len(nn))
        self.assertEqual(1, len(nnn))
        self.assertEqual(1, len(nnnn))
        self.assertIn(n2, nn)
        self.assertIn(n3, nn)
        self.assertIn(n1, nnn)
        self.assertIn(n1, nnnn)
        """Duplicare NON cambia nulla"""
        n1.connect(n2)
        n1.connect(n3)
        nn = n1.connected
        nnn = n2.connected
        nnnn = n3.connected
        self.assertEqual(2, len(nn))
        self.assertEqual(1, len(nnn))
        self.assertEqual(1, len(nnnn))
        self.assertIn(n2, nn)
        self.assertIn(n3, nn)
        self.assertIn(n1, nnn)
        self.assertIn(n1, nnnn)
    
    def test_030_phy(self):
        sg0 = SG()
        n1 = SN(sg0)
        self.assertEqual(0.0, n1.phy)
        n1.phy = 1.2
        self.assertEqual(1.2, n1.phy)
        self.assertRaises(ValueError, n1.__setattr__, "phy", "pippo")
    
    def test_050__contex(self):
        """Try to set and get node _contex"""
        g = SG()
        n = g.add_node()
        self.assertIsNone(n._context)
        n._context = "paperino"
        self.assertEqual("paperino",n._context)
        n._context = None
        self.assertIsNone(n._context)
        
class Test_100_SizeGraph_Extensions(unittest.TestCase):
    """Here I would like to test the advanced options like
    the node factory and the optional arguments of standard
    node factory.
    Moreover we will test get_connection() e _clea_contex functions"""
    
    def test_add_node(self):
        sg = SG()
        n = sg.add_node(1.3)
        self.assertEqual(1.3, n.phy)
        n2 = sg.add_node(n)
        self.assertIn(n, n2.connected)
        self.assertIn(n2, n.connected)
        n3 = sg.add_node(1.5,n2,n)
        self.assertEqual(1.5, n3.phy)
        self.assertIn(n3, n2.connected)
        self.assertIn(n3, n.connected)
        self.assertIn(n2, n3.connected)
        self.assertIn(n, n3.connected)
        self.assertRaises(ValueError, sg.add_node, None)
        self.assertRaises(ValueError, sg.add_node, "pippo")
        self.assertRaises(ValueError, sg.add_node, 1, "paperino")
        self.assertRaises(ValueError, sg.add_node, 1, n, "paperino")
        
    def test_nodes_factory(self):
        sg = SG(SN)
        self.assertIsInstance(sg.add_node(), SN)
        class nSN(SN):
            pass
        sg = SG(nSN)
        self.assertIsInstance(sg.add_node(), nSN)
        self.assertIs(nSN, sg.nodes_factory)
        class nnSN(object):
            def __init__(self,sg):
                pass
        self.assertRaises(ValueError, SG, nnSN)
    
    def test_get_connection(self):
        sg = SG()
        self.assertFalse(sg.get_connections())
        nn = [sg.add_node() for _i in xrange(10)]
        self.assertFalse(sg.get_connections())
        for n in nn:
            for m in nn:
                n.connect(m)
        connections = sg.get_connections()
        self.assertEqual(55, len(connections))
        for n in nn:
            for m in nn:
                self.assertTrue((n,m) in connections or (m,n) in connections)

    def test_clean_contex(self):
        g = SG()
        for x in xrange(20):
            g.add_node()._context = x
        g.clean_context()
        for n in g.nodes:
            self.assertIsNone(n._context)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
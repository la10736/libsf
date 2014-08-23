'''
Created on 29/giu/2014

@author: michele
'''
import unittest
from sf.SizeGraph import SizeGraph as SG
from sf.SizeGraph import SizeNode as SN
import sf.SizeGraph as SizeGraph
from cStringIO import StringIO as sio
from itertools import permutations
import tempfile
import os

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
    
    def test_030_remove_node(self):
        sg = SG()
        n = sg.add_node()
        self.assertEqual(1,len(sg.nodes))
        sg.remove_node(n)
        self.assertEqual(0,len(sg.nodes))
        n = sg.add_node()
        m = sg.add_node()
        r = sg.add_node()
        n.connect(m)
        n.connect(r)
        m.connect(r)
        sg.remove_node(n)
        self.assertEqual(2,len(sg.nodes))
        self.assertEqual(1,len(m.connected))
        self.assertEqual(1,len(r.connected))
        self.assertIn(r,m.connected)
        self.assertRaises(ValueError, sg.remove_node, SG().add_node())
        self.assertRaises(ValueError, sg.remove_node, None)
        
        
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
    
    def test_025_disconnect(self):
        g = SG()
        n = SN(g)
        m = SN(g)
        n.connect(m)
        self.assertEqual(1,len(n.connected))
        self.assertEqual(1,len(m.connected))
        n.disconnect(m)
        self.assertEqual(0,len(n.connected))
        self.assertEqual(0,len(m.connected))
        """Already disconnected"""
        n.disconnect(m)
        """Assert ValueError"""
        g1 = SG()
        m = SN(g1)
        self.assertRaises(ValueError, n.disconnect, m)
        self.assertRaises(ValueError, n.disconnect, None)
    
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
            
def two_graph_equal(g1,g2):
    if not g1.__class__ is g2.__class__:
        return "Not same kind of object"
    if not g1.nodes_factory is g2.nodes_factory:
        return "Not same node factory"
    if len(g1.nodes) != len(g2.nodes):
        return "Different numbers of nodes"
    if len(g1.get_connections()) != len(g2.get_connections()):
        return "Different numbers of connections"
    N = [n for n in g1.nodes]
    M = [n for n in g2.nodes]
    for p in permutations(xrange(len(N))):
        for i,n in enumerate(N):
            n._context = M[p[i]]
        ok = True
        for n in N:
            ok = (n.phy == n._context.phy) and \
                    all([nn.phy == nn._context.phy for nn in n.connected])
            if not ok:
                break
        if ok:
            return
    return "There isn't any matching"


class TSizeGraph(unittest.TestCase):
    def assertSameGraph(self,g1,g2):
        m = two_graph_equal(g1, g2)
        if m:
            self.fail(m)

class Test_100_SizeGraph_Extensions(TSizeGraph):
    """Here I would like to test the advanced options like
    the node factory and the optional arguments of standard
    node factory.
    Moreover we will test get_connection() e _clean_contex functions"""
    
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
    
    def test_get_connections(self):
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
        
    def test_copy(self):
        """Copy graph"""
        g = SG()
        self.assertSameGraph(g, g.copy())
        n = g.add_node(1.0)
        self.assertSameGraph(g, g.copy())
        nn = [n] + [g.add_node(x) for x in xrange(3)]
        self.assertSameGraph(g, g.copy())
        mm = [g.add_node(x) for x in xrange(20,24)]
        self.assertSameGraph(g, g.copy())
        for n in nn:
            for m in mm:
                n.connect(m)
        self.assertSameGraph(g, g.copy())
        for n in nn+mm:
            for m in nn+mm:
                n.connect(m)
        self.assertSameGraph(g, g.copy())

class Test_x00_SizeGraph_Utils(TSizeGraph):
    """Test the utility functions for like
    1) read from file
    2) dump to a fime
    3) export to dot graph format
    """
    
    def test_read_sg_000_nodes(self):
        g = SizeGraph.readsg(sio())
        self.assertIsInstance(g, SG)
        """Just a Node"""
        g = SizeGraph.readsg(sio("1"))
        self.assertEqual(1, len(g.nodes))
        g = SizeGraph.readsg(sio("""1"""),[0.2])
        self.assertEqual(1, len(g.nodes))
        self.assertEqual(0.2,g.nodes.pop().phy)
        g = SizeGraph.readsg(sio("""1
        MS
        0.5"""))
        self.assertEqual(1, len(g.nodes))
        self.assertEqual(0.5,g.nodes.pop().phy)

        """Just a Nodes"""
        g = SizeGraph.readsg(sio("4"))
        self.assertEqual(4, len(g.nodes))
        g = SizeGraph.readsg(sio("""4"""),[1,2,3,4])
        self.assertEqual(4, len(g.nodes))
        for i in xrange(1,5):
            self.assertIn(i,[n.phy for n in g.nodes])
        g = SizeGraph.readsg(sio("""4
        MS
        0.1
        0.2
        0.3
        0.4"""))
        self.assertEqual(4, len(g.nodes))
        for i in range(1,5):
            self.assertIn(i/10.0,[n.phy for n in g.nodes])
        """ms instead file value"""
        g = SizeGraph.readsg(sio("""4
        MS
        0.1
        0.2
        0.3
        0.4"""),[1,2,3,4])
        self.assertEqual(4, len(g.nodes))
        for i in range(1,5):
            self.assertIn(i,[n.phy for n in g.nodes])
    
    def _is_connection(self,c,phy1,phy2):
        return any([c[0].phy==phy1 and c[1].phy==phy2,
                             c[0].phy==phy2 and c[1].phy==phy1])

    def _assert_connection(self,c,phy1,phy2):
        self.assertTrue(self._is_connection(c, phy1, phy2))

    def _assert_in_connection(self,cc,phy1,phy2):
        self.assertTrue(any([
                            self._is_connection(c, phy1, phy2 ) for c in cc]))
    
    def test_read_sg_005_edges(self):
        """Just a edge"""
        g = SizeGraph.readsg(sio("""4
        MS
        0.1
        0.2
        0.3
        0.4
        1
        0 1
        """))
        self.assertEqual(4, len(g.nodes))
        C = g.get_connections()
        self.assertEqual(1, len(C))
        c = C.pop()
        self._assert_connection(c, 0.1, 0.2)
        g = SizeGraph.readsg(sio("""4
        1
        0 1
        """),ms=[.1,.2,.3,.4])
        self.assertEqual(4, len(g.nodes))
        C = g.get_connections()
        self.assertEqual(1, len(C))
        c = C.pop()
        self._assert_connection(c, 0.1, 0.2)
        """More edges"""
        g = SizeGraph.readsg(sio("""4
        MS
        0.1
        0.2
        0.3
        0.4
        4
        0 1
        1 2
        2 3
        3 0
        """))
        self.assertEqual(4, len(g.nodes))
        C = g.get_connections()
        self.assertEqual(4, len(C))
        ii=[.1,.2,.3,.4,.1]
        for i in xrange(4):
            self._assert_in_connection(C, ii[i],ii[i+1])
        g = SizeGraph.readsg(sio("""4
        4
        0 1
        1 2
        2 3
        3 0
        """),ms=[.1,.2,.3,.4])
        self.assertEqual(4, len(g.nodes))
        C = g.get_connections()
        self.assertEqual(4, len(C))
        ii=[.1,.2,.3,.4,.1]
        for i in xrange(4):
            self._assert_in_connection(C, ii[i],ii[i+1])
            
    def test_read_sg_010_comments_and_empty_lines(self):
        """Empty graph"""
        g = SizeGraph.readsg(sio("""
        
        """))
        self.assertEqual(0, len(g.nodes))
        g = SizeGraph.readsg(sio("""# comment
        
#c
 # o
         #mme
        #      nt
        
        """))
        self.assertEqual(0, len(g.nodes))
        """Just a node"""
        g = SizeGraph.readsg(sio("""
        
        1
        
        """))
        self.assertEqual(1, len(g.nodes))
        g = SizeGraph.readsg(sio("""# comment
        
#c
 # o
          1
         #mme
        #      nt
        
        """))
        self.assertEqual(1, len(g.nodes))
        """Some Nodes"""
        g = SizeGraph.readsg(sio("""
        
        4
        
        """))
        self.assertEqual(4, len(g.nodes))
        g = SizeGraph.readsg(sio("""# comment
        
#c
 # o
          5
         #mme
        #      nt
        
        """))
        self.assertEqual(5, len(g.nodes))
        g = SizeGraph.readsg(sio("""
        
        4
        
        MS
    1
    #  www
    
    2
            3
    # ha
    
    # ha
                                  4
        """))
        self.assertEqual(4, len(g.nodes))
        for i in xrange(1,5):
            self.assertIn(i, [n.phy for n in g.nodes])
        
        """Edges"""
        g = SizeGraph.readsg(sio("""# dddd
        
        4
        #co
        
        MS
#mments

        0.1
        
        #   
        0.2
        0.3
        0.4
        
        #
        
        4
#more com
        0 1
        
        
        1 2
    #    ments
        2 3
        3 0
        
        
        """))
        self.assertEqual(4, len(g.nodes))
        C = g.get_connections()
        self.assertEqual(4, len(C))
        ii=[.1,.2,.3,.4,.1]
        for i in xrange(4):
            self._assert_in_connection(C, ii[i],ii[i+1])
        
    def test_read_sg_050_asserts(self):
        """Pass wrong ms"""
        self.assertRaises(ValueError, SizeGraph.readsg,
                          f=sio("""2"""),ms=[1])
        """Sanity check"""
        SizeGraph.readsg(f=sio("""2"""),ms=[1,2,3])
        
        """Invalid formats"""
        self.assertRaises(ValueError, SizeGraph.readsg,
                          f=sio("""1.2"""))
        self.assertRaises(ValueError, SizeGraph.readsg,
                  f=sio("""1.2"""))
        self.assertRaises(ValueError, SizeGraph.readsg,
                  f=sio("""1
                  paperino"""))
        self.assertRaises(ValueError, SizeGraph.readsg,
                  f=sio("""1
                  1.3"""))
        self.assertRaises(ValueError, SizeGraph.readsg,
                  f=sio("""1
                  MS
                  qqq"""))
        self.assertRaises(ValueError, SizeGraph.readsg,
                  f=sio("""1
                  MS
                  1.2
                  2.2
                  """))
        self.assertRaises(ValueError, SizeGraph.readsg,
                  f=sio("""1
                  MS
                  1.2
                  pippo
                  """))
        self.assertRaises(ValueError, SizeGraph.readsg,
                  f=sio("""2
                  MS
                  1.2
                  2.3
                  1
                  a 2
                  """))
        self.assertRaises(ValueError, SizeGraph.readsg,
                  f=sio("""2
                  MS
                  1.2
                  2.3
                  1
                  1 a
                  """))
        self.assertRaises(ValueError, SizeGraph.readsg,
                  f=sio("""2
                  MS
                  1.2
                  2.3
                  1
                  paperino
                  """))
        self.assertRaises(ValueError, SizeGraph.readsg,
                  f=sio("""2
                  MS
                  1.2
                  2.3
                  1
                  0.2 1.1
                  """))

    def test_read_sg_x00_from_file_real_file(self):
        p = tempfile.mktemp()
        f = file(p, "w")
        try:
            f.write("""1
            MS
            1.1
            """)
            f.close()
            g = SG()
            g.add_node(1.1)
            self.assertSameGraph(g, SizeGraph.readsg(p))
        finally:
            os.unlink(p)
    
    def test_xxx_dump_read_sg_dual(self):
        g = SG()
        N = [g.add_node(.1), g.add_node(.2), g.add_node(.3), g.add_node(.4) ]
        N[0].connect(N[1])
        N[0].connect(N[2])
        N[1].connect(N[3])
        f = sio()
        g.dump(f)
        f.seek(0)
        self.assertSameGraph(g, SizeGraph.readsg(f))
        print f.getvalue()

    def test_xxx_dump_options(self):
        g = SG()
        N = [g.add_node(.1), g.add_node(.2), g.add_node(.3), g.add_node(.4) ]
        N[0].connect(N[1])
        N[0].connect(N[2])
        N[1].connect(N[3])
        f = sio()
        g.dump(f,legacy=True)
        f.seek(0)
        print """LEGACY ########################
        """ + f.getvalue()
        self.assertSameGraph(g, SizeGraph.readsg(f,ms=[.1,.2,.3,.4]))
        self.assertNotIn("#", f.getvalue())
        self.assertNotIn("MS", f.getvalue())
        f = sio()
        g.dump(f,comments=False)
        f.seek(0)
        print """COMMENTS ########################
        
        """ + f.getvalue()
        self.assertSameGraph(g, SizeGraph.readsg(f))
        self.assertNotIn("#", f.getvalue())
        self.assertIn("MS", f.getvalue())
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on 26/lug/2014

@author: michele
'''
import unittest
from sf.UnionFind import Set

class Test(unittest.TestCase):


    def test_0000_create(self):
        self.assertIsNotNone(Set())
        self.assertIsNotNone(Set("pippo"))
    
    def test_0001_find_base(self):
        s = Set()
        self.assertIs(s, s.find())

    def test_0002_union_base(self):
        a = Set()
        b = Set()
        self.assertIsNot(a.find(), b.find())
        r = a.union(b)
        self.assertIs(r, a.find())
        self.assertIs(r, b.find())
        self.assertIs(r, b.union(a))
        self.assertRaises(ValueError, a.union, "pippo")
        self.assertRaises(Exception, a.union, None)
        c,d = Set("Pippo"), Set("Pluto")
        r = c.union(d)
        self.assertIsNone(r.contex)
        c,d = Set(), Set()
        r = c.union(d, "paperino")
        self.assertEqual("paperino", r.contex)
        
    def test_0003_contex_base(self):
        s = Set()
        self.assertIsNone(s.contex)
        s.contex = "pippo"
        self.assertEqual("pippo", s.contex)
        
    def test_0004_contex_union(self):
        c,d = Set(), Set()
        c.union(d, "ooo")
        self.assertEqual("ooo", c.contex)
        self.assertEqual("ooo", d.contex)
        e,f = Set(), Set()
        e.union(f).union(c,"sss")
        for a in [c,d,e,f]:
            self.assertEqual("sss", a.contex)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

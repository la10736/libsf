'''
Created on 26/lug/2014

@author: michele
'''
import unittest
import sf.UnionFind

class Test_Base_Union_Find(unittest.TestCase):

    impl = sf.UnionFind.Set

    def test_0000_create(self):
        self.assertIsNotNone(self.impl())
        self.assertIsNotNone(self.impl("pippo"))
    
    def test_0001_find_base(self):
        s = self.impl()
        self.assertIs(s, s.find())

    def test_0002_union_base(self):
        a = self.impl()
        b = self.impl()
        self.assertIsNot(a.find(), b.find())
        r = a.union(b)
        self.assertIs(r, a.find())
        self.assertIs(r, b.find())
        self.assertIs(r, b.union(a))
        self.assertRaises(ValueError, a.union, "pippo")
        self.assertRaises(Exception, a.union, None)
        c,d = self.impl("Pippo"), self.impl("Pluto")
        r = c.union(d)
        self.assertIsNone(r.contex)
        c,d = self.impl(), self.impl()
        r = c.union(d, "paperino")
        self.assertEqual("paperino", r.contex)
        
    def test_0003_contex_base(self):
        s = self.impl()
        self.assertIsNone(s.contex)
        s.contex = "pippo"
        self.assertEqual("pippo", s.contex)
        
    def test_0004_contex_union(self):
        c,d = self.impl(), self.impl()
        c.union(d, "ooo")
        self.assertEqual("ooo", c.contex)
        self.assertEqual("ooo", d.contex)
        e,f = self.impl(), self.impl()
        e.union(f).union(c,"sss")
        for a in [c,d,e,f]:
            self.assertEqual("sss", a.contex)

class Test_Rank_Union_Find(Test_Base_Union_Find):
    
    impl = sf.UnionFind.UnionFind_by_rank



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

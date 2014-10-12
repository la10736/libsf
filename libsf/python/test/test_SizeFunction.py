'''
Created on 21/giu/2014

@author: michele
'''
import unittest
import sf.SizeFunction as SF
from sf.SizeFunction import _AngularPoint as AP 
from sf.SizeFunction import SimpleSizeFunctionOld
from sf.SizeFunction import SimpleSizeFunction
from sf.SizeFunction import readsf
from cStringIO import StringIO as sio
import tempfile
import os

class Test_AngularPoint(unittest.TestCase):


    def test_Create(self):
        self.assertIsNotNone(AP(0, 2))
        self.assertRaises(TypeError, AP)
        self.assertRaises(TypeError, AP, 1.2)
        self.assertRaises(ValueError, AP, "pluto", 1.2)
        self.assertRaises(ValueError, AP, 1.3, "pluto")
        self.assertRaises(ValueError, AP, None, None)
        self.assertRaises(ValueError, AP, 1, 0)
        self.assertRaises(ValueError, AP, 1.3, 1.3)
        self.assertIsNotNone(AP(1.4, 1.5))
    
    def test_Equal(self):
        points = [[AP(x, y) for x, y in 
              ((0, 2), (1, 2), (0, 1), (0, 2), (1, 2), (0, 1))],
                  [AP(x, y) for x, y in 
              ((0.1, 2.1), (1.1, 2.1), (0.1, 1.1), (0.1, 2.1), (1.1, 2.1), (0.1, 1.1))]]
        for a, b, c, aa, bb, cc in points:
            self.assertNotEqual(a, b)
            self.assertNotEqual(a, c)
            self.assertNotEqual(b, c)
            self.assertEqual(a, aa)
            self.assertEqual(b, bb)
            self.assertEqual(c, cc)
            self.assertEqual(a, a)
            self.assertEqual(b, b)
            self.assertEqual(c, c)
            self.assertEqual(aa, aa)
            self.assertEqual(bb, bb)
            self.assertEqual(cc, cc)

    def test_Equal_other_type(self):
        self.assertNotEqual(AP(1, 2), None)
        class a(object):
            def __init__(self):
                self._x = 1
                self._y = 2
        self.assertNotEqual(AP(1, 2), a())
    
    def test_coords(self):
        ap = AP(1, 2)
        self.assertEqual(ap.x, 1)
        self.assertEqual(ap.y, 2)

    def test_create_arge(self):
        ap = AP(x=1, y=2)
        self.assertEqual(ap.x, 1)
        self.assertEqual(ap.y, 2)
    
    def test_copy(self):
        ap = AP(1, 2)
        ap2 = ap.copy()
        self.assertEqual(ap, ap2)
        self.assertFalse(ap is ap2)

class Test_SimpleSizeFunctionOld(unittest.TestCase):
    
    def test_Create(self):
        self.assertIsNotNone(SimpleSizeFunctionOld(-2))
        self.assertRaises(TypeError, SimpleSizeFunctionOld)
        self.assertRaises(ValueError, SimpleSizeFunctionOld, "pluto")
        self.assertRaises(ValueError, SimpleSizeFunctionOld, None)
    
    def test_cl(self):
        ssf = SimpleSizeFunctionOld(2)
        self.assertEqual(ssf.cornerline, 2)
    
    def test_add_point(self):
        ssf = SimpleSizeFunctionOld(-2)
        ssf.add_point(1, 2)
        ap = AP(1, 2)
        self.assertIn(ap, ssf.get_points())
        self.assertRaises(ValueError, ssf.add_point, -3, 2)
        ssf.add_point(1.1, 2.2)
        self.assertIn(AP(1.1, 2.2), ssf.points)
        ssf.add_point(1, 2)
        self.assertEqual(2, ssf.points.count(ap))
    
    def test_equal(self):
        ssf1 = SimpleSizeFunctionOld(-2)
        ssf1.add_point(1, 2)
        ssf2 = SimpleSizeFunctionOld(-2)
        ssf2.add_point(1, 2)
        self.assertEqual(ssf1, ssf2)
        ssf2.add_point(2, 3)
        self.assertNotEqual(ssf1, ssf2)
        ssf1.add_point(2, 3)
        self.assertEqual(ssf1, ssf2)
        ssf2.add_point(2, 3)
        self.assertNotEqual(ssf1, ssf2)
        ssf1.add_point(2, 3)
        self.assertEqual(ssf1, ssf2)
        ssf1 = SimpleSizeFunctionOld(0)
        ssf2 = SimpleSizeFunctionOld(0.5)
        self.assertNotEqual(ssf1, ssf2)
    
    def test_equal_fail_other_type(self):
        class a(object):
            def __init__(self):
                self._cl = -2
                self.points = []
        self.assertNotEqual(SimpleSizeFunctionOld(-2), a())
    
    def test_not_equal(self):
        ssf1 = SimpleSizeFunctionOld(-2, [(1, 2), (2, 3)])
        ssf2 = ssf1.copy()
        self.assertFalse(ssf1 != ssf2)
    
    def test_Create_points(self):
        ssf1 = SimpleSizeFunctionOld(-2, [(1, 2), (2, 3)])
        ssf2 = SimpleSizeFunctionOld(-2)
        ssf2.add_point(1, 2)
        ssf2.add_point(2, 3)
        self.assertEqual(ssf1, ssf2)
        ssf1 = SimpleSizeFunctionOld(-2, [AP(1, 2), AP(2, 3)])
        self.assertEqual(ssf1, ssf2)
        ssf1 = SimpleSizeFunctionOld(-2, ((1, 2), (2, 3)))
        self.assertEqual(ssf1, ssf2)
        ssf1 = SimpleSizeFunctionOld(-2, (AP(1, 2), AP(2, 3)))
        self.assertEqual(ssf1, ssf2)
        ssf1 = SimpleSizeFunctionOld(-2, [(1, 2), AP(2, 3), (3, 4), AP(4, 5)])
        ssf2 = SimpleSizeFunctionOld(-2)
        ssf2.add_point(1, 2)
        ssf2.add_point(2, 3)
        ssf2.add_point(3, 4)
        ssf2.add_point(4, 5)
        self.assertEqual(ssf1, ssf2)

    def test_Create_nominal_args(self):
        ssf1 = SimpleSizeFunctionOld(cl=-2, points=[(1, 2), (2, 3)])
        ssf2 = SimpleSizeFunctionOld(points=[(1, 2), (2, 3)], cl=-2)
        self.assertEqual(ssf1, ssf2)
    
    def test_copy(self):
        ssf1 = SimpleSizeFunctionOld(-2, [(1, 2), (2, 3)])
        ssf2 = ssf1.copy()
        self.assertIsInstance(ssf2, SimpleSizeFunctionOld)
        self.assertEqual(ssf1, ssf2)
        self.assertFalse(ssf1 is ssf2)
        ap = ssf1._points[0]
        for p in ssf2._points:
            self.assertFalse(ap is p)
        
class Test_SimpleSizeFunction(unittest.TestCase):
    
    def test_Create(self):
        ssf = SimpleSizeFunction(-2, 3)
        self.assertIsInstance(ssf, SimpleSizeFunctionOld)
        self.assertRaises(TypeError, SimpleSizeFunction)
        self.assertRaises(ValueError, SimpleSizeFunction, "pluto", 3)
        self.assertRaises(ValueError, SimpleSizeFunction, 3, "pluto")

    def test_add_point(self):
        ssf = SimpleSizeFunction(-2, 5)
        ssf.add_point(1, 2)
        ap = AP(1, 2)
        self.assertIn(ap, ssf.get_points())
        self.assertRaises(ValueError, ssf.add_point, -3, 2)
        self.assertRaises(ValueError, ssf.add_point, -1, 6)
        ssf.add_point(1.1, 2.2)
        self.assertIn(AP(1.1, 2.2), ssf.points)
        ssf.add_point(1, 2)
        self.assertEqual(2, ssf.points.count(ap))
    
    def test_maximum(self):
        ssf = SimpleSizeFunction(2)
        self.assertIsNone(ssf.maximum)

    def test_equal(self):
        ssf1 = SimpleSizeFunction(-2, 5)
        ssf1.add_point(1, 2)
        ssf2 = SimpleSizeFunction(-2, 5)
        ssf2.add_point(1, 2)
        self.assertEqual(ssf1, ssf2)
        ssf2.add_point(2, 3)
        self.assertNotEqual(ssf1, ssf2)
        ssf1.add_point(2, 3)
        self.assertEqual(ssf1, ssf2)
        ssf2.add_point(2, 3)
        self.assertNotEqual(ssf1, ssf2)
        ssf1.add_point(2, 3)
        self.assertEqual(ssf1, ssf2)
        ssf1 = SimpleSizeFunction(0)
        ssf2 = SimpleSizeFunction(0)
        self.assertEqual(ssf1, ssf2)
        ssf1 = SimpleSizeFunction(0, 3)
        ssf2 = SimpleSizeFunction(0, 4)
        self.assertNotEqual(ssf1, ssf2)
        ssf2 = SimpleSizeFunction(0)
        self.assertNotEqual(ssf1, ssf2)
        ssf1 = SimpleSizeFunction(0)
        ssf2 = SimpleSizeFunctionOld(0)
        self.assertEqual(ssf1, ssf2)
        self.assertEqual(ssf2, ssf1)
        ssf1 = SimpleSizeFunction(0, 3)
        self.assertNotEqual(ssf1, ssf2)
        self.assertNotEqual(ssf2, ssf1)
        
    def test_Create_nominal_args(self):
        ssf1 = SimpleSizeFunction(cl=-2, m=5, points=[(1, 2), (2, 3)])
        ssf2 = SimpleSizeFunction(points=[(1, 2), (2, 3)], cl=-2, m=5)
        self.assertEqual(ssf1, ssf2)

    def test_copy(self):
        ssf1 = SimpleSizeFunction(-2, 5, [(1, 2), (2, 3)])
        ssf2 = ssf1.copy()
        self.assertIsInstance(ssf2, SimpleSizeFunction)
        self.assertEqual(ssf1, ssf2)
        self.assertFalse(ssf1 is ssf2)
        ap = ssf1._points[0]
        for p in ssf2._points:
            self.assertFalse(ap is p)

class Test_SizeFunctionOld(unittest.TestCase):
    
    def test_Create(self):
        SF.SizeFunctionOld()
    
    def test_new_ssf(self):
        sf = SF.SizeFunctionOld()
        ssf = sf.new_ssf(cl=-2, points=((0, 1), (1, 2)))
        self.assertIsInstance(ssf, SimpleSizeFunctionOld)
        self.assertEqual(ssf, SimpleSizeFunctionOld(-2, ((0, 1), (1, 2))))
    
    def test_add(self):
        sf = SF.SizeFunctionOld()
        ssf = SimpleSizeFunctionOld(cl=-2, points=((0, 1), (1, 2)))
        ssf2 = sf.add(ssf)
        self.assertEqual(ssf, sf._ssfs[0])
        self.assertFalse(ssf is sf._ssfs[0])
        self.assertIsInstance(ssf2, SimpleSizeFunctionOld)
        self.assertEqual(ssf, ssf2)
        self.assertIs(ssf2, sf._ssfs[0])
        self.assertRaises(ValueError, sf.add,
                          SimpleSizeFunction(-1, 5, ((1, 2), (1.5, 2.5))))

    def test_equal(self):
        sf1 = SF.SizeFunctionOld()
        sf2 = SF.SizeFunctionOld()
        self.assertEqual(sf1, sf2)
        ssf1 = sf1.new_ssf(1)
        self.assertNotEqual(sf1, sf2)
        ssf2 = sf2.new_ssf(1)
        self.assertEqual(sf1, sf2)
        ssf1.add_point(2, 3)
        self.assertNotEqual(sf1, sf2)
        ssf2.add_point(2, 3)
        self.assertEqual(sf1, sf2)
        sf1.add(ssf1)
        self.assertNotEqual(sf1, sf2)
        sf2.add(ssf1)
        self.assertEqual(sf1, sf2)
    
    def test_ssfs(self):
        sf = SF.SizeFunctionOld()
        ssf = sf.new_ssf(1)
        ssf.add_point(2, 3)
        ssfs = sf.ssfs
        self.assertEqual(1, len(ssfs))
        self.assertEqual(ssf, ssfs[0])
        sf.add(ssf)
        ssfs = sf.ssfs
        self.assertEqual(2, len(ssfs))
        self.assertEqual(ssf, ssfs[0])
        self.assertEqual(ssf, ssfs[1])
    
    def test_copy(self):
        sf1 = SF.SizeFunctionOld()
        sf1.new_ssf(1).add_point(2, 3)
        sf2 = sf1.copy()
        self.assertIsInstance(sf2, SF.SizeFunctionOld)
        self.assertEqual(sf1, sf2)
        self.assertFalse(sf1 is sf2)
        
        
class Test_SizeFunction(unittest.TestCase):
    
    def test_Create(self):
        SF.SizeFunction()
    
    def test_new_ssf(self):
        sf = SF.SizeFunction()
        ssf = sf.new_ssf(cl=-2, m=5, points=((0, 1), (1, 2)))
        self.assertIsInstance(ssf, SimpleSizeFunction)
        self.assertEqual(ssf, SimpleSizeFunction(-2, 5, ((0, 1), (1, 2))))
        ssf = sf.new_ssf(cl=-2, points=((0, 1), (1, 2)))
        self.assertEqual(ssf, SimpleSizeFunction(-2, None, ((0, 1), (1, 2))))
        
    def test_add(self):
        sf = SF.SizeFunction()
        ssf = SimpleSizeFunction(cl=-2, m=5, points=((0, 1), (1, 2)))
        sf.add(ssf)
        self.assertEqual(ssf, sf._ssfs[0])
        self.assertFalse(ssf is sf._ssfs[0])
        self.assertRaises(ValueError, sf.add,
                          SimpleSizeFunctionOld(-1, ((1, 2), (1.5, 2.5))))
        
    def test_equal(self):
        sf1 = SF.SizeFunction()
        sf2 = SF.SizeFunction()
        self.assertEqual(sf1, sf2)
        ssf1 = sf1.new_ssf(1, 5)
        self.assertNotEqual(sf1, sf2)
        ssf2 = sf2.new_ssf(1, 5)
        self.assertEqual(sf1, sf2)
        ssf1.add_point(2, 3)
        self.assertNotEqual(sf1, sf2)
        ssf2.add_point(2, 3)
        self.assertEqual(sf1, sf2)
        sf1.add(ssf1)
        self.assertNotEqual(sf1, sf2)
        sf2.add(ssf1)
        self.assertEqual(sf1, sf2)
    
    def test_ssfs(self):
        sf = SF.SizeFunction()
        ssf = sf.new_ssf(1, 5)
        ssf.add_point(2, 3)
        ssfs = sf.ssfs
        self.assertEqual(1, len(ssfs))
        self.assertEqual(ssf, ssfs[0])
        sf.add(ssf)
        ssfs = sf.ssfs
        self.assertEqual(2, len(ssfs))
        self.assertEqual(ssf, ssfs[0])
        self.assertEqual(ssf, ssfs[1])

    def test_copy(self):
        sf1 = SF.SizeFunction()
        sf1.new_ssf(1).add_point(2, 3)
        sf2 = sf1.copy()
        self.assertIsInstance(sf2, SF.SizeFunction)
        self.assertEqual(sf1, sf2)
        self.assertFalse(sf1 is sf2)

class Test_XXX_SizeFunction_Utils(unittest.TestCase):
    
    def test_read_sf_from_file_0000(self):
        empty = SF.SizeFunctionOld()
        """Empty"""
        self.assertEqual(empty, readsf(f = sio()))
        """Just Empty lines"""
        self.assertEqual(empty, readsf(f = sio("""
        
        """)))
        """Just Comments"""
        self.assertEqual(empty, readsf(f = sio("""#Just
  #S
 #o
#m
  #e
   #         COMMENTS########
################""")))
        """Comments and empty"""
        self.assertEqual(empty, readsf(f = sio("""# Comment
################""")))
        """A Line """
        sf = SF.SizeFunctionOld()
        sf.new_ssf(0.0)
        self.assertEqual(sf, readsf(sio("""l 0 0.0""")))
        """A Line min max"""
        sf = SF.SizeFunction()
        sf.new_ssf(0.0, 1.0)
        self.assertEqual(sf, readsf(sio("""l 0 0.0 1.0""")))
        """Two lines min max"""
        sf = SF.SizeFunction()
        sf.new_ssf(0.0, 1.0)
        sf.new_ssf(-30.0, 20.0)
        self.assertEqual(sf, readsf(sio("""l 0 0.0 1.0
        l 1 -30 20""")))
        """Two lines mix"""
        sf = SF.SizeFunction()
        sf.new_ssf(0.0, 1.0)
        sf.new_ssf(-30.0)
        self.assertEqual(sf, readsf(sio("""l 0 0.0 1.0
        l 1 -30""")))
        """Line and points"""
        sf = SF.SizeFunction()
        sf.new_ssf(-2.0, 1.0, [(0.1,.5),(-1,0.4)])
        self.assertEqual(sf, readsf(sio("""l 0 -2.0 1.0
        p 1 0.1 0.5
        p 2 -1.0 0.4""")))
        """Lines and points"""
        sf = SF.SizeFunction()
        sf.new_ssf(-2.0, 1.0, [(0.1,.5),(-1,0.4)])
        sf.new_ssf(-23.0, 31.0, [(-0.1,5),(-12,0.44)])
        self.assertEqual(sf, readsf(sio("""l 0 -2.0 1.0
        p 1 0.1 0.5
        p 2 -1.0 0.4
        l 3 -23 31
        p 4 -0.1 5
        p 5 -12 0.44""")))
        """Lines and points empty and comments"""
        sf = SF.SizeFunction()
        sf.new_ssf(-2.0, 1.0, [(0.1,.5),(-1,0.4)])
        sf.new_ssf(-23.0, 31.0, [(-0.1,5),(-12,0.44)])
        self.assertEqual(sf, readsf(sio("""
        # first comment
           l 0 -2.0 1.0
        # second comment
        
p 1 0.1 0.5
   p 2 -1.0 0.4
        #l 3 -23 31
        l 3 -23 31
        #more comment
        
        p 4 -0.1 5
        p 5 -12 0.44
        
        """)))
        
    def test_read_sf_from_file_asserts(self):
        """Wrong line"""
        self.assertRaises(ValueError, readsf, sio("l"))
        self.assertRaises(ValueError, readsf, sio("l 0"))
        self.assertRaises(ValueError, readsf, sio("l p"))
        self.assertRaises(ValueError, readsf, sio("l 0 p"))
        self.assertRaises(ValueError, readsf, sio("l 0 1 p"))
        """Wrong point"""
        self.assertRaises(ValueError, readsf, sio("""l 0 0
        p 1"""))
        self.assertRaises(ValueError, readsf, sio("""l 0 0
        p 1 12"""))
        self.assertRaises(ValueError, readsf, sio("""l 0 0
        p 1 p p"""))
        """Wrong character"""
        self.assertRaises(ValueError, readsf, sio("c"))
        """Point without any line"""
        self.assertRaises(ValueError, readsf, sio("p 0 0 1"))
        """Wrong Position"""
        self.assertRaises(ValueError, readsf, sio("l 1 0"))
        self.assertRaises(ValueError, readsf, sio("""l 0 0
        l 2 1"""))
        self.assertRaises(ValueError, readsf, sio("""l 0 0
        l 0 1"""))
        self.assertRaises(ValueError, readsf, sio("""l 0 0
        p 2 0 1"""))
        
    def test_read_sf_from_file_dump_dual(self):
        sf = SF.SizeFunction()
        sf.new_ssf(-10,10, [(-3,2),(-5,-2),(2,9),(-1,1)])
        sf.new_ssf(-3,12, [(-1,2),(2,10),(2,11),(-1,3)])
        f=sio()
        sf.dump(f)
        f.seek(0)
        self.assertEqual(sf, readsf(f))

    def test_read_sf_from_file_real_file(self):
        p = tempfile.mktemp()
        f = file(p, "w")
        try:
            f.write("""l 0 0 1
            p 1 .1 .5""")
            f.close()
            sf = SF.SizeFunction()
            sf.new_ssf(0,1, [(.1,.5)])
            self.assertEqual(sf, readsf(p))
        finally:
            os.unlink(p)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test']
    unittest.main()

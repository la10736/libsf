'''
Created on 21/giu/2014

@author: michele
'''
import unittest
import sf.SizeFunction as SF
from sf.SizeFunction import _AngularPoint as AP, SimpleSizeFunctionOld

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
        self.assertIsNotNone(SF.SimpleSizeFunctionOld(-2))
        self.assertRaises(TypeError, SF.SimpleSizeFunctionOld)
        self.assertRaises(ValueError, SF.SimpleSizeFunctionOld, "pluto")
        self.assertRaises(ValueError, SF.SimpleSizeFunctionOld, None)
    
    def test_cl(self):
        ssf = SF.SimpleSizeFunctionOld(2)
        self.assertEqual(ssf.cornerline, 2)
    
    def test_add_point(self):
        ssf = SF.SimpleSizeFunctionOld(-2)
        ssf.add_point(1, 2)
        ap = AP(1, 2)
        self.assertIn(ap, ssf.get_points())
        self.assertRaises(ValueError, ssf.add_point, -3, 2)
        ssf.add_point(1.1, 2.2)
        self.assertIn(AP(1.1, 2.2), ssf.points)
        ssf.add_point(1, 2)
        self.assertEqual(2, ssf.points.count(ap))
    
    def test_equal(self):
        ssf1 = SF.SimpleSizeFunctionOld(-2)
        ssf1.add_point(1, 2)
        ssf2 = SF.SimpleSizeFunctionOld(-2)
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
        ssf1 = SF.SimpleSizeFunctionOld(0)
        ssf2 = SF.SimpleSizeFunctionOld(0.5)
        self.assertNotEqual(ssf1, ssf2)
    
    def test_equal_fail_other_type(self):
        class a(object):
            def __init__(self):
                self._cl = -2
                self.points = []
        self.assertNotEqual(SimpleSizeFunctionOld(-2), a())
    
    def test_not_equal(self):
        ssf1 = SF.SimpleSizeFunctionOld(-2, [(1, 2), (2, 3)])
        ssf2 = ssf1.copy()
        self.assertFalse(ssf1 != ssf2)
    
    def test_Create_points(self):
        ssf1 = SF.SimpleSizeFunctionOld(-2, [(1, 2), (2, 3)])
        ssf2 = SF.SimpleSizeFunctionOld(-2)
        ssf2.add_point(1, 2)
        ssf2.add_point(2, 3)
        self.assertEqual(ssf1, ssf2)
        ssf1 = SF.SimpleSizeFunctionOld(-2, [AP(1, 2), AP(2, 3)])
        self.assertEqual(ssf1, ssf2)
        ssf1 = SF.SimpleSizeFunctionOld(-2, ((1, 2), (2, 3)))
        self.assertEqual(ssf1, ssf2)
        ssf1 = SF.SimpleSizeFunctionOld(-2, (AP(1, 2), AP(2, 3)))
        self.assertEqual(ssf1, ssf2)
        ssf1 = SF.SimpleSizeFunctionOld(-2, [(1, 2), AP(2, 3), (3, 4), AP(4, 5)])
        ssf2 = SF.SimpleSizeFunctionOld(-2)
        ssf2.add_point(1, 2)
        ssf2.add_point(2, 3)
        ssf2.add_point(3, 4)
        ssf2.add_point(4, 5)
        self.assertEqual(ssf1, ssf2)

    def test_Create_nominal_args(self):
        ssf1 = SF.SimpleSizeFunctionOld(cl=-2, points=[(1, 2), (2, 3)])
        ssf2 = SF.SimpleSizeFunctionOld(points=[(1, 2), (2, 3)], cl=-2)
        self.assertEqual(ssf1, ssf2)
    
    def test_copy(self):
        ssf1 = SF.SimpleSizeFunctionOld(-2, [(1, 2), (2, 3)])
        ssf2 = ssf1.copy()
        self.assertEqual(ssf1, ssf2)
        self.assertFalse(ssf1 is ssf2)
        ap = ssf1._points[0]
        for p in ssf2._points:
            self.assertFalse(ap is p)
        
class Test_SimpleSizeFunction(unittest.TestCase):
    
    def test_Create(self):
        ssf = SF.SimpleSizeFunction(-2, 3)
        self.assertIsInstance(ssf, SimpleSizeFunctionOld)
        self.assertRaises(TypeError, SF.SimpleSizeFunction)
        self.assertRaises(ValueError, SF.SimpleSizeFunction, "pluto", 3)
        self.assertRaises(ValueError, SF.SimpleSizeFunction, 3, "pluto")

    def test_add_point(self):
        ssf = SF.SimpleSizeFunction(-2, 5)
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
        ssf = SF.SimpleSizeFunction(2)
        self.assertIsNone(ssf.maximum)

    def test_equal(self):
        ssf1 = SF.SimpleSizeFunction(-2, 5)
        ssf1.add_point(1, 2)
        ssf2 = SF.SimpleSizeFunction(-2, 5)
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
        ssf1 = SF.SimpleSizeFunction(0)
        ssf2 = SF.SimpleSizeFunction(0)
        self.assertEqual(ssf1, ssf2)
        ssf1 = SF.SimpleSizeFunction(0, 3)
        ssf2 = SF.SimpleSizeFunction(0, 4)
        self.assertNotEqual(ssf1, ssf2)
        ssf2 = SF.SimpleSizeFunction(0)
        self.assertNotEqual(ssf1, ssf2)
        ssf1 = SF.SimpleSizeFunction(0)
        ssf2 = SF.SimpleSizeFunctionOld(0)
        self.assertEqual(ssf1,ssf2)
        self.assertEqual(ssf2,ssf1)
        ssf1 = SF.SimpleSizeFunction(0,3)
        self.assertNotEqual(ssf1,ssf2)
        self.assertNotEqual(ssf2,ssf1)
        
    def test_Create_nominal_args(self):
        ssf1 = SF.SimpleSizeFunction(cl=-2, M=5, points=[(1, 2), (2, 3)])
        ssf2 = SF.SimpleSizeFunction(points=[(1, 2), (2, 3)], cl=-2, M=5)
        self.assertEqual(ssf1, ssf2)
            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test']
    unittest.main()

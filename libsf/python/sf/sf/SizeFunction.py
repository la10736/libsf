'''
Created on 21/giu/2014

@author: michele
'''

class _AngularPoint(object):
    '''
    Angular Point
    '''
    def __init__(self, x, y):
        if not all((isinstance(x, (int, long, float)),
                    isinstance(y, (int, long, float)))):
            raise ValueError("The coordinate of angular point must be numbers")
        if x >= y:
            raise ValueError("In Angular point y MUST be greater than x but %s>=%s " % 
                             (x, y))
        self._x = x
        self._y = y
    
    def __eq__(self, other):
        if not isinstance(other, _AngularPoint):
            return False
        return self._x == other._x and self._y == other._y
    
    def copy(self):
        return _AngularPoint(self._x, self._y)
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
class SimpleSizeFunctionOld(object):
    """The Simple Size Function object: a collection of angular point 
    and a corner line (so a size function of a connected size graph).
    That is the old legacy version with no info about the maximum value
    of measuring function on the size graph
    """
    
    def __init__(self, cl, points=[]):
        """Create a simple size function where cl is the corner line 
        (the minimum of the measuring function on the size graph).
        
        @param cl: The corner line
        @param points: the angular points that can be both _Angularpoins and
        tuple of coordinates.
        """
        if not isinstance(cl, (int, long, float)):
            raise ValueError("The value of the corner line must be number")
        self._cl = cl
        self._points = [ap.copy() if isinstance(ap, _AngularPoint) else _AngularPoint(*ap)
                        for ap in points]
    
    @property
    def cornerline(self):
        return self._cl
    
    def _add_ap(self, ap):
        if ap.x < self._cl:
            raise ValueError("Cannot add a cornerpoint at the left of the corner line %s<%s" % 
                             (ap.x, self._cl))
        self._points.append(ap)
    
    def add_point(self, x, y):
        """ Add a angular point (x,y)
        @param x: the x coordinate
        @param y: the x coordinate
        @raise ValueError: if x or y are not numbers, y<=x or x is less
        than the corner line
        """
        self._add_ap(_AngularPoint(x, y))
    
    def get_points(self):
        return self._points[:]
    
    @property
    def points(self):
        return self.get_points()
    
    def __eq__(self, other):
        if other.__class__ != self.__class__:
            if not isinstance(other, SimpleSizeFunctionOld):
                return False
            if other.__class__ != SimpleSizeFunctionOld:
                return other.__eq__(self)
        if self._cl != other._cl:
            return False
        op = other.points
        
        for p in self._points:
            try:
                op.remove(p)
            except ValueError:
                return False
        if op:
            return False
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def copy(self):
        return SimpleSizeFunctionOld(self._cl, self._points)

class SimpleSizeFunction(SimpleSizeFunctionOld):
    """The Simple Size Function object: a collection of angular point 
    and a corner line (so a size function of a connected size graph).
    That is the old legacy version with no info about the maximum value
    of measuring function on the size graph
    """
    
    def __init__(self, cl, M=None, points=[]):
        """Create a simple size function where cl is the corner line 
        (the minimum of the measuring function on the size graph).
        M is the maximum of the measuring function that could be None, 
        in that case the SimpleSizeFunction have the same behaviour of
        a SimpleSizeFunctionOld.
        
        @param cl: The corner line
        @param M: The maximum of the measuring function
        @param points: the angular points that can be both _Angularpoins and
        tuple of coordinates.
        """
        if M is not None and not isinstance(M, (int, long, float)):
            raise ValueError("The value of the maximum of measuring function must be number")
        self._m = M
        super(SimpleSizeFunction,self).__init__(cl,points)
        
    def _add_ap(self, ap):
        if self._m is not None and ap.y > self._m:
            raise ValueError("Cannot add a cornerpoint greater than the maximum of measuring function %s>%s" % 
                             (ap.y, self._m))
        super(SimpleSizeFunction,self)._add_ap(ap)
        
    @property
    def maximum(self):
        return self._m

    def __eq__(self, other):
        if not isinstance(other, SimpleSizeFunction):
            if self._m is None:
                return super(SimpleSizeFunction,self).__eq__(other)
            return False
        return self._m == other._m and super(SimpleSizeFunction,self).__eq__(other)

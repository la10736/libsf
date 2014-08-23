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

    def copy(self):
        return SimpleSizeFunction(self._cl, self._m, self._points)

def check_abstract(f):
    def new_f(self, *args, **kwags):
        if self.ssf_type is None:
            raise NotImplementedError()
        return f(self, *args, **kwags)
    new_f.__name__ = f.__name__
    return new_f

class _AbstractSizeFunction(object):
    
    ssf_type = None
    
    def __init__(self):
        self._ssfs = []
    
    @check_abstract
    def new_ssf(self, *args, **kwargs):
        """Create and add new Simple Size Function.
        """
        ssf = self.ssf_type(*args, **kwargs)
        self._add(ssf)
        return ssf
    
    def _add(self, ssf):
        self._ssfs.append(ssf)
    
    @check_abstract
    def __eq__(self, other):
        if not isinstance(other, _AbstractSizeFunction):
            return False
        m = other._ssfs[:]
        for ssf in self._ssfs:
            if ssf in m:
                m.remove(ssf)
            else:
                return False
        return not m
    
    @check_abstract
    def add(self, ssf):
        """Add a copy of Simple Size Function ssf
        @param ssf: The simple size function to add
        @raise ValueError: if ssf is not the correct type
        @return: the new ssf
        """
        if ssf.__class__ != self.ssf_type:
            raise ValueError("You can just add simple size function of type %s"%
                             self.ssf_type.__class__.__name__)
        ret = ssf.copy()
        self._add(ret)
        return ret

    def get_ssfs(self):
        return [ssf.copy() for ssf in self._ssfs]
    
    @property
    def ssfs(self):
        return self.get_ssfs()
    
    def copy(self):
        ret = self.__class__()
        for ssf in self._ssfs:
            ret.add(ssf)
        return ret
    
    def dump(self, f):
        pos = 0
        for ssf in self.ssfs:
            f.write("l %d %f"%(pos,ssf.cornerline))
            if isinstance(ssf, SimpleSizeFunction):
                f.write(" %f"%ssf.maximum)
            f.write("\n")
            pos += 1
            for p in ssf.points:
                f.write("p %d %f %f\n"%(pos,p.x,p.y))
                pos += 1
            
            

class SizeFunctionOld(_AbstractSizeFunction):
    """The size function object old legacy implementation.
    It is a list of Simple Size Functions that don't care 
    about the maximum of measuring function.
    """
    ssf_type = SimpleSizeFunctionOld

class SizeFunction(_AbstractSizeFunction):
    """The size function object. It is a list of Simple Size 
    Functions with the maximum of measuring function.
    """
    ssf_type = SimpleSizeFunction

def readsf(f, forceold=False):
    """Read a Size Function from file. It reads a format like the output
    of the dump function of SizeFunction object. The empty lines and 
    the lines that starts by # will be ignored.
    @param f: it could be a open file (implenets readline) or a path 
    @return a size function 
    """
    try:
        l = f.readline()
    except AttributeError:
        """Try to use it as path"""
        f = file(str(f))
        l = f.readline()
    sf = SizeFunctionOld() if forceold else SizeFunction()
    ssf = None
    i=1
    pos=0
    while l:
        l = l.strip()
        if l and not l.startswith("#"):
            ll = l.split(" ")
            if ll[0]=='l':
                if len(ll)<3:
                    raise ValueError("line %d : wrong syntax must be 'l <n> <min> [max]'"%i)
                p = int(ll[1])
                if p != pos :
                    raise ValueError("line %d : wrong pos %d!=%d"%(i,p,pos))
                pos += 1
                M = None
                if len (ll)>3:
                    M = float(ll[3])
                ssf = sf.new_ssf(float(ll[2]),M)
            elif ll[0]=='p':
                if len(ll)<4:
                    raise ValueError("line %d : wrong syntax must be 'p <n> <x> <y>' "%i)
                if ssf is None:
                    raise ValueError("line %d : found a point without any line before"%i)
                p = int(ll[1])
                if p != pos :
                    raise ValueError("line %d : wrong pos %d!=%d"%(i,p,pos))
                pos += 1
                ssf.add_point(float(ll[2]),float(ll[3]))
            else:
                raise ValueError("line %d : cannot understand '%s' "%(i,l))
        l = f.readline()
        i += 1
    return sf
    
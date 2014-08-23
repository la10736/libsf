'''
Created on 14/ago/2014

Example program that explain how to use the sf library in 
the basic way. The script read a size graph from file a 
measuring function and write the size function
@author: michele
'''
from sf import SizeGraph, H0Tree
import sys

_pname=None

def _read_and_compute(fg,fms,fout):
    if fms is None:
        ms = None
    else:
        ms = []
        l=fms.readline()
        while l:
            ms.append(float(l))
            l=fms.readline()
    g = SizeGraph.readsg(fg, ms)
    h = H0Tree.compute_H0Tree(g)
    sf = h.get_sf()
    sf.dump(fout)

def usage(er):
    print "Use %s <graph> [out sf] [ms]"%(_pname)
    sys.exit(er)

def main(argv):
    if len(argv)<1:
        usage(-1)
    if argv[0] in ["-h","-?","--help"]:
        usage(0)
    fg = argv[0]
    print "Graph to compute %s"%argv[0]
    fms = None
    fout = sys.stdout
    if len(argv)>1:
        fout = file(argv[1], "w")
        print "Writing output to %s"%argv[1]
    if len(argv)>2:
        fms = file(argv[2], "r")
        print "Measuring function %s"%argv[2]
        
    _read_and_compute(fg, fms, fout)
    

if __name__ == '__main__':
    _pname = sys.argv[0]
    main(sys.argv[1:])

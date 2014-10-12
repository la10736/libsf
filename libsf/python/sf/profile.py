'''
Created on 23/ago/2014

@author: michele
'''
import os
from sf import SizeGraph, H0Tree
import logging
import cProfile
import sys
import pstats

logging.getLogger().setLevel(logging.DEBUG)

base_path = os.path.join('..', '..', 'tests')
traindir = os.path.join(base_path, 'train')
graphs_ext = '.size'
ms_ext = '-Filtfunc.f'
sf_dir = os.path.join(base_path, 'out')
sf_ext = '.sf'
outdir = 'out_train'
N = 1
SF_FACTOR = 1000
H0_FACTOR = 50


def _get_graph(f):
    b = os.path.basename(f).rsplit('.')[0]
    f = os.path.join(traindir, f)
    fms = file(os.path.join(traindir, b + ms_ext))
    ms = []
    l = fms.readline()
    while l:
        ms.append(float(l))
        l = fms.readline()
    return SizeGraph.readsg(f, ms)

if __name__ == '__main__':
    files = [f for f in os.listdir(traindir) if f.endswith(graphs_ext)]
    files.sort()
    files = [f for i, f in enumerate(files) if N is None or N > i]
    print "STARTING"
    print "LOADING GRAPHS"
    elements = [_get_graph(f) for f in files]
    print "GRAPHS:"+"\n"+"\n".join(files)
    
    i = 0
    N = len(elements)
    print "="*20 + "PROFILING H0 COMPUTATION [*%d]" % H0_FACTOR + "="*20
    pr = cProfile.Profile()
    sortby = 'time'
    pr.enable()
    for i in xrange(H0_FACTOR):
        h0s = [H0Tree.compute_H0Tree(g) for g in elements]
    pr.disable()
    pstats.Stats(pr, stream=sys.stdout).sort_stats(sortby).print_stats()
    print "#"*80
    print "="*20 + "PROFILING SF COMPUTATION [*%d]" % SF_FACTOR + "="*20
    pr = cProfile.Profile()
    pr.enable()
    for i in xrange(SF_FACTOR):
        sfs = [h.get_sf() for h in h0s]
    pr.disable()
    pstats.Stats(pr, stream=sys.stdout).sort_stats(sortby).print_stats()
    print "\n".join(["#"*80]*2)
    print "="*20 + "DONE" + "="*20
    print "\n".join(["#"*80]*2)

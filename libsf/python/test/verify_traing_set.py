'''
Created on 23/ago/2014

compute all size function for the graphs in traindir (the files in the form
'<name>.size') where the measuring function is taken from the
file with the same name plus ms_ext (i.e. '<name>-Filtfunc.f').
If the file '<name>.sf' in the sf_dir exist it will check that the
size function is the same. If outdir is not None it will save the result in 
outdir with the name '<name>.sf'

@author: michele
'''

import os
from sf import SizeGraph, H0Tree, SizeFunction
import logging

logging.getLogger().setLevel(logging.DEBUG)

base_path = os.path.join('..','..','tests')
traindir = os.path.join(base_path,'train')
graphs_ext = '.size'
ms_ext = '-Filtfunc.f'
sf_dir = os.path.join(base_path,'out')
sf_ext = '.sf'
outdir = 'out_train'

def _get_graph(fg,fms):
    if fms is None:
        ms = None
    else:
        ms = []
        l=fms.readline()
        while l:
            ms.append(float(l))
            l=fms.readline()
    return SizeGraph.readsg(fg, ms)

if __name__ == '__main__':
    try:
        if outdir is not None:
            os.makedirs(outdir)
    except:
        pass
    elements = [f for f in os.listdir(traindir) if f.endswith(graphs_ext)]
    i = 0
    N = len(elements)
    for f in elements:
        i += 1
        logging.info("========= [%d/%d] ========="%(i,N))
        b = os.path.basename(f).rsplit('.')[0]
        d = traindir
        f = os.path.join(d,f)
        ms = os.path.join(d,b + ms_ext)
        logging.info("Read graph from %s [ms = %s] "%(f,ms))
        g = _get_graph(f, file(ms))
        logging.info("..... Computing H0Tree")
        h = H0Tree.compute_H0Tree(g)
        logging.info("..... Computing SF")
        sf = h.get_sf()
        logging.info("Done")
        if outdir is not None:
            out = os.path.join(outdir , b + sf_ext)
            logging.info("Save the sf to %s"%out)
            sf.dump(file(out,'w'))
        chk_f = os.path.join(outdir,b + sf_ext)
        sf_chk= None
        try:
            sf_chk = SizeFunction.readsf(chk_f)
        except IOError:
            logging.warning("Cannot find %s for checking sf"%chk_f)
        else:
            if sf_chk == sf:
                logging.info("OK:  The function are the SAME!!!!!!")
            else:
                logging.warning("KO:  Something was going wrong !!!!!!")
            

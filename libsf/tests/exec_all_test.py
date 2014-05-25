
"""
exec_all_test.py
 Created on: 10/apr/2014
     Author: michele
"""


#!/usr/bin/env python
import os
import sys
import logging
import shutil

logging.getLogger().setLevel(logging.DEBUG)

traindir = 'train'
outdir = 'out'
ex = "../exampleProgram/exampleProgram "

if __name__ == "__main__":
    try:
        os.makedirs(outdir)
    except:
        pass
    for f in os.listdir(traindir):
        if f.endswith(".size"):
            b = os.path.basename(f).rsplit('.')[0]
            d = traindir
            f = os.path.join(d,f)
            ms = os.path.join(d,b + '-Filtfunc.f')
            out = os.path.join(outdir , b + '.sf')
            cmd = ' '.join([ex,f,ms,out])
            logging.info("EXEC "+cmd)
            os.system(' '.join([ex,f,ms,out]))

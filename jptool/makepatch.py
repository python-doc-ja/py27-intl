#!/usr/bin/env python

import difflib
import os
import os.path as path
from shutil import copyfile

join = path.join

def makepatch(left, right, dest):
    print left, right, dest
    for root,dirs,files in os.walk(right):
        if ".svn" in root: continue
        assert root.startswith(right)
        rel_root = root[len(right)+1:]
        dirpath = join(dest, rel_root)
        if not path.exists(dirpath):
            print "mkdir %s" % dirpath
            os.mkdir(dirpath)
        for f in files:
            lpath = join(left, rel_root, f)
            rpath = join(right, rel_root, f)
            dpath = join(dest, rel_root, f)

            if path.exists(lpath):
                cmd = """diff -U 12 '%s' '%s' > '%s.diff'""" % (lpath, rpath, dpath)
                print cmd
                os.system(cmd)
            else:
                print "new: %s" % rpath
                copyfile(rpath, dpath)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print "makepatch.py fromdir todir patchdir"
        sys.exit(1)
    makepatch(*sys.argv[1:])


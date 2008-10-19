import sys, os.path, codecs

def converttosjis(arg, dirname, names):

    for name in names:
        root, ext = os.path.splitext(name)
        if ext in ['.html', '.hhc', '.hhk', '.hhp', '.txt']:
            fpath = os.path.join(dirname, name)
            infile = codecs.open(fpath, 'rb', 'euc-jp', 'replace')
            data = infile.read()
            infile.close()
            outfile = codecs.open(fpath, 'wb', 'shift_jis', 'xmlcharrefreplace')
            outfile.write(data.replace("charset=EUC-JP", "charset=shift_jis"))
            outfile.close()
            print "processed %s/%s" %(dirname, name)


if __name__=="__main__":
    dir = sys.argv[1]
    os.path.walk(dir, converttosjis, None)

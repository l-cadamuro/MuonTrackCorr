import ROOT

def parse_input_filelist (fileName) :
    filelist = []
    with open (fileName) as fIn:
        for line in fIn:
            line = (line.split("#")[0]).strip()
            if line:
                filelist.append(line)
    return filelist

def load_from_filelist (chain, fileName, maxFiles=-1):
    flist = parse_input_filelist(fileName)

    if maxFiles > -1 and maxFiles < len(flist):
        flist = flist[:maxFiles]
        print "... plotUtils: restricting to the first", len(flist), 'files'

    print "... plotUtils: loading", len(flist), "files"
    for f in flist:
        chain.Add(f)

import ROOT

def parseInputFileList (fileName) :
    filelist = []
    with open (fileName) as fIn:
        for line in fIn:
            line = (line.split("#")[0]).strip()
            if line:
                filelist.append(line)
    return filelist

def is_bad(fname):
    fIn = ROOT.TFile.Open(fname)

    bad = False
    if not fIn: bad = True
    elif (fIn.IsZombie()): bad = True
    elif (fIn.TestBit(ROOT.TFile.kRecovered)): bad = True

    if fIn: fIn.Close()

    return bad


#########################################################################################

# filelistname = 'filelist/testlist.txt'
filelistname = 'filelist/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts.txt'
prepend_to_fname = 'root://cmseos.fnal.gov/'

# filelist = parseInputFileList('filelist/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts.txt')
filelist = parseInputFileList(filelistname)
print "... checking", len(filelist), 'files'

goodfiles = []
badfiles = []

for idx, fname in enumerate(filelist):
    if idx % 100 == 0:
        print idx , '/', len(filelist)
    bad = is_bad(prepend_to_fname + fname)
    if bad: badfiles.append(fname)
    else: goodfiles.append(fname)

print 'Good files {ngood}/{ntot} = {frgood:.2f}%: '.format(ngood=len(goodfiles), ntot=len(filelist), frgood=100.*len(goodfiles)/len(filelist))
print 'Bad  files {nbad}/{ntot} = {frbad:.2f}%: '.format(nbad=len(badfiles), ntot=len(filelist), frbad=100.*len(badfiles)/len(filelist))

flistgoodname = filelistname.replace('.txt', '_good.txt')
flistbadname  = filelistname.replace('.txt', '_bad.txt')

print "... dumping list collection to"
print flistgoodname
print flistbadname

flistgood = open(flistgoodname, 'w')
for f in goodfiles:
    flistgood.write(f+'\n')
flistgood.close()

flistbad = open(flistbadname, 'w')
for f in badfiles:
    flistbad.write(f+'\n')
flistbad.close()

# f = '/eos/uscms/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_1647.root'
# f = '/eos/uscms/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_1868.root'
# fIn = ROOT.TFile.Open(f)

# print fIn

# bad = False
# if (fIn.IsZombie()): bad = True
# if (fIn.TestBit(ROOT.TFile.kRecovered)): bad = True

# print bad

# print is_bad(f)
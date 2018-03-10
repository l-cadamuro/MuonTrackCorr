import os
import sys
import argparse
import datetime

############################################################################################################

# def parseInputFileList (fileName) :
#     filelist = []
#     with open (fileName) as fIn:
#         for line in fIn:
#             line = (line.split("#")[0]).strip()
#             if line:
#                 filelist.append(line)
#     return filelist

def parseInputFileList (fileName) :
    filelist = []
    with open (fileName) as fIn:
        for line in fIn:
            line = (line.split("#")[0]).strip()
            if line:
                filelist.append(line)
    return filelist


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def splitInBlocks (l, n):
    """split the list l in n blocks of equal size"""
    k = len(l) / n
    r = len(l) % n

    i = 0
    blocks = []
    while i < len(l):
        if len(blocks)<r:
            blocks.append(l[i:i+k+1])
            i += k+1
        else:
            blocks.append(l[i:i+k])
            i += k

    return blocks

def writeln(f, line):
    f.write(line + '\n')

############################################################################################################

##############################
##### CMD line options
parser = argparse.ArgumentParser(description='Command line parser of plotting options')

parser.add_argument('--filelist',       dest='filelist',   help='input file list', default=None)
parser.add_argument('--tag',            dest='tag',        help='process tag',     default=None)
parser.add_argument('--njobs',          dest='njobs',      help='number of jobs',  type=int, default=20)
parser.add_argument('--no-tar',         dest='tar',        help='do not tar the CMSSW folder',       action='store_false', default=True)
parser.add_argument('--no-xrdcp-tar',   dest='xrdcptar',   help='do not xrdcp the tar to EOS',       action='store_false', default=True)
parser.add_argument('--no-xrdcp-flist', dest='xrdcpflist', help='do not xrdcp the filelist to EOS',  action='store_false', default=True)
parser.add_argument('--dry-run',        dest='dryrun',     help='dry run without launching',         action='store_true',  default=False)
parser.add_argument('--verbose',        dest='verbose',    help='set verbose mode',                  action='store_true',  default=False)

args = parser.parse_args()

##############################
##### Prepare CMSSW space vars

cmssw_base    = os.environ['CMSSW_BASE']
cmssw_version = os.environ['CMSSW_VERSION']
scram_arch    = os.environ['SCRAM_ARCH']
print '** INFO: CMSSW located in: ', cmssw_base

tarName      = '%s_tar.tgz' % cmssw_version
cmsswWorkDir = os.path.abspath(os.path.join(cmssw_base, '..'))
tarLFN       = cmsswWorkDir + '/' + tarName

# cmsRunInto   = 'L1TMuonSimulations/Analyzers/testLuca' # where to run cmsRun, relative from CMSSW/src
# cmsRunExec   = 'ntuplizer.py' # python to run

cmsRunInto   = 'MuonTrackCorr/MuonTrackCorr/test' # where to run cmsRun, relative from CMSSW/src
cmsRunExec   = 'analyze_eras_muonly.py' # python to run


##############################
##### Tar the folder if needed

if args.tar:
    # tar -zcvf <Tar output name> <folder to tar>
    # note -v is verbose option
    # excludePath        = '{0}/src/L1TMuonSimulations/Analyzers/batch'.format(cmssw_version)
    # excludePath2       = '{0}/src/L1TMuonSimulations/Studies'.format(cmssw_version)
    
    toExclude = [
        '{0}/src/.git'.format(cmssw_version),
        '{0}/src/MuonTrackCorr/MuonTrackCorr/batch'.format(cmssw_version),
        '{0}/src/MuonTrackCorr/MuonTrackCorr/test/*.root'.format(cmssw_version),
     ]

    # command = 'tar --exclude="{0}" --exclude="{1}" -zcf {2} -C {3} {4}'.format(excludePath, excludePath2, tarLFN, cmsswWorkDir, cmssw_version)
    command = 'tar'
    for te in toExclude:
        command += ' --exclude="{0}"'.format(te)
    command += ' -zcf {0} -C {1} {2}'.format(tarLFN, cmsswWorkDir, cmssw_version)

    # '--exclude="{0}" --exclude="{1}" -zcf {2} -C {3} {4}'.format(excludePath, excludePath2, tarLFN, cmsswWorkDir, cmssw_version)
    print '** INFO: Going to tar CMSSW folder into', tarName
    if args.verbose: print "** INFO: executing:", command
    os.system(command)
    print '** INFO: tar finished and saved in:', tarLFN
else:
    print '** INFO: Not going to tar CMSSW folder, using', tarLFN


##############################
##### Prepare file lists

if not args.filelist:
    print "** ERROR: no file list specified, exiting"
    sys.exit()

xroootdServ   = 'root://cmsxrootd.fnal.gov/'

inputfiles = parseInputFileList (args.filelist)    ## parse input list
inputfiles = [xroootdServ + s for s in inputfiles] ## complete with lfn
njobs      = args.njobs if args.njobs <= len (inputfiles) else len (inputfiles)
fileblocks = splitInBlocks (inputfiles, njobs)
if njobs != len(fileblocks):
    print "** ERROR: length of file lists and njobs do not match, something went wrong"
    sys.exit()

# print fileblocks

##############################
#### Prepare the folder with the filelists and scripts

tag = args.tag if args.tag else datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
jobsDir = 'jobs_' + tag
print "** INFO: preparing jobs in:", jobsDir
os.system('mkdir ' + jobsDir)

baseEOSout            = 'root://cmseos.fnal.gov//store/user/lcadamur/L1MuTrks_ntuples/%s' % tag
tarEOSdestLFN         = 'root://cmseos.fnal.gov//store/user/lcadamur/CMSSW_tar/'+ tarName
# filelistEOSdestLFNdir = 'root://cmseos.fnal.gov//store/user/lcadamur/CMSSW_tar/'+ tarName

outListNameBareProto   = 'filelist_{0}.txt'
outScriptNameBareProto = 'job_{0}.sh'
outListNameProto       = (jobsDir + '/' + outListNameBareProto)
outScriptNameProto     = (jobsDir + '/' + outScriptNameBareProto)
EOSfilelistBase        = baseEOSout + '/filelist'
EOSfilelistProto       = EOSfilelistBase + '/' + outListNameBareProto

## filelist
for n in range(0, njobs):
    outListName = outListNameProto.format(n)
    jobfilelist = open(outListName, 'w')
    for f in fileblocks[n]: jobfilelist.write(f+"\n")
    jobfilelist.close()

# script
for n in range(0, njobs):
    outListName     = outListNameProto.format(n)
    outListNameBare = outListNameBareProto.format(n)
    outputFileName = 'ntuple_%i.root' % n
    outputEOSName  = '%s/output/%s' % (baseEOSout, outputFileName)
    outScriptName  = outScriptNameProto.format(n)
    outScript      = open(outScriptName, 'w')
    writeln(outScript, '#!/bin/bash')
    writeln(outScript, '{') ## start of redirection..., keep stderr and stdout in a single file, it's easier
    writeln(outScript, 'echo "... starting job on " `date` #Date/time of start of job')
    writeln(outScript, 'echo "... running on: `uname -a`" #Condor job is running on this node')
    writeln(outScript, 'echo "... system software: `cat /etc/redhat-release`" #Operating System on that node')
    writeln(outScript, 'source /cvmfs/cms.cern.ch/cmsset_default.sh')
    writeln(outScript, 'echo "... retrieving CMSSW tarball"')
    writeln(outScript, 'xrdcp -f -s %s .' % tarEOSdestLFN) ## force overwrite CMSSW tar
    writeln(outScript, 'echo "... uncompressing CMSSW tarball"')
    writeln(outScript, 'tar -xzf %s' % tarName)
    writeln(outScript, 'rm %s' % tarName)
    writeln(outScript, 'export SCRAM_ARCH=%s' % scram_arch)
    writeln(outScript, 'cd %s/src/' % cmssw_version)
    writeln(outScript, 'scramv1 b ProjectRename')
    writeln(outScript, 'eval `scramv1 runtime -sh`')
    writeln(outScript, 'cd %s' % cmsRunInto)
    writeln(outScript, 'echo "... retrieving filelist"')
    writeln(outScript, 'xrdcp -f -s %s .' % EOSfilelistProto.format(n)) ## force overwrite file list
    # writeln(outScript, 'echo "... listing files"')
    # writeln(outScript, 'ls -altrh')
    # writeln(outScript, 'echo "Arguments passed to this script are: for 1: $1, and for 2: $2"')
    writeln(outScript, 'echo "... starting CMSSW run"')
    writeln(outScript, 'cmsRun %s inputFiles_load=%s outputFile=%s' % (cmsRunExec, outListNameBare, outputFileName))
    writeln(outScript, 'echo "... cmsRun finished with status $?"')
    writeln(outScript, 'echo "... copying output file %s to EOS in %s"' % (outputFileName, outputEOSName))
    writeln(outScript, 'xrdcp -s %s %s' % (outputFileName, outputEOSName)) ## no not force overwrite output in destination
    writeln(outScript, 'echo "... copy done with status $?"')
    # writeln(outScript, 'remove the input and output files if you dont want it automatically transferred when the job ends')
    # writeln(outScript, 'rm nameOfOutputFile.root')
    # writeln(outScript, 'rm Filename1.root')
    # writeln(outScript, 'rm Filename2.root')
    writeln(outScript, 'cd ${_CONDOR_SCRATCH_DIR}')
    writeln(outScript, 'rm -rf %s' % cmssw_version)
    writeln(outScript, 'echo "... job finished with status $?"')
    writeln(outScript, 'echo "... finished job on " `date`')
    writeln(outScript, 'echo "... exiting script"')
    writeln(outScript, '} 2>&1') ## end of redirection
    outScript.close()

##############################
#### Ship the CMSSW tarball and submit the jobs

if args.xrdcptar:
    print "** INFO: copying CMSSW tarball to:", tarEOSdestLFN
    command = 'xrdcp -f -s %s %s' % (tarLFN, tarEOSdestLFN)
    os.system(command)
    if args.verbose: print "** INFO: executing:", command
else:
    print "** INFO: not going to xrdcp the CMSSW tarball to EOS, assuming it exists at", tarEOSdestLFN

if args.xrdcpflist:    
    print "** INFO: copying input filelists to:", EOSfilelistProto.format('*')
    command = 'eos root://cmseos.fnal.gov mkdir -p %s' % EOSfilelistBase.replace('root://cmseos.fnal.gov/', '/eos/uscms')
     # there is an incompatibility of EOS commands with cmsenv, so this below encapsulated the call of the command in a new shell
    command = 'env -i PATH="$(getconf PATH)" HOME="$HOME" USER="$USER" SHELL="$SHELL" "$SHELL" -lc "%s"' % command
    if args.verbose: print "** INFO: executing:", command
    os.system(command)    
    command = 'xrdcp -f -s %s %s' % (outListNameProto.format('*'), EOSfilelistBase)
    if args.verbose: print "** INFO: executing:", command
    os.system(command)

else:
    print "** INFO: not going to xrdcp the filelistsi to EOS, they exists at", EOSfilelistProto.format('*')


## set directory to job directory, so that logs will be saved there
os.chdir(jobsDir)
for n in range(0, njobs):
    command = "../t3submit %s" % outScriptNameBareProto.format(n)
    if not args.dryrun:
        if args.verbose: print "** INFO: submit job with command", command
        os.system(command)
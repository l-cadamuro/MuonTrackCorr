SUFFIX_TAG="7Mar19_CMSSW_SvenPRTPAlgo_runTPalgo"

echo "... preparing the submission (tar and copy of CMSSW)"
python submitOnTier3.py --xrdcp-tar-only --tar-suffix ${SUFFIX_TAG}
echo ".. done, launching"

### single mu eff
python submitOnTier3.py --filelist filelist/SingleMu_FlatPt-2to100_L1TnoPU.txt          --tag SingleMu_FlatPt-2to100_L1TnoPU_${SUFFIX_TAG}     --njobs 50 --no-tar --no-xrdcp-tar --tar-suffix ${SUFFIX_TAG}
#python submitOnTier3.py --filelist filelist/SingleMu_FlatPt-2to100_L1TPU140.txt         --tag SingleMu_FlatPt-2to100_L1TPU140_${SUFFIX_TAG}    --njobs 50 --no-tar --no-xrdcp-tar --tar-suffix ${SUFFIX_TAG}
python submitOnTier3.py --filelist filelist/SingleMu_FlatPt-2to100_L1TPU200.txt         --tag SingleMu_FlatPt-2to100_L1TPU200_${SUFFIX_TAG}    --njobs 50 --no-tar --no-xrdcp-tar --tar-suffix ${SUFFIX_TAG}

### rates
#python submitOnTier3.py --filelist filelist/SingleNeutrino_L1TnoPU.txt          --tag SingleNeutrino_L1TnoPU_${SUFFIX_TAG}     --njobs 200 --no-tar --no-xrdcp-tar --tar-suffix ${SUFFIX_TAG}
python submitOnTier3.py --filelist filelist/SingleNeutrino_L1TPU140.txt         --tag SingleNeutrino_L1TPU140_${SUFFIX_TAG}    --njobs 200 --no-tar --no-xrdcp-tar --tar-suffix ${SUFFIX_TAG}
python submitOnTier3.py --filelist filelist/SingleNeutrino_L1TPU200.txt         --tag SingleNeutrino_L1TPU200_${SUFFIX_TAG}    --njobs 200 --no-tar --no-xrdcp-tar --tar-suffix ${SUFFIX_TAG}

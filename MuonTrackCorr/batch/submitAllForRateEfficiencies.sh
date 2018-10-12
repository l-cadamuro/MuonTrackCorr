SUFFIX_TAG="12Ott_DWcorr_CMSSW"

echo "... preparing the submission (tar and copy of CMSSW)"
python submitOnTier3.py --xrdcp-tar-only
echo ".. done, launching"

### single mu eff
python submitOnTier3.py --filelist filelist/SingleMu_FlatPt-2to100_L1TnoPU.txt          --tag SingleMu_FlatPt-2to100_L1TnoPU_${SUFFIX_TAG}     --njobs 50 --no-tar --no-xrdcp-tar
python submitOnTier3.py --filelist filelist/SingleMu_FlatPt-2to100_L1TPU140.txt         --tag SingleMu_FlatPt-2to100_L1TPU140_${SUFFIX_TAG}    --njobs 50 --no-tar --no-xrdcp-tar
python submitOnTier3.py --filelist filelist/SingleMu_FlatPt-2to100_L1TPU200.txt         --tag SingleMu_FlatPt-2to100_L1TPU200_${SUFFIX_TAG}    --njobs 50 --no-tar --no-xrdcp-tar

### rates
python submitOnTier3.py --filelist filelist/SingleNeutrino_L1TnoPU.txt          --tag SingleNeutrino_L1TnoPU_${SUFFIX_TAG}     --njobs 200 --no-tar --no-xrdcp-tar
python submitOnTier3.py --filelist filelist/SingleNeutrino_L1TPU140.txt         --tag SingleNeutrino_L1TPU140_${SUFFIX_TAG}    --njobs 200 --no-tar --no-xrdcp-tar
python submitOnTier3.py --filelist filelist/SingleNeutrino_L1TPU200.txt         --tag SingleNeutrino_L1TPU200_${SUFFIX_TAG}    --njobs 200 --no-tar --no-xrdcp-tar
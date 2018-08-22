SUFFIX_TAG="3Mag_TkMu_moreinfotrk"

echo "... preparing the submission (tar and copy of CMSSW)"
python submitOnTier3.py --xrdcp-tar-only
echo ".. done, launching"

python submitOnTier3.py --filelist filelist/ZToMuMu_RelVal_PU0.txt     --tag ZToMuMu_RelVal_PU0_${SUFFIX_TAG}   --njobs 50 --no-tar --no-xrdcp-tar
python submitOnTier3.py --filelist filelist/ZToMuMu_RelVal_PU200.txt   --tag ZToMuMu_RelVal_PU200_${SUFFIX_TAG} --njobs 50 --no-tar --no-xrdcp-tar
SUFFIX_TAG="18Apr_hitinfo_fix"

echo "... preparing the submission (tar and copy of CMSSW)"
python submitOnTier3.py --xrdcp-tar-only
echo ".. done, launching"

python submitOnTier3.py --filelist filelist/MuMu_2to500_flatPt_0PU_8Mar2018.txt         --tag MuMu_flatPt_0PU_${SUFFIX_TAG}    --njobs 50 --no-tar --no-xrdcp-tar
python submitOnTier3.py --filelist filelist/MuMu_2to2000_flatOneOverPt_0PU_8Mar2018.txt --tag MuMu_OneOverPt_0PU_${SUFFIX_TAG} --njobs 50 --no-tar --no-xrdcp-tar
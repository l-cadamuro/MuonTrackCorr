SUFFIX_TAG="6Sett_TDR_MC_EMTFmode_FixCppFlag"

echo "... preparing the submission (tar and copy of CMSSW)"
python submitOnTier3.py --xrdcp-tar-only  --tar-suffix $SUFFIX_TAG
echo ".. done, launching"

#python submitOnTier3.py --filelist filelist/MuMu_2to500_flatPt_0PU_8Mar2018.txt         --tag MuMu_flatPt_0PU_${SUFFIX_TAG}    --njobs 50 --no-tar --no-xrdcp-tar
#python submitOnTier3.py --filelist filelist/MuMu_2to2000_flatOneOverPt_0PU_8Mar2018.txt --tag MuMu_OneOverPt_0PU_${SUFFIX_TAG} --njobs 50 --no-tar --no-xrdcp-tar

python submitOnTier3.py --filelist filelist/Mu_FlatPt2to100-pythia8-gun_TDR_PU0.txt         --tag MuMu_flatPt_0PU_${SUFFIX_TAG}    --njobs 50 --no-tar --no-xrdcp-tar --tar-suffix $SUFFIX_TAG

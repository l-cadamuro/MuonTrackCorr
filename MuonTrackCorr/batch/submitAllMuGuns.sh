SUFFIX_TAG="21Ott_TDR_MC_TkMuStubv3"

echo "... preparing the submission (tar and copy of CMSSW)"
python submitOnTier3.py --xrdcp-tar-only  --tar-suffix $SUFFIX_TAG
echo ".. done, launching"

#python submitOnTier3.py --filelist filelist/MuMu_2to500_flatPt_0PU_8Mar2018.txt         --tag MuMu_flatPt_0PU_${SUFFIX_TAG}    --njobs 50 --no-tar --no-xrdcp-tar
#python submitOnTier3.py --filelist filelist/MuMu_2to2000_flatOneOverPt_0PU_8Mar2018.txt --tag MuMu_OneOverPt_0PU_${SUFFIX_TAG} --njobs 50 --no-tar --no-xrdcp-tar

##### TDR MC samples

python submitOnTier3.py --filelist filelist/Mu_FlatPt2to100_gun_PU0_TDR_MC.txt        --tag MuMu_flatPt_0PU_${SUFFIX_TAG}      --njobs 50   --no-tar --no-xrdcp-tar --tar-suffix $SUFFIX_TAG
python submitOnTier3.py --filelist filelist/Mu_FlatPt2to100_gun_PU200_TDR_MC.txt      --tag MuMu_flatPt_200PU_${SUFFIX_TAG}    --njobs 150  --no-tar --no-xrdcp-tar --tar-suffix $SUFFIX_TAG
python submitOnTier3.py --filelist filelist/Mu_FlatPt2to100_gun_PU300_TDR_MC.txt      --tag MuMu_flatPt_300PU_${SUFFIX_TAG}    --njobs 300  --no-tar --no-xrdcp-tar --tar-suffix $SUFFIX_TAG

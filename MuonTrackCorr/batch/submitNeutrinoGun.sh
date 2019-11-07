SUFFIX_TAG="21Ott_TDR_MC_TkMuStubv3"

# echo "... preparing the submission (tar and copy of CMSSW)"
# python submitOnTier3.py --xrdcp-tar-only --tar-suffix $SUFFIX_TAG
# echo ".. done, launching"

python submitOnTier3.py --filelist filelist/ZeroBias_PU140_L1_TDR.txt         --tag NuGun_140PU_${SUFFIX_TAG}    --njobs 1500 --no-tar --no-xrdcp-tar --tar-suffix $SUFFIX_TAG
python submitOnTier3.py --filelist filelist/ZeroBias_PU200_L1_TDR.txt         --tag NuGun_200PU_${SUFFIX_TAG}    --njobs 1500 --no-tar --no-xrdcp-tar --tar-suffix $SUFFIX_TAG
python submitOnTier3.py --filelist filelist/ZeroBias_PU250_L1_TDR.txt         --tag NuGun_250PU_${SUFFIX_TAG}    --njobs 1500 --no-tar --no-xrdcp-tar --tar-suffix $SUFFIX_TAG
python submitOnTier3.py --filelist filelist/ZeroBias_PU300_L1_TDR.txt         --tag NuGun_300PU_${SUFFIX_TAG}    --njobs 1500 --no-tar --no-xrdcp-tar --tar-suffix $SUFFIX_TAG

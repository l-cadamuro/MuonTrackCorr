SUFFIX_TAG="8Giu_TkMu_moreinfotrk_allEvts"

echo "... preparing the submission (tar and copy of CMSSW)"
python submitOnTier3.py --xrdcp-tar-only
echo ".. done, launching"

python submitOnTier3.py --filelist filelist/SingleNeutrino_PU200.txt         --tag NuGun_200PU_${SUFFIX_TAG}    --njobs 200 --no-tar --no-xrdcp-tar

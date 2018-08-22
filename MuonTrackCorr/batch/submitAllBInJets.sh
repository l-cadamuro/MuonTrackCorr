SUFFIX_TAG="25Giu_TkMu_moreinfotrk"

echo "... preparing the submission (tar and copy of CMSSW)"
python submitOnTier3.py --xrdcp-tar-only
echo ".. done, launching"

python submitOnTier3.py --filelist filelist/BjetToMu_endcap_neg.txt         --tag BjetToMu_endcap_neg_0PU_${SUFFIX_TAG} --all-gen-mu   --njobs 50 --no-tar --no-xrdcp-tar
python submitOnTier3.py --filelist filelist/BjetToMu_endcap_pos_resub.txt   --tag BjetToMu_endcap_pos_0PU_${SUFFIX_TAG} --all-gen-mu   --njobs 50 --no-tar --no-xrdcp-tar
### extra production for more stats in the pos endcap
### python submitOnTier3.py --filelist filelist/BjetToMu_endcap_pos_resub2.txt   --tag BjetToMu_endcap_pos_0PU_${SUFFIX_TAG} --all-gen-mu   --njobs 50 --no-tar --no-xrdcp-tar

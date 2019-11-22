SUFFIX_TAG="20Nov2019_newMantraOvrlEndc_MTDTDR"

echo "... preparing the submission (tar and copy of CMSSW)"
python submitOnTier3.py --xrdcp-tar-only  --tar-suffix $SUFFIX_TAG
echo ".. done, launching"

# python submitOnTier3.py --filelist filelist/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts_good.txt     --tag Ds_Tau3Mu_PU0_${SUFFIX_TAG}                    --save-tau-3mu --all-gen-mu  --only-mu-from-tau  --njobs 50 --no-tar --no-xrdcp-tar
# ####
# python submitOnTier3.py --filelist filelist/TauTau_pm_To3muFlatPt1To10_6Apr2019_2p5MEvts.txt  --tag TauTau_pm_Tau3Mu_FlatPt1To10_PU0_${SUFFIX_TAG} --save-tau-3mu --all-gen-mu  --only-mu-from-tau  --njobs 25 --no-tar --no-xrdcp-tar
# python submitOnTier3.py --filelist filelist/TauTau_mp_To3muFlatPt1To10_6Apr2019_2p5MEvts.txt  --tag TauTau_mp_Tau3Mu_FlatPt1To10_PU0_${SUFFIX_TAG} --save-tau-3mu --all-gen-mu  --only-mu-from-tau  --njobs 25 --no-tar --no-xrdcp-tar
# ####
# python submitOnTier3.py --filelist filelist/TauTau_mp_To3muFlatPt10To20_15Apr2019_2p5MEvts.txt  --tag TauTau_mp_Tau3Mu_FlatPt10To20_PU0_${SUFFIX_TAG} --save-tau-3mu --all-gen-mu  --only-mu-from-tau  --njobs 25 --no-tar --no-xrdcp-tar

# python submitOnTier3.py --filelist filelist/TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU0.txt    --tag TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU0_${SUFFIX_TAG}   --save-tau-3mu --all-gen-mu  --only-mu-from-tau  --njobs 25 --no-tar --no-xrdcp-tar  --tar-suffix $SUFFIX_TAG
# python submitOnTier3.py --filelist filelist/TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU140.txt  --tag TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU140_${SUFFIX_TAG} --save-tau-3mu --all-gen-mu  --only-mu-from-tau  --njobs 25 --no-tar --no-xrdcp-tar  --tar-suffix $SUFFIX_TAG
# python submitOnTier3.py --filelist filelist/TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU200.txt  --tag TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU200_${SUFFIX_TAG} --save-tau-3mu --all-gen-mu  --only-mu-from-tau  --njobs 200 --no-tar --no-xrdcp-tar  --tar-suffix $SUFFIX_TAG
###
python submitOnTier3.py --filelist filelist/Tau3Mu_RelVal.txt  --tag TauTo3Mu_RelVal_PU200_${SUFFIX_TAG} --save-tau-3mu --all-gen-mu  --only-mu-from-tau  --njobs 200 --no-tar --no-xrdcp-tar  --tar-suffix $SUFFIX_TAG --cmsRunCfg 'analyze_MTD_MC.py'
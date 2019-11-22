################################

# DEST_FLDR="/uscms/home/lcadamur/nobackup/MuonTrackCorr_analysis/CMSSW_10_6_1_patch2/src/MuonTrackCorr/MuonTrackCorr/analysis/filelist/TDR_MC_MantraOvrlEndc"

# python getTaskStatus.py --dir jobs_MuMu_flatPt_0PU_6Nov2019_newMantraOvrlEndc                          --flist ${DEST_FLDR}/MuMu_flatPt_PU0.txt
# python getTaskStatus.py --dir jobs_MuMu_flatPt_200PU_6Nov2019_newMantraOvrlEndc                        --flist ${DEST_FLDR}/MuMu_flatPt_PU200.txt
# python getTaskStatus.py --dir jobs_MuMu_flatPt_300PU_6Nov2019_newMantraOvrlEndc                        --flist ${DEST_FLDR}/MuMu_flatPt_PU300.txt
# ######
# # python getTaskStatus.py --dir jobs_TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU0_6Nov2019_newMantraOvrlEndc   --flist ${DEST_FLDR}/TauTo3Mu_PU0.txt
# python getTaskStatus.py --dir jobs_TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU140_6Nov2019_newMantraOvrlEndc --flist ${DEST_FLDR}/TauTo3Mu_PU140.txt
# python getTaskStatus.py --dir jobs_TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU200_6Nov2019_newMantraOvrlEndc --flist ${DEST_FLDR}/TauTo3Mu_PU200.txt
# ####
# python getTaskStatus.py --dir jobs_NuGun_140PU_6Nov2019_newMantraOvrlEndc                              --flist ${DEST_FLDR}/NuGun_140PU.txt
# python getTaskStatus.py --dir jobs_NuGun_200PU_6Nov2019_newMantraOvrlEndc                              --flist ${DEST_FLDR}/NuGun_200PU.txt
# python getTaskStatus.py --dir jobs_NuGun_250PU_6Nov2019_newMantraOvrlEndc                              --flist ${DEST_FLDR}/NuGun_250PU.txt
# python getTaskStatus.py --dir jobs_NuGun_300PU_6Nov2019_newMantraOvrlEndc                              --flist ${DEST_FLDR}/NuGun_300PU.txt

###### MTD TDR

DEST_FLDR="/uscms/home/lcadamur/nobackup/MuonTrackCorr_analysis/CMSSW_10_6_1_patch2/src/MuonTrackCorr/MuonTrackCorr/analysis/filelist/MTD_MC_Tau3Mu"

python getTaskStatus.py --dir jobs_TauTo3Mu_RelVal_PU200_20Nov2019_newMantraOvrlEndc_MTDTDR --flist ${DEST_FLDR}/TauTo3Mu_PU200.txt
####
python getTaskStatus.py --dir jobs_NuGun_140PU_20Nov2019_newMantraOvrlEndc_MTDTDR           --flist ${DEST_FLDR}/NuGun_140PU.txt
python getTaskStatus.py --dir jobs_NuGun_200PU_20Nov2019_newMantraOvrlEndc_MTDTDR           --flist ${DEST_FLDR}/NuGun_200PU.txt
python getTaskStatus.py --dir jobs_NuGun_250PU_20Nov2019_newMantraOvrlEndc_MTDTDR           --flist ${DEST_FLDR}/NuGun_250PU.txt
python getTaskStatus.py --dir jobs_NuGun_300PU_20Nov2019_newMantraOvrlEndc_MTDTDR           --flist ${DEST_FLDR}/NuGun_300PU.txt

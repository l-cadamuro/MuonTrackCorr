################################

DEST_FLDR="/uscms/home/lcadamur/nobackup/MuonTrackCorr_analysis/CMSSW_10_6_1_patch2/src/MuonTrackCorr/MuonTrackCorr/analysis/filelist/TDR_MC_TkMuStubv3"

python getTaskStatus.py --dir jobs_MuMu_flatPt_0PU_21Ott_TDR_MC_TkMuStubv3                          --flist ${DEST_FLDR}/MuMu_flatPt_PU0.txt
python getTaskStatus.py --dir jobs_MuMu_flatPt_200PU_21Ott_TDR_MC_TkMuStubv3                        --flist ${DEST_FLDR}/MuMu_flatPt_PU200.txt
python getTaskStatus.py --dir jobs_MuMu_flatPt_300PU_21Ott_TDR_MC_TkMuStubv3                        --flist ${DEST_FLDR}/MuMu_flatPt_PU300.txt
######
python getTaskStatus.py --dir jobs_TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU0_21Ott_TDR_MC_TkMuStubv3   --flist ${DEST_FLDR}/TauTo3Mu_PU0.txt
python getTaskStatus.py --dir jobs_TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU140_21Ott_TDR_MC_TkMuStubv3 --flist ${DEST_FLDR}/TauTo3Mu_PU140.txt
python getTaskStatus.py --dir jobs_TauTo3Mu_TuneCP5_14TeV-pythia8_TDR_PU200_21Ott_TDR_MC_TkMuStubv3 --flist ${DEST_FLDR}/TauTo3Mu_PU200.txt
####
python getTaskStatus.py --dir jobs_NuGun_140PU_21Ott_TDR_MC_TkMuStubv3                              --flist ${DEST_FLDR}/NuGun_140PU.txt
python getTaskStatus.py --dir jobs_NuGun_200PU_21Ott_TDR_MC_TkMuStubv3                              --flist ${DEST_FLDR}/NuGun_200PU.txt
python getTaskStatus.py --dir jobs_NuGun_250PU_21Ott_TDR_MC_TkMuStubv3                              --flist ${DEST_FLDR}/NuGun_250PU.txt
python getTaskStatus.py --dir jobs_NuGun_300PU_21Ott_TDR_MC_TkMuStubv3                              --flist ${DEST_FLDR}/NuGun_300PU.txt


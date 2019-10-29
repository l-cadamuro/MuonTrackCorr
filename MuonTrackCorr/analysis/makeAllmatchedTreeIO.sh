# ./makeMatchedTree_IO --input filelist/MuGun_flatPt_0PU_TDR_MC_EMTFmode_SvenTPFix_BarrOvrl.txt --output matchedTree_MuGun_PU0_BarrOvrl.root --all-eta-muons --dRmax 0.1
# ./makeMatchedTree_IO --input filelist/MuGun_flatPt_200PU_TDR_MC_EMTFmode_SvenTPFix_BarrOvrl.txt --output matchedTree_MuGun_PU200_BarrOvrl.root --all-eta-muons --dRmax 0.1

#### for the TDR plots
./makeMatchedTree_IO --input filelist/TDR_MC_TkMuStubv3/MuMu_flatPt_PU0.txt   --output matchedTree_MuGun_PU0_EMTFpp.root   --require-single-mu-in-endcap --dRmax 0.1
./makeMatchedTree_IO --input filelist/TDR_MC_TkMuStubv3/MuMu_flatPt_PU200.txt --output matchedTree_MuGun_PU200_EMTFpp.root --require-single-mu-in-endcap --dRmax 0.1
./makeMatchedTree_IO --input filelist/TDR_MC_TkMuStubv3/MuMu_flatPt_PU300.txt --output matchedTree_MuGun_PU300_EMTFpp.root --require-single-mu-in-endcap --dRmax 0.1
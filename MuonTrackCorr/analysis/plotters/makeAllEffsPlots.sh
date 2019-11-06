# for pl in MuMu_flatPt_0PU ZToMuMu_200PU; do
# # for pl in MuMu_flatPt_0PU; do
# # for pl in ZToMuMu_200PU; do
#     for q in 90 95 99; do
#         python make_eff_plots.py --in ../matched_tree_${pl}_fix_q${q}.root --out efficiencies/effs_${pl}_fix_q${q}.root
#     done
# done

# python make_eff_plots.py --in ../matched_tree_MuMu_flatPt_0PU_q99_relax0p5.root --out efficiencies/effs_MuMu_flatPt_0PU_q99_relax0p5.root
# python make_eff_plots.py --in ../matched_tree_ZToMuMu_200PU_q99_relax0p5.root   --out efficiencies/effs_ZToMuMu_200PU_q99_relax0p5.root

# python make_eff_plots.py --in ../matched_tree_SingleMu_PU200_DWcorr_CMSSWdefaultNoRelax_mults.root --out efficiencies/effs_SingleMu_PU200_DWcorr_CMSSWdefaultNoRelax_mults.root
# python make_eff_plots.py --in ../matched_tree_SingleMu_PU200_TPcorr_SvenPars_mults.root            --out efficiencies/effs_SingleMu_PU200_TPcorr_SvenPars_mults.root
# python make_eff_plots.py --in ../matched_tree_SingleMu_PU200_DWcorr_relax0p5At6GeV_mults.root      --out efficiencies/effs_SingleMu_PU200_DWcorr_relax0p5At6GeV_mults.root
# python make_eff_plots.py --in ../matched_tree_SingleMu_PU200_TPcorr_mults.root                     --out efficiencies/effs_SingleMu_PU200_TPcorr_mults.root

# python make_eff_plots.py --in ../matchedTree_MuGun_PU0_EMTFpp.root        --out efficiencies/effs_SingleMu_PU0_TDR_MC.root
# python make_eff_plots.py --in ../matchedTree_MuGun_PU200_EMTFpp.root      --out efficiencies/effs_SingleMu_PU200_TDR_MC.root
# python make_eff_plots.py --in ../matchedTree_MuGun_PU300_EMTFpp.root      --out efficiencies/effs_SingleMu_PU300_TDR_MC.root

# python make_eff_plots.py --in ../matchedTree_MuGun_PU0_alldetector.root      --out efficiencies/effs_SingleMu_PU0_alldetector.root
# python make_eff_plots.py --in ../matchedTree_MuGun_PU200_alldetector.root    --out efficiencies/effs_SingleMu_PU200_alldetector.root
# python make_eff_plots.py --in ../matchedTree_MuGun_PU300_alldetector.root    --out efficiencies/effs_SingleMu_PU300_alldetector.root


python make_eff_plots.py --in ../matchedTree_MuGun_PU0_alldetector_mindpt.root      --out efficiencies/effs_SingleMu_PU0_alldetector_mindpt.root
python make_eff_plots.py --in ../matchedTree_MuGun_PU200_alldetector_mindpt.root    --out efficiencies/effs_SingleMu_PU200_alldetector_mindpt.root
python make_eff_plots.py --in ../matchedTree_MuGun_PU300_alldetector_mindpt.root    --out efficiencies/effs_SingleMu_PU300_alldetector_mindpt.root

python make_eff_plots.py --in ../matchedTree_MuGun_PU0_alldetector_maxpt.root      --out efficiencies/effs_SingleMu_PU0_alldetector_maxpt.root
python make_eff_plots.py --in ../matchedTree_MuGun_PU200_alldetector_maxpt.root    --out efficiencies/effs_SingleMu_PU200_alldetector_maxpt.root
python make_eff_plots.py --in ../matchedTree_MuGun_PU300_alldetector_maxpt.root    --out efficiencies/effs_SingleMu_PU300_alldetector_maxpt.root
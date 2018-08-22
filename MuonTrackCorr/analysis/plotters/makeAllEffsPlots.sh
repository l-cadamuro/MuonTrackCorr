for pl in MuMu_flatPt_0PU ZToMuMu_200PU; do
# for pl in MuMu_flatPt_0PU; do
# for pl in ZToMuMu_200PU; do
    for q in 90 95 99; do
        python make_eff_plots.py --in ../matched_tree_${pl}_fix_q${q}.root --out efficiencies/effs_${pl}_fix_q${q}.root
    done
done

python make_eff_plots.py --in ../matched_tree_MuMu_flatPt_0PU_q99_relax0p5.root --out efficiencies/effs_MuMu_flatPt_0PU_q99_relax0p5.root
python make_eff_plots.py --in ../matched_tree_ZToMuMu_200PU_q99_relax0p5.root   --out efficiencies/effs_ZToMuMu_200PU_q99_relax0p5.root
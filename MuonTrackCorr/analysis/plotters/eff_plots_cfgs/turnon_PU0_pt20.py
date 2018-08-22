inputs = [
    {
        'name' : "eff_upgtkmu_vspt_ptgt20",
        'file' : "efficiencies/effs_MuMu_flatPt_0PU_fix_q99.root",
        'color' : ROOT.kGreen+1,
        'legend' : '#alpha = 99%',
    },
    {
        'name' : "eff_upgtkmu_vspt_ptgt20",
        'file' : "efficiencies/effs_MuMu_flatPt_0PU_fix_q95.root",
        'color' : ROOT.kBlue,
        'legend' : '#alpha = 95%',
    },
    {
        'name'   : "eff_upgtkmu_vspt_ptgt20",
        'file'   : "efficiencies/effs_MuMu_flatPt_0PU_fix_q90.root",
        'color'  : ROOT.kRed,
        'legend' : '#alpha = 90%',
    },
]

frame = ROOT.TH1D('frame', ';p_{T}^{gen #mu} [GeV]; Efficiency', 200, 0, 200)
frame.SetMinimum(0)
frame.SetMaximum(1.09)
leg_coords = (0.6, 0.2, 0.88, 0.5)
testo = "#mu gun, PU 0"
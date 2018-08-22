inputs = [
    {
        'name' : "eff_upgtkmu_vspt_ptgt0",
        'file' : "efficiencies/effs_MuMu_flatPt_0PU_fix_q99.root",
        'color' : ROOT.kBlue,
        'legend' : 'Correlator',
    },
    {
        'name' : "eff_upgtkmu_vspt_ptgt0",
        'file' : "efficiencies/effs_MuMu_flatPt_0PU_trkPreFilter.root",
        'color' : ROOT.kRed,
        'legend' : 'Correlator - track prefilter',
    },
    # {
    #     'name'   : "eff_myimpltkmu_vspt_ptgt0",
    #     'file'   : "efficiencies/effs_MuMu_flatPt_0PU_q99_relax0p5.root",
    #     'color'  : ROOT.kGray+1,
    #     'legend' : 'CMSSW implementation',
    # },
]

frame = ROOT.TH1D('frame', ';p_{T}^{gen #mu} [GeV]; Efficiency', 200, 0, 30)
frame.SetMinimum(0)
frame.SetMaximum(1.09)
leg_coords = (0.6, 0.2, 0.88, 0.5)
testo = "#mu gun, PU 0"

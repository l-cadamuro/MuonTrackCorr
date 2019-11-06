inputs = [
    {
        'name'   : "eff_standalone_ovrl_vspt_ptgt20_eta0p8to1p2",
        'file'   : "efficiencies/effs_SingleMu_PU300_alldetector_maxpt.root",
        'color'  : ROOT.kGray,
        'legend' : 'OMTF',
    },
    {
        'name'   : "eff_mantra_tkmu_ovrl_vspt_ptgt20_eta0p8to1p2",
        'file'   : "efficiencies/effs_SingleMu_PU300_alldetector_maxpt.root",
        'color'  : ROOT.kGreen+2,
        'legend' : 'TkMu, overlap, max p_{T}',
    },
    {
        'name'   : "eff_mantra_tkmu_ovrl_vspt_ptgt20_eta0p8to1p2",
        'file'   : "efficiencies/effs_SingleMu_PU300_alldetector_mindpt.root",
        'color'  : ROOT.kRed+2,
        'legend' : 'TkMu, overlap, min p_{T}^{#mu}/p_{T}^{trk}',
    },
]

frame = ROOT.TH1D('frame', ';p_{T}; Efficiency', 100, 0, 100)
frame.SetMinimum(0)
frame.SetMaximum(1.09)
leg_coords = (0.2, 0.3, 0.5, 0.5)
# testo = "#mu gun, PU 0"
testo = None
cms_header = True

# inputs = [
#     {
#         'name'   : "eff_emtf_vspt_ptgt20",
#         'file'   : "efficiencies/effs_MuMu_flatPt_0PU_fix_q99.root",
#         'color'  : ROOT.kAzure+1,
#         'legend' : 'EMTF standalone',
#     },
#     {
#         'name'   : "eff_trk_vspt_ptgt20",
#         'file'   : "efficiencies/effs_MuMu_flatPt_0PU_fix_q99.root",
#         'color'  : ROOT.kOrange,
#         'legend' : 'L1 TT standalone',
#     },
#     {
#         'name'   : "eff_upgtkmu_vspt_ptgt20",
#         'file'   : "efficiencies/effs_MuMu_flatPt_0PU_fix_q99.root",
#         'color'  : ROOT.kRed,
#         'legend' : 'Correlator',
#     },
# ]

inputs = [
    {
        'name'   : "eff_emtf_vspt_ptgt20",
        'file'   : "efficiencies/effs_MuMu_flatPt_0PU_q99_relax0p5.root",
        'color'  : ROOT.kAzure+1,
        'legend' : 'EMTF standalone',
    },
    {
        'name'   : "eff_trk_vspt_ptgt20",
        'file'   : "efficiencies/effs_MuMu_flatPt_0PU_q99_relax0p5.root",
        'color'  : ROOT.kOrange,
        'legend' : 'L1 TT standalone',
    },
    {
        'name'   : "eff_upgtkmu_vspt_ptgt20",
        'file'   : "efficiencies/effs_MuMu_flatPt_0PU_q99_relax0p5.root",
        'color'  : ROOT.kRed,
        'legend' : 'Correlator',
    },
]

frame = ROOT.TH1D('frame', ';p_{T}^{gen #mu} [GeV]; Efficiency', 100, 0, 100)
frame.SetMinimum(0)
frame.SetMaximum(1.09)
leg_coords = (0.6, 0.2, 0.88, 0.5)
testo = "#mu gun, PU 0"
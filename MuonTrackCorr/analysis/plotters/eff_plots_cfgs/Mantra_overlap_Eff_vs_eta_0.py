inputs = [
    {
        'name'   : "eff_standalone_ovrl_vseta_ptgt0_all",
        'file'   : "efficiencies/effs_SingleMu_PU200_alldetector.root",
        'color'  : ROOT.kGreen,
        'legend' : 'OMTF',
    },
    {
        'name'   : "eff_mantra_tkmu_ovrl_vseta_ptgt0_all",
        'file'   : "efficiencies/effs_SingleMu_PU200_alldetector.root",
        'color'  : ROOT.kGreen+2,
        'legend' : 'TkMu, overlap',
    },
]

frame = ROOT.TH1D('frame', ';#eta; Efficiency', 100, -3, 3)
frame.SetMinimum(0)
frame.SetMaximum(1.09)
leg_coords = (0.2, 0.3, 0.5, 0.5)
# testo = "#mu gun, PU 0"
testo = None
cms_header = True

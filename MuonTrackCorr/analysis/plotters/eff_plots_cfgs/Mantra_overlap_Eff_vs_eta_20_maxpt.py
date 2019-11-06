inputs = [
    {
        'name'   : "eff_standalone_ovrl_vsabseta_ptgt20_all",
        'file'   : "efficiencies/effs_SingleMu_PU200_alldetector_maxpt.root",
        'color'  : ROOT.kGreen,
        'legend' : 'OMTF',
    },
    {
        'name'   : "eff_mantra_tkmu_ovrl_vsabseta_ptgt20_all",
        'file'   : "efficiencies/effs_SingleMu_PU200_alldetector_maxpt.root",
        'color'  : ROOT.kGreen+2,
        'legend' : 'TkMu, overlap',
    },
]

frame = ROOT.TH1D('frame', ';#eta; Efficiency', 100, 0.7, 1.3)
frame.SetMinimum(0)
frame.SetMaximum(1.09)
leg_coords = (0.5, 0.3, 0.8, 0.5)
# testo = "#mu gun, PU 0"
testo = None
cms_header = True

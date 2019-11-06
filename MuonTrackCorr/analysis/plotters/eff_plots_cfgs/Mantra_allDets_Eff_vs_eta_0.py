inputs = [
    {
        'name'   : "eff_standalone_barr_vseta_ptgt0_all",
        'file'   : "efficiencies/effs_SingleMu_PU300_alldetector.root",
        'color'  : ROOT.kRed,
        'legend' : 'kBMTF',
    },
    {
        'name'   : "eff_standalone_ovrl_vseta_ptgt0_all",
        'file'   : "efficiencies/effs_SingleMu_PU300_alldetector.root",
        'color'  : ROOT.kGreen,
        'legend' : 'OMTF',
    },
    {
        'name'   : "eff_standalone_endc_vseta_ptgt0_all",
        'file'   : "efficiencies/effs_SingleMu_PU300_alldetector.root",
        'color'  : ROOT.kAzure+1,
        'legend' : 'EMTF++',
    },
    ###
    {
        'name'   : "eff_mantra_tkmu_barr_vseta_ptgt0_all",
        'file'   : "efficiencies/effs_SingleMu_PU300_alldetector.root",
        'color'  : ROOT.kRed+2,
        'legend' : 'Mantra, barrel',
    },
    {
        'name'   : "eff_mantra_tkmu_ovrl_vseta_ptgt0_all",
        'file'   : "efficiencies/effs_SingleMu_PU300_alldetector.root",
        'color'  : ROOT.kGreen+2,
        'legend' : 'Mantra, overlap',
    },
    {
        'name'   : "eff_mantra_tkmu_endc_vseta_ptgt0_all",
        'file'   : "efficiencies/effs_SingleMu_PU300_alldetector.root",
        'color'  : ROOT.kBlue+2,
        'legend' : 'Mantra, endcap',
    },
]

frame = ROOT.TH1D('frame', ';#eta; Efficiency', 100, -3, 3)
frame.SetMinimum(0)
frame.SetMaximum(1.09)
leg_coords = (0.2, 0.3, 0.5, 0.5)
# testo = "#mu gun, PU 0"
testo = None
cms_header = True

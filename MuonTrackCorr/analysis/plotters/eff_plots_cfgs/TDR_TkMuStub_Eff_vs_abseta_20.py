inputs = [
    {
        'name'   : "eff_emtf_vsabseta_ptgt20",
        'file'   : "efficiencies/effs_SingleMu_PU200_TDR_MC.root",
        'color'  : ROOT.kAzure+1,
        'legend' : 'EMTF++',
    },
    # {
    #     'name'   : "eff_trk_vsabseta_ptgt20",
    #     'file'   : "efficiencies/effs_MuMu_flatPt_0PU_q99_relax0p5.root",
    #     'color'  : ROOT.kOrange,
    #     'legend' : 'L1 TT standalone',
    # },
    {
        'name'   : "eff_tkmu_vsabseta_ptgt20",
        'file'   : "efficiencies/effs_SingleMu_PU200_TDR_MC.root",
        'color'  : ROOT.kRed,
        'legend' : 'TkMu',
    },
    {
        'name'   : "eff_tkmustub_vsabseta_ptgt20",
        'file'   : "efficiencies/effs_SingleMu_PU200_TDR_MC.root",
        'color'  : ROOT.kGreen+2,
        'legend' : 'TkMuStub',
    },

]

frame = ROOT.TH1D('frame', ';|#eta|; Efficiency', 100, 1.2, 2.5)
frame.SetMinimum(0)
frame.SetMaximum(1.09)
leg_coords = (0.6, 0.3, 0.88, 0.5)
# testo = "#mu gun, PU 0"
testo = None
cms_header = True

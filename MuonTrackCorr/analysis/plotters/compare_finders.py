import ROOT


ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

def make_histogram(tIn, expr, cut, hname, bounds, sumw2=False):
    hformat = 'h (%s)' % bounds
    tIn.Draw(expr + ' >> ' + hformat, cut) ## note: if using goff, I can't retrieve the histo
    myh = ROOT.gPad.GetPrimitive("h");
    out_h = myh.Clone(hname)
    out_h.SetDirectory(0)
    if sumw2: out_h.Sumw2()
    return out_h



# fIn = ROOT.TFile.Open('../matched_tree_MuMu_flatPt_0PU_25Apr_TkMu.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_RelVal_PU0_27Apr_TkMu.root')
fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_RelVal_PU200_27Apr_TkMu.root')
tIn = fIn.Get('tree')

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)

hgen   = make_histogram(tIn,    "gen_pt",     "",               "hgen",     "100, 0, 100", sumw2=True)
htrk   = make_histogram(tIn,    "trk_pt",     "trk_pt > 0",     "htrk",     "100, 0, 100", sumw2=True)
hemtf  = make_histogram(tIn,    "emtf_pt",    "emtf_pt > 0",    "hemtf",    "100, 0, 100", sumw2=True)
htkmu  = make_histogram(tIn,    "tkmu_pt",    "tkmu_pt > 0",    "htkmu",    "100, 0, 100", sumw2=True)
hupgtkmu  = make_histogram(tIn, "upgtkmu_pt", "upgtkmu_pt > 0", "hupgtkmu", "100, 0, 100", sumw2=True)

# hgen   = make_histogram(tIn,    "gen_pt",     "",               "hgen",     "100, 0, 100", sumw2=True)
# htrk   = make_histogram(tIn,    "gen_pt",     "trk_pt > 0",     "htrk",     "100, 0, 100", sumw2=True)
# hemtf  = make_histogram(tIn,    "gen_pt",     "emtf_pt > 0",    "hemtf",    "100, 0, 100", sumw2=True)
# htkmu  = make_histogram(tIn,    "gen_pt",     "tkmu_pt > 0",    "htkmu",    "100, 0, 100", sumw2=True)
# hupgtkmu  = make_histogram(tIn, "gen_pt",     "upgtkmu_pt > 0", "hupgtkmu", "100, 0, 100", sumw2=True)


hgen.SetLineColor(ROOT.kBlack)
htrk.SetLineColor(ROOT.kGreen+1)
hemtf.SetLineColor(ROOT.kRed)
htkmu.SetLineColor(ROOT.kBlue)
hupgtkmu.SetLineColor(ROOT.kOrange)

hgen.SetMarkerColor(hgen.GetLineColor())
htrk.SetMarkerColor(htrk.GetLineColor())
hemtf.SetMarkerColor(hemtf.GetLineColor())
htkmu.SetMarkerColor(htkmu.GetLineColor())
hupgtkmu.SetMarkerColor(hupgtkmu.GetLineColor())

hgen.SetMarkerSize(1.2)
htrk.SetMarkerSize(0.6)
hemtf.SetMarkerSize(0.6)
htkmu.SetMarkerSize(0.6)
hupgtkmu.SetMarkerSize(0.6)

hgen.Draw()
htrk.Draw('same')
hemtf.Draw('same')
htkmu.Draw('same')
hupgtkmu.Draw('same')

c1.Update()
# raw_input()
c1.Print('finder_comparison.pdf', 'pdf')
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
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_TEST.root')
# fIn = ROOT.TFile.Open('../matched_tree_MuMu_flatPt_0PU_noSF.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_SF0p9.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_SF0p5.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_noSF.root')

# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_SF0p9fix.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_SF0p5fix.root')

# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_relax0p9.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_fix0p9.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_q99_delta0.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_q99_delta0_check.root')
# fIn = ROOT.TFile.Open("../matched_tree_ZToMuMu_200PU_q99_delta0_0p0_to_0p5.root")
# fIn = ROOT.TFile.Open("../matched_tree_ZToMuMu_200PU_q99_delta0_0p0_to_0p1.root")
fIn = ROOT.TFile.Open("../matched_tree_ZToMuMu_200PU_q99_relax0p5.root")

print fIn.GetName()
tIn = fIn.Get('tree')

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)
c1.SetFrameLineWidth(3)
c1.SetBottomMargin(0.13)
c1.SetLeftMargin(0.16)


# hgen   = make_histogram(tIn,    "gen_pt",     "",               "hgen",     "100, 0, 100", sumw2=True)
# htrk   = make_histogram(tIn,    "trk_pt",     "trk_pt > 0",     "htrk",     "100, 0, 100", sumw2=True)
# hemtf  = make_histogram(tIn,    "emtf_pt",    "emtf_pt > 0",    "hemtf",    "100, 0, 100", sumw2=True)
# htkmu  = make_histogram(tIn,    "tkmu_pt",    "tkmu_pt > 0",    "htkmu",    "100, 0, 100", sumw2=True)
# hupgtkmu  = make_histogram(tIn, "upgtkmu_pt", "upgtkmu_pt > 0", "hupgtkmu", "100, 0, 100", sumw2=True)

# hgen   = make_histogram(tIn,    "gen_pt",       "gen_pt < 0",   "hgen",     "20, 0, 20", sumw2=True) ### just a dummy histo
# htrk   = make_histogram(tIn,    "trk_mult",     "",             "htrk",     "20, 0, 20", sumw2=True)
# hemtf  = make_histogram(tIn,    "emtf_mult",    "",             "hemtf",    "20, 0, 20", sumw2=True)
# htkmu  = make_histogram(tIn,    "tkmu_mult",    "",             "htkmu",    "20, 0, 20", sumw2=True)
# hupgtkmu     = make_histogram(tIn, "upgtkmu_mult",    "",       "hupgtkmu", "20, 0, 20", sumw2=True)
# hmyimpltkmu  = make_histogram(tIn, "myimpltkmu_mult", "",       "hmyimplhtkmu",  "20, 0, 20", sumw2=True)

# hgen   = make_histogram(tIn,    "gen_pt",     "",               "hgen",     "100, 0, 100", sumw2=True)
# htrk   = make_histogram(tIn,    "gen_pt",     "trk_pt > 0",     "htrk",     "100, 0, 100", sumw2=True)
# hemtf  = make_histogram(tIn,    "gen_pt",     "emtf_pt > 0",    "hemtf",    "100, 0, 100", sumw2=True)
# htkmu  = make_histogram(tIn,    "gen_pt",     "tkmu_pt > 0",    "htkmu",    "100, 0, 100", sumw2=True)
# hupgtkmu  = make_histogram(tIn, "gen_pt",     "upgtkmu_pt > 0", "hupgtkmu", "100, 0, 100", sumw2=True)

hgen   = make_histogram(tIn,    "gen_pt",       "gen_pt < 0",   "hgen",     "15, 0, 15", sumw2=True) ### just a dummy histo
htrk   = hgen.Clone("dummy1")
hemtf  = hgen.Clone("dummy2")
htkmu  = hgen.Clone("dummy3")
hupgtkmu     = make_histogram(tIn, "upgtkmu_narb",    "",       "hupgtkmu", "15, 0, 15", sumw2=True)
hmyimpltkmu  = make_histogram(tIn, "myimpltkmu_narb", "",       "hmyimplhtkmu",  "15, 0, 15", sumw2=True)


print 'hgen      : ', hgen.GetEntries(), hgen.Integral(), hgen.Integral(-1,-1)
print 'htrk      : ', htrk.GetEntries(), htrk.Integral(), htrk.Integral(-1,-1)
print 'hemtf     : ', hemtf.GetEntries(), hemtf.Integral(), hemtf.Integral(-1,-1)
print 'htkmu     : ', htkmu.GetEntries(), htkmu.Integral(), htkmu.Integral(-1,-1)
print 'hupgtkmu  : ', hupgtkmu.GetEntries(), hupgtkmu.Integral(), hupgtkmu.Integral(-1,-1)
print 'hmyimpltkmu  : ', hmyimpltkmu.GetEntries(), hmyimpltkmu.Integral(), hmyimpltkmu.Integral(-1,-1)

print 'hgen : ',     hgen.GetMaximum()
print 'htrk : ',     htrk.GetMaximum()
print 'hemtf : ',    hemtf.GetMaximum()
print 'htkmu : ',    htkmu.GetMaximum()
print 'hupgtkmu : ', hupgtkmu.GetMaximum()
print 'hmyimpltkmu : ', hmyimpltkmu.GetMaximum()


hgen.SetLineColor(ROOT.kBlack)
htrk.SetLineColor(ROOT.kGreen+1)
hemtf.SetLineColor(ROOT.kRed)
htkmu.SetLineColor(ROOT.kBlue)
hupgtkmu.SetLineColor(ROOT.kRed)
hmyimpltkmu.SetLineColor(ROOT.kGray+1)

hgen.SetMarkerColor(hgen.GetLineColor())
htrk.SetMarkerColor(htrk.GetLineColor())
hemtf.SetMarkerColor(hemtf.GetLineColor())
htkmu.SetMarkerColor(htkmu.GetLineColor())
hupgtkmu.SetMarkerColor(hupgtkmu.GetLineColor())
hmyimpltkmu.SetMarkerColor(hmyimpltkmu.GetLineColor())

hgen.SetMarkerSize(1.2)
htrk.SetMarkerSize(0.6)
hemtf.SetMarkerSize(0.6)
htkmu.SetMarkerSize(0.6)
hupgtkmu.SetMarkerSize(0.6)
hmyimpltkmu.SetMarkerSize(0.6)

hgen.SetMarkerStyle(8)
htrk.SetMarkerStyle(8)
hemtf.SetMarkerStyle(8)
htkmu.SetMarkerStyle(8)
hupgtkmu.SetMarkerStyle(8)
hmyimpltkmu.SetMarkerStyle(8)


hgen.GetXaxis().SetTitleSize(0.05)
hgen.GetYaxis().SetTitleSize(0.05)
hgen.GetXaxis().SetLabelSize(0.045)
hgen.GetYaxis().SetLabelSize(0.045)


mmaxs = [
    hgen.GetMaximum(),
    htrk.GetMaximum(),
    hemtf.GetMaximum(),
    htkmu.GetMaximum(),
    hupgtkmu.GetMaximum(),
    hmyimpltkmu.GetMaximum(),
]
mmax = max(mmaxs)

# hgen.SetTitle(';p_{T}^{gen} [GeV]; Efficiency')
hgen.SetTitle(';N matched; a.u.')

hgen.SetMaximum(1.15*mmax)
hgen.Draw()
htrk.Draw('pl same')
hemtf.Draw('pl same')
htkmu.Draw('pl same')
hupgtkmu.Draw('pl same')
hmyimpltkmu.Draw('pl same')

leg = ROOT.TLegend(0.5, 0.5, 0.88, 0.75)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
# leg.AddEntry(hgen,        "Gen", 'lep')
# leg.AddEntry(hemtf,       "EMTF", 'lep')
# leg.AddEntry(htrk,        "L1 TT", 'lep')
# leg.AddEntry(htkmu,       "TT + EMTF (current CMSSW)", 'lep')
leg.AddEntry(hupgtkmu,    "Correlator - relaxed #varepsilon", 'lep')
leg.AddEntry(hmyimpltkmu, "CMSSW implementation", 'lep')
leg.Draw()


c1.Update()
# raw_input()
c1.Print('finder_comparison.pdf', 'pdf')
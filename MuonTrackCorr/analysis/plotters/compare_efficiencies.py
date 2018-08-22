import ROOT

def make_histogram(tIn, expr, cut, hname, bounds, sumw2=False):
    hformat = 'h (%s)' % bounds
    tIn.Draw(expr + ' >> ' + hformat, cut) ## note: if using goff, I can't retrieve the histo
    myh = ROOT.gPad.GetPrimitive("h");
    out_h = myh.Clone(hname)
    out_h.SetDirectory(0)
    if sumw2: out_h.Sumw2()
    return out_h

def make_eff(tIn, expr, cut, cutpass, bounds, eff_name):
    cpass = '(' + cut + ') && ' + cutpass if cut.strip() else cutpass
    # print cut
    # print cpass
    hAll  = make_histogram(tIn, expr, cut   , eff_name + '_all',  bounds)
    hPass = make_histogram(tIn, expr, cpass , eff_name + '_pass', bounds)
    oeff = ROOT.TEfficiency(hPass,hAll)
    oeff.SetName(eff_name)
    return oeff

def setStyle(frame, c1):
    c1.SetFrameLineWidth(3)
    c1.SetBottomMargin(0.13)
    c1.SetLeftMargin(0.13)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetLabelSize(0.045)

# fIn = ROOT.TFile.Open('../matched_tree_MuMu_flatPt_0PU_25Apr_TkMu_prePhiFix.root')
# fIn = ROOT.TFile.Open('../matched_tree_MuMu_flatPt_0PU_25Apr_TkMu.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_RelVal_PU200_27Apr.root')

# fIn = ROOT.TFile.Open('../matched_tree_MuMu_flatPt_0PU_25Apr_TkMu.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_RelVal_PU0_27Apr_TkMu.root')

# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU.root')
# fIn = ROOT.TFile.Open('../matched_tree_MuMu_flatPt_0PU.root')

# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_TEST.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_noSF.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_SF0p5.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_SF0p9.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_noSF.root')
# fIn = ROOT.TFile.Open('../matched_tree_MuMu_flatPt_0PU_noSF.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_SF0p9fix.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_SF0p9.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_relax0p9.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_fix0p9.root')
# fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_q99_delta0_check.root')
# fIn = ROOT.TFile.Open("../matched_tree_ZToMuMu_200PU_q99_delta0_0p0_to_0p5.root")
fIn = ROOT.TFile.Open("../matched_tree_ZToMuMu_200PU_q99_delta0_0p0_to_0p1.root")

print fIn.GetName()
tIn = fIn.Get('tree')

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
# c1.SetFrameLineWidth(3)


# threshold = 0 ### use min 0 which means match exists
# nbins = 50
# xmin  = 0
# xmax  = 100 
# x_var = 'gen_pt'
# x_title = 'p_{T}^{gen} [GeV]'

threshold = 0 ### use min 0 which means match exists
nbins = 50
xmin  = -2.4
xmax  = 2.4 
x_var = 'gen_eta'
x_title = '#eta^{gen}'

ymin = 0.0 ### value or None
ymax = 1.1

eff_emtf    = make_eff(tIn, x_var, '', 'emtf_pt > %f'    % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_emtf')
eff_trk     = make_eff(tIn, x_var, '', 'trk_pt > %f'     % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_trk')
eff_tkmu    = make_eff(tIn, x_var, '', 'tkmu_pt > %f'    % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_tkmu')
eff_upgtkmu = make_eff(tIn, x_var, '', 'upgtkmu_pt > %f' % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_upgtkmu')
eff_myimpltkmu    = make_eff(tIn, x_var, '', 'myimpltkmu_pt > %f'    % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_myimpltkmu')

eff_emtf.SetLineColor(ROOT.kRed)
eff_trk.SetLineColor(ROOT.kGreen+1)
eff_tkmu.SetLineColor(ROOT.kBlue)
eff_upgtkmu.SetLineColor(ROOT.kBlack)
eff_myimpltkmu.SetLineColor(ROOT.kCyan)

frame = ROOT.TH1D("frame", ';%s;Efficiency' % x_title, nbins, xmin, xmax)
setStyle(frame, c1)

if ymin: frame.SetMinimum(ymin)
if ymax: frame.SetMaximum(ymax)

frame.Draw()
# eff_emtf.Draw('same')
# eff_trk.Draw('same')
# eff_tkmu.Draw('same')
eff_upgtkmu.Draw('same')
eff_myimpltkmu.Draw('same')

leg = ROOT.TLegend(0.5, 0.5, 0.88, 0.75)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
# leg.AddEntry(eff_emtf, "EMTF", 'lep')
# leg.AddEntry(eff_trk,  "L1 TT", 'lep')
# leg.AddEntry(eff_tkmu, "TT + EMTF (current CMSSW)", 'lep')
leg.AddEntry(eff_upgtkmu, "TT + EMTF (new)", 'lep')
leg.AddEntry(eff_myimpltkmu, "TT + EMTF (CMSSW, my impl.)", 'lep')
leg.Draw()

c1.Update()
# raw_input()
# c1.Print('efficiencies/eff_plot_prePhiFix.pdf', 'pdf')
# fOut = ROOT.TFile('efficiencies/eff_plot_prePhiFix.root', 'recreate')
c1.Print('efficiencies/eff_plot.pdf', 'pdf')
fOut = ROOT.TFile('efficiencies/eff_plot.root', 'recreate')
eff_emtf.Write()
eff_trk.Write()
eff_tkmu.Write()
eff_upgtkmu.Write()
eff_myimpltkmu.Write()
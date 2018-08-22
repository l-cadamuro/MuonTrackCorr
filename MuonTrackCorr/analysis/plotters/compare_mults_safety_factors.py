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

# sfs = [0, 0.05, 0.1, 0.25, 0.5, 0.75, 0.99]
# colors = {
#     0    : ROOT.kBlack,
#     0.05 : ROOT.kBlue,
#     0.1  : ROOT.kRed,
#     0.25 : ROOT.kOrange,
#     0.5  : ROOT.kGreen+1,
#     0.75 : ROOT.kCyan,
#     0.99 : ROOT.kViolet, 
# }

sfs = [-0.01, -0.05, -0.1, -0.2, -0.5]
colors = {
    -0.01 : ROOT.kBlack,
    -0.05 : ROOT.kBlue,
    -0.1  : ROOT.kRed,
    -0.2  : ROOT.kOrange,
    -0.5  : ROOT.kGreen+1,
}

effs = []

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
# c1.SetFrameLineWidth(3)

# threshold = 0 ### use min 0 which means match exists
# nbins = 50
# xmin  = -3.0
# xmax  = 3.0 
# x_var = 'gen_eta'
# x_title = '#eta^{gen}'


threshold = 0 ### use min 0 which means match exists
nbins = 10
xmin  = 0
xmax  = 10
# x_var = 'gen_pt'
# x_title = 'p_{T}^{gen} [GeV]'
x_var = 'upgtkmu_narb'
x_title = 'N_{trk}^{arbitrated}'



for sf in sfs:

    print 'sf = ' , sf
    # fIn = ROOT.TFile.Open('../matched_tree_ZToMuMu_200PU_sf_%s.root' % str(sf))
    fname = '../matched_tree_ZToMuMu_200PU_q99_rfrom_%s_high.root' % str(sf)
    # fname = '../matched_tree_ZToMuMu_200PU_q99_rfrom_%s_low.root' % str(sf)
    print fname
    fIn = ROOT.TFile.Open(fname)
    tIn = fIn.Get('tree')

    # eff_emtf    = make_eff(tIn, x_var, '', 'emtf_pt > %f'    % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_emtf')
    # eff_trk     = make_eff(tIn, x_var, '', 'trk_pt > %f'     % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_trk')
    # eff_tkmu    = make_eff(tIn, x_var, '', 'tkmu_pt > %f'    % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_tkmu')
    # eff_upgtkmu = make_eff(tIn, x_var, '', 'upgtkmu_pt > %f' % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_upgtkmu')
    # eff_myimpltkmu    = make_eff(tIn, x_var, '', 'myimpltkmu_pt > %f'    % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_myimpltkmu')
    
    eff_upgtkmu = make_histogram(tIn, x_var, 'upgtkmu_pt > %f' % float(threshold),  'eff_upgtkmu_%s' % str(sf), '%i, %f, %f' % (nbins, xmin, xmax))
    
    effs.append(eff_upgtkmu)
    fIn.Close()

# ymin = 0.0 ### value or None
# ymax = 1.1

for idx, sf in enumerate(sfs):
    # eff_emtf.SetLineColor(ROOT.kRed)
    # eff_trk.SetLineColor(ROOT.kGreen+1)
    # eff_tkmu.SetLineColor(ROOT.kBlue)
    # eff_upgtkmu.SetLineColor(ROOT.kBlack)
    # eff_myimpltkmu.SetLineColor(ROOT.kCyan)
    col = colors[sf] if sf in colors else idx+1
    effs[idx].SetLineColor(col)

ymin = 0.0
mmaxs = []
for e in effs: mmaxs.append(e.GetMaximum())
ymax = 1.15*max(mmaxs)

frame = ROOT.TH1D("frame", ';%s;Events' % x_title, nbins, xmin, xmax)
setStyle(frame, c1)

if ymin: frame.SetMinimum(ymin)
if ymax: frame.SetMaximum(ymax)

frame.Draw()
for e in effs:
    e.Draw('same')

leg = ROOT.TLegend(0.6, 0.2, 0.88, 0.55)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
for idx, e in reversed(list(enumerate(effs))):
    leg.AddEntry(e, "#Delta = {:.0f}%".format(100.*sfs[idx]), 'lep')
leg.Draw()

# frame.Draw()
# eff_emtf.Draw('same')
# eff_trk.Draw('same')
# eff_tkmu.Draw('same')
# eff_upgtkmu.Draw('same')
# eff_myimpltkmu.Draw('same')

# leg = ROOT.TLegend(0.5, 0.5, 0.88, 0.75)
# leg.SetFillStyle(0)
# leg.SetBorderSize(0)
# leg.AddEntry(eff_emtf, "EMTF", 'lep')
# leg.AddEntry(eff_trk,  "L1 TT", 'lep')
# leg.AddEntry(eff_tkmu, "TT + EMTF (current CMSSW)", 'lep')
# leg.AddEntry(eff_upgtkmu, "TT + EMTF (new)", 'lep')
# leg.AddEntry(eff_myimpltkmu, "TT + EMTF (CMSSW, my impl.)", 'lep')
# leg.Draw()

ttext = ROOT.TLatex(0.6, 0.6, "p_{T}^{tkmu} > %.0f GeV" % threshold)
ttext.SetNDC(True)
ttext.SetTextFont(42)
ttext.SetTextSize(0.04)
ttext.SetTextAlign(11)
ttext.Draw()

c1.Update()
# # raw_input()
# # c1.Print('efficiencies/eff_plot_prePhiFix.pdf', 'pdf')
# # fOut = ROOT.TFile('efficiencies/eff_plot_prePhiFix.root', 'recreate')
c1.Print('efficiencies/mult_plot_sfcompare.pdf', 'pdf')
# fOut = ROOT.TFile('efficiencies/eff_plot.root', 'recreate')
# eff_emtf.Write()
# eff_trk.Write()
# eff_tkmu.Write()
# eff_upgtkmu.Write()
# eff_myimpltkmu.Write()
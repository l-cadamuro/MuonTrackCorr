import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

toplot = [
    # 'DWcorr_default',
    'DWcorr_0p5At6GeV',
    'TPcorr_default',
    'TPcorr_SvenPars',
]

inputs = {
    'DWcorr_default'   : "efficiencies/effs_SingleMu_PU200_DWcorr_CMSSWdefaultNoRelax_mults.root",
    'DWcorr_0p5At6GeV' : "efficiencies/effs_SingleMu_PU200_DWcorr_relax0p5At6GeV_mults.root",
    'TPcorr_default'   : "efficiencies/effs_SingleMu_PU200_TPcorr_mults.root",
    'TPcorr_SvenPars'  : "efficiencies/effs_SingleMu_PU200_TPcorr_SvenPars_mults.root",
}


colors = {
    'DWcorr_default'   : ROOT.kRed - 6,
    'DWcorr_0p5At6GeV' : ROOT.kRed + 1,
    'TPcorr_default'   : ROOT.kBlue + 2,
    'TPcorr_SvenPars'  : ROOT.kAzure,
}

mstyles = {
    'DWcorr_default'   : 8,
    'DWcorr_0p5At6GeV' : 8,
    'TPcorr_default'   : 4,
    'TPcorr_SvenPars'  : 4,
}

msizes = {
    'DWcorr_default'   : 0.4,
    'DWcorr_0p5At6GeV' : 0.4,
    'TPcorr_default'   : 0.6,
    'TPcorr_SvenPars'  : 0.6,
}


legnames = {
    'DWcorr_default'   : 'Dynamic Windows',
    # 'DWcorr_0p5At6GeV' : 'Dynamic Windows w/ relax',
    'DWcorr_0p5At6GeV' : 'Dynamic Windows',
    'TPcorr_default'   : 'Fixed #Delta R = 0.7 match',
    'TPcorr_SvenPars'  : 'Fixed #Delta R = 0.2 match',
}

TP_scan_file = 'TP_scans/eff_fwd_TP_muonTrk.txt'

#######
# frame  = ROOT.TH1D('frame', ';p_{T} threshold [GeV]; Efficiency', 1000, 0, 100)
# plname = 'eff_tkmu_vspt_ptgt0'
# pttxt  = 'p_{T} inclusive'
# oname    = "eff_comparison_NovReview_ptgt0.pdf"
# frame.SetMinimum(0.0)
# frame.SetMaximum(1.09)
# doratio = True
# add_TP_scan = False

frame  = ROOT.TH1D('frame', ';p_{T} threshold [GeV]; Efficiency', 1000, 0, 100)
plname = 'eff_tkmu_vspt_ptgt20'
pttxt  = 'p_{T} > 20 GeV'
oname    = "eff_comparison_NovReview_ptgt20.pdf"
frame.SetMinimum(0.0)
frame.SetMaximum(1.09)
doratio = False
add_TP_scan = True

#######

frame.GetXaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleSize(0.05)

frame.GetXaxis().SetTitleFont(43)
frame.GetXaxis().SetTitleSize(22)
frame.GetYaxis().SetTitleFont(43)
frame.GetYaxis().SetTitleSize(22)

frame.GetXaxis().SetLabelFont(43)
frame.GetXaxis().SetLabelSize(16)
frame.GetYaxis().SetLabelFont(43)
frame.GetYaxis().SetLabelSize(16)

frame.GetXaxis().SetTitleOffset(1.1)
frame.GetYaxis().SetTitleOffset(1.3)

if doratio:
    ratioframe = frame.Clone('ratioframe')
    ratioframe.GetYaxis().SetTitle('Ratio')
    ratioframe.SetTitleOffset(4.0)
    ratioframe.GetYaxis().SetNdivisions(505)
    frame.GetXaxis().SetTitleSize(0)
    frame.GetXaxis().SetLabelSize(0)


# print inputs.items()
files  = {key : ROOT.TFile(f)           for (key, f) in inputs.items() if key in toplot}
# print files.items()
histos = {key : f.Get(plname) for (key, f) in files.items()}

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetBottomMargin(0.13)
c1.SetLeftMargin(0.15)
c1.SetFrameLineWidth(3)

if doratio:
    c1.cd()
    pad1 = ROOT.TPad ("pad1", "pad1", 0, 0.25, 1, 1.0)
    pad1.SetFrameLineWidth(3)
    pad1.SetLeftMargin(0.15);
    pad1.SetBottomMargin(0.02);
    pad1.SetTopMargin(0.055);
    # pad1.Draw()

    c1.cd()
    pad2 = ROOT.TPad ("pad2", "pad2", 0, 0.0, 1, 0.2496)
    pad2.SetLeftMargin(0.15);
    pad2.SetTopMargin(0.05);
    # pad2.SetBottomMargin(0.35);
    pad2.SetBottomMargin(0.35);
    pad2.SetGridy(True);
    pad2.SetFrameLineWidth(3)
    # self.pad2.Draw()
    # self.pad2.SetGridx(True);
else:
    pad1 = ROOT.TPad ("pad1", "pad1", 0, 0.0, 1.0, 1.0)
    pad1.SetFrameLineWidth(3)
    pad1.SetLeftMargin(0.15);
    pad1.SetBottomMargin(0.12);
    pad1.SetTopMargin(0.055);
    pad1.Draw()
    pad2 = None

### compute tot rate

# orbitFreq    = 11.2456 # kHz
# # nCollBunches = 1866
# nCollBunches = 2808
# khZconv      = 1 ### converts kHz to Hz : 1000 -> Hz, 1 -> kHz
# scale        = khZconv * orbitFreq * nCollBunches

# for h in toplot: histos[h].Scale(scale)
for h in toplot: histos[h].SetLineColor(colors[h])
for h in toplot: histos[h].SetMarkerColor(colors[h])

for h in toplot: histos[h].SetMarkerStyle(mstyles[h])
for h in toplot: histos[h].SetMarkerSize(msizes[h])

if add_TP_scan:
    gr_TP = ROOT.TGraph(TP_scan_file)
    gr_TP.SetLineColor(ROOT.kBlack)
    gr_TP.SetMarkerColor(ROOT.kBlack)
    gr_TP.SetMarkerStyle(8)
    gr_TP.SetMarkerSize(0.9)

leg = ROOT.TLegend(0.5, 0.6-0.3, 0.88, 0.88-0.3)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
for h in toplot:
    leg.AddEntry(histos[h], legnames[h], 'lep')
if add_TP_scan:
    leg.AddEntry(gr_TP, "CMS-TDR-15-02 (TP, 140 PU)", 'pl')

if doratio:
    PUtext = ROOT.TLatex(0.90, 0.96, "#sqrt{s} = 14 TeV, PU 200")
else:
    PUtext = ROOT.TLatex(0.90, 0.92, "#sqrt{s} = 14 TeV, PU 200")
PUtext.SetNDC(True)
PUtext.SetTextFont(43)
PUtext.SetTextSize(18)
PUtext.SetTextAlign(31)

PTtext = ROOT.TLatex(0.52, 0.22, pttxt)
PTtext.SetNDC(True)
PTtext.SetTextFont(43)
PTtext.SetTextSize(18)
PTtext.SetTextAlign(11)


### plot

# c1.SetLogy()
c1.cd()
pad1.Draw()
pad1.cd()
if not doratio: c1.cd() ## simple trick top maintain alignment
frame.Draw()
for h in histos.values():
    h.Draw('peZ same')
if add_TP_scan: gr_TP.Draw('p same')

leg.Draw()
PUtext.Draw()
PTtext.Draw()

if doratio:
    c1.cd()
    pad2.Draw()
    pad2.cd()
    
    eff_denom_name = 'TPcorr_default'
    effs_nums = [h for h in toplot if h != eff_denom_name]
    eff_denom = histos[eff_denom_name]
    effs = [histos[h].Clone('ratio_' + histos[h].GetName()) for h in effs_nums]

    ## convert all to histograms
    h_denom = eff_denom.GetPassedHistogram().Clone('eff_' + eff_denom.GetName())
    h_denom.Divide(eff_denom.GetTotalHistogram())

    ratios = [h.GetPassedHistogram().Clone('eff_' + h.GetName()) for h in effs]
    for idx, r in enumerate(ratios):
        r.Divide(effs[idx].GetTotalHistogram())
        r.SetLineColor(effs[idx].GetLineColor())
        r.SetMarkerColor(effs[idx].GetMarkerColor())
        r.SetMarkerStyle(effs[idx].GetMarkerStyle())
        r.SetMarkerSize(effs[idx].GetMarkerSize())

    for r in ratios: r.Divide(h_denom)
    ratioframe.SetMinimum(0.9)
    ratioframe.SetMaximum(1.1)
    ratioframe.Draw()
    for r in ratios: r.Draw('p same')


c1.Update()
c1.Print(oname, 'pdf')
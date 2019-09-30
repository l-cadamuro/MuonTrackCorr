import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


def setStyle(frame, c1):
    c1.SetFrameLineWidth(3)
    c1.SetBottomMargin(0.13)
    c1.SetLeftMargin(0.13)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetLabelSize(0.045)



toplot = [
    # 'DWcorr_default',
    # 'DWcorr_0p5At6GeV',
    # 'TPcorr_default',
    # 'TPcorr_SvenPars',
    'EMTF',
    'TkMu'
]

inputs = {
    'EMTF'   : ["../rate_200PU_TDR_MC_EMTFmode_SvenTPFix.root", 'rate_EMTF_lead_mu_pt'],
    'TkMu'   : ["../rate_200PU_TDR_MC_EMTFmode_SvenTPFix.root", 'rate_TPTkMu_lead_mu_pt'],
}

colors = {
    'EMTF'   : ROOT.kAzure+1,
    'TkMu'   : ROOT.kRed,
}

legnames = {
    'EMTF' : 'EMTF',
    'TkMu' : 'TkMu',
}

# TP_scan_file = 'TP_scans/rate_fwd_TP_muonTrk.txt'

doratio     = False
# add_TP_scan = True


# print inputs.items()
files  = {key : (ROOT.TFile(f[0]), f[1]) for (key, f) in inputs.items() if key in toplot}
# print files.items()
histos = {key : f[0].Get(f[1]) for (key, f) in files.items()}

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
frame = ROOT.TH1D('frame', ';p_{T} threshold [GeV]; Rate [kHz]', 1000, 0, 100)

# c1.SetBottomMargin(0.13)
# c1.SetLeftMargin(0.15)
# c1.SetFrameLineWidth(3)

setStyle(frame, c1)

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



frame.SetMinimum(1.e-2)
frame.SetMaximum(1e5)

frame.GetXaxis().SetTitleOffset(1.1)
frame.GetYaxis().SetTitleOffset(1.3)

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


if doratio:
    ratioframe = frame.Clone('ratioframe')
    ratioframe.GetYaxis().SetTitle('Ratio')
    ratioframe.SetTitleOffset(4.0)
    ratioframe.GetYaxis().SetNdivisions(505)
    frame.GetXaxis().SetTitleSize(0)
    frame.GetXaxis().SetLabelSize(0)
    

### compute tot rate

orbitFreq    = 11.2456 # kHz
# nCollBunches = 1866
nCollBunches = 2748 #2808 is LHC Phase-1
khZconv      = 1 ### converts kHz to Hz : 1000 -> Hz, 1 -> kHz
scale        = khZconv * orbitFreq * nCollBunches

for h in toplot: histos[h].Scale(scale)
for h in toplot: histos[h].SetLineColor(colors[h])

# if add_TP_scan:
#     gr_TP = ROOT.TGraph(TP_scan_file)
#     gr_TP.SetLineColor(ROOT.kBlack)
#     gr_TP.SetMarkerColor(ROOT.kBlack)
#     gr_TP.SetMarkerStyle(8)
#     gr_TP.SetMarkerSize(0.9)

# leg = ROOT.TLegend(0.5, 0.6, 0.88, 0.88)
leg = ROOT.TLegend(0.5, 0.7, 0.88, 0.88)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
for h in toplot:
    leg.AddEntry(histos[h], legnames[h], 'l')
# if add_TP_scan:
#     leg.AddEntry(gr_TP, "CMS-TDR-15-02 (TP, 140 PU)", 'pl')

if doratio:
    PUtext = ROOT.TLatex(0.90, 0.96, "#sqrt{s} = 14 TeV, PU 200, %i colliding bunches" % nCollBunches)
else:
    PUtext = ROOT.TLatex(0.90, 0.92, "#sqrt{s} = 14 TeV, PU 200, %i colliding bunches" % nCollBunches)
PUtext.SetNDC(True)
PUtext.SetTextFont(43)
PUtext.SetTextSize(18)
PUtext.SetTextAlign(31)

### plot

if not doratio: c1.SetLogy()
else: pad1.SetLogy()
c1.cd()
pad1.Draw()
pad1.cd()
if not doratio: c1.cd() ## simple trick top maintain alignment
frame.Draw()
for h in histos.values():
    h.Draw('hist same')
# if add_TP_scan: gr_TP.Draw('p same')

leg.Draw()
PUtext.Draw()

if doratio:
    c1.cd()
    pad2.SetLogy()
    pad2.Draw()
    pad2.cd()
    h_denom = 'TPcorr_default'
    h_nums = [h for h in toplot if h != h_denom]
    ratios = [histos[h].Clone('ratio_' + histos[h].GetName()) for h in h_nums]
    for r in ratios: r.Divide(histos[h_denom])
    ratioframe.SetMinimum(0.01)
    ratioframe.SetMaximum(1)
    ratioframe.Draw()
    for r in ratios: r.Draw('hist same')


c1.Update()
c1.Print("rate_comparison_TDR.pdf", 'pdf')
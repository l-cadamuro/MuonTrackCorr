import ROOT

def SetStyle(gr, color, mstyle = 8):
    gr.SetLineColor(color)
    gr.SetMarkerColor(color)
    gr.SetMarkerStyle(mstyle)
    gr.SetMarkerSize(0.8)

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

# suffix = '_eta'
# xmin, xmax = -3, 3
# xtitle = 'Gen #mu #eta'

suffix = '_eta'
xmin, xmax = 1.1, 2.6
xtitle = 'Gen #mu |#eta|'

# suffix = ''
# xmin, xmax = 0, 130
# xtitle = 'Gen #mu p_{t} [GeV]'

# inputname = '../eff_onlyEMTFdigis.root'
# pdfname = 'eff_plot_onlyEMTFdigis%s.pdf' % suffix

# inputname = '../eff_plots_pt22.root'
# pdfname = 'eff_plots_pt22%s.pdf' % suffix

# inputname = '../eff_plots_phaseI_digi.root'
# pdfname = 'eff_plots_phaseI_digi%s.pdf' % suffix

inputname = '../plots_JFsynch_pt20_eta1p2_2p4_scaledPt_tree.root'
pdfname = 'eff_plots_JFsynch_pt20_eta1p2_2p4_scaledPt%s.pdf' % suffix

# inputname = '../eff_plots.root'
# pdfname = 'eff_plot%s.pdf' % suffix

fIn = ROOT.TFile.Open(inputname)

eff_trk       = fIn.Get('eff_trk%s' % suffix)
eff_emtf      = fIn.Get('eff_emtf%s' % suffix)
eff_emtf_nopt = fIn.Get('eff_emtf_nopt%s' % suffix)
eff_comb      = fIn.Get('eff_comb%s' % suffix)

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)
frame = ROOT.TH1F('frame', ';%s; Efficiency' % xtitle, 1000, xmin, xmax)

SetStyle(eff_trk, ROOT.kGreen+1)
SetStyle(eff_emtf, ROOT.kRed)
SetStyle(eff_emtf_nopt, ROOT.kRed+3, 4)
SetStyle(eff_comb, ROOT.kBlue)

leg = ROOT.TLegend(0.4, 0.15, 0.88, 0.45)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.AddEntry(eff_trk, "L1 Tracks only", 'lp')
leg.AddEntry(eff_emtf, "EMTF only", 'lp')
leg.AddEntry(eff_emtf_nopt, "EMTF only (no p_{T} sel.)", 'lp')
leg.AddEntry(eff_comb, "EMTF + L1 Tracks", 'lp')

# leg = ROOT.TLegend(0.4, 0.2, 0.88, 0.4)
# leg.SetBorderSize(0)
# leg.SetFillStyle(0)
# leg.AddEntry(eff_emtf, "EMTF, p_{T} > 20 GeV", 'lp')
# leg.AddEntry(eff_emtf_nopt, "EMTF, inclusive", 'lp')



frame.Draw()
eff_trk.Draw('psame')
eff_emtf.Draw('psame')
eff_emtf_nopt.Draw('psame')
eff_comb.Draw('psame')
leg.Draw()
c1.Update()
c1.Print(pdfname, 'pdf')
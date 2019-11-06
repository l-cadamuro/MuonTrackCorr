import ROOT
import sys
import collections
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def setStyle(frame, c1):
    c1.SetFrameLineWidth(3)
    c1.SetBottomMargin(0.13)
    c1.SetTopMargin(0.13)
    c1.SetLeftMargin(0.13)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetLabelSize(0.045)

def calc_rate_err (h_pt, ibin, scale):
    """ calculate the error on the rate division """
    denom = h_pt.Integral(-1, -1)
    num = h_pt.Integral(ibin, -1)
    rate = 1.*scale*num/denom
    print "... rate", rate

    ### the righth way
    # err_up = ROOT.TEfficiency.Bayesian  (denom, num, 0.683, 1, 1, True)
    # err_do = ROOT.TEfficiency.Bayesian  (denom, num, 0.683, 1, 1, False)
    # print 'err_up = ', err_up, "err_do = ", err_do, "( pass, tot = ", num, denom, ")"

    ## being small numbers, sqrt is OK
    err_up = 1./ROOT.TMath.Sqrt(num)
    err_do = 1./ROOT.TMath.Sqrt(num)
    return (err_up, err_do)

PU_points = collections.OrderedDict()

icfg = 0
if len(sys.argv) > 1:
    icfg = int(sys.argv[1])

inputs = {
    140 : 'ZB_PU140_plots_ZeroBias/histos.root',
    200 : 'ZB_PU200_plots_ZeroBias/histos.root',
    250 : 'ZB_PU250_plots_ZeroBias/histos.root',
    300 : 'ZB_PU300_plots_ZeroBias/histos.root',
}


outfolder = 'ZB_plots_vs_pt' ## or None for no plots

if icfg == 0: ## tracks
    print "... doing tracks pt > 5 GeV"
    hname = 'n_trk_ptgt5_ext'
    oname = "avg_track5_vs_PU.pdf"
    title = "Average N_{tracks} with p_{T} > 5 GeV, #chi^{2} < 100 and N_{stubs} #geq 4 in positive endcap"

if icfg == 1: ## tracks
    print "... doing tracks pt > 10 GeV"
    hname = 'n_trk_ptgt10'
    oname = "avg_track10_vs_PU.pdf"
    title = "Average N_{tracks} with p_{T} > 10 GeV, #chi^{2} < 100 and N_{stubs} #geq 4 in positive endcap"

if icfg == 2: ## tracks
    print "... doing tracks pt > 20 GeV"
    hname = 'n_trk_ptgt20'
    oname = "avg_track20_vs_PU.pdf"
    title = "Average N_{tracks} with p_{T} > 20 GeV, #chi^{2} < 100 and N_{stubs} #geq 4 in positive endcap"

#################

if icfg == 3: ## tracks barrel
    print "... doing tracks barrel pt > 5 GeV"
    hname = 'n_trk_barr_ptgt5_ext'
    oname = "avg_track5_barr_vs_PU.pdf"
    title = "Average N_{tracks} with p_{T} > 5 GeV, #chi^{2} < 100 and N_{stubs} #geq 4  in barrel"

if icfg == 4: ## tracks barrel
    print "... doing tracks barrel pt > 10 GeV"
    hname = 'n_trk_barr_ptgt10'
    oname = "avg_track10_barr_vs_PU.pdf"
    title = "Average N_{tracks} with p_{T} > 10 GeV, #chi^{2} < 100 and N_{stubs} #geq 4  in barrel"

if icfg == 5: ## tracks barrel
    print "... doing tracks barrel pt > 20 GeV"
    hname = 'n_trk_barr_ptgt20'
    oname = "avg_track20_barr_vs_PU.pdf"
    title = "Average N_{tracks} with p_{T} > 20 GeV, #chi^{2} < 100 and N_{stubs} #geq 4  in barrel"

############


if icfg == 6: ## tracks overlap
    print "... doing tracks overlap pt > 5 GeV"
    hname = 'n_trk_ovrl_ptgt5_ext'
    oname = "avg_track5_ovrl_vs_PU.pdf"
    title = "Average N_{tracks} with p_{T} > 5 GeV, #chi^{2} < 100 and N_{stubs} #geq 4  in positive overlap"

if icfg == 7: ## tracks overlap
    print "... doing tracks overlap pt > 10 GeV"
    hname = 'n_trk_ovrl_ptgt10'
    oname = "avg_track10_ovrl_vs_PU.pdf"
    title = "Average N_{tracks} with p_{T} > 10 GeV, #chi^{2} < 100 and N_{stubs} #geq 4  in positive overlap"

if icfg == 8: ## tracks overlap
    print "... doing tracks overlap pt > 20 GeV"
    hname = 'n_trk_ovrl_ptgt20'
    oname = "avg_track20_ovrl_vs_PU.pdf"
    title = "Average N_{tracks} with p_{T} > 20 GeV, #chi^{2} < 100 and N_{stubs} #geq 4  in positive overlap"

#################

if icfg == 9: ## EMTF
    print "... doing EMTF++"
    hname = 'EMTF_mu_endcap_pos'
    oname = "avg_EMTFpp_vs_PU.pdf"
    title = "Average N_{EMTF++} in positive endcap"

if icfg == 10: ## TkMu
    print "... doing TkMu"
    hname = 'TkMu_endcap_pos'
    oname = "avg_TkMu_vs_PU.pdf"
    title = "Average N_{TkMu} in positive endcap"

if icfg == 11: ## TkMu
    print "... doing TkMuStub"
    hname = 'TkMuStub_endcap_pos'
    oname = "avg_TkMuStub_vs_PU.pdf"
    title = "Average N_{TkMuStub} in positive endcap"

if icfg == 12: ## CSC S1
    print "... doing CSC S1"
    hname = 'n_CSC_S1_ext'
    oname = "avg_CSC_S1_vs_PU.pdf"
    title = "Average N_{CSC S1} in positive endcap"


###############

if icfg == 13: ## TkMu true
    print "... doing TkMu true"
    hname = 'TkMu_endcap_pos_genMuMatch'
    oname = "avg_TkMu_genMuMatch_vs_PU.pdf"
    title = "Average N_{TkMu} (true #mu) in positive endcap"

if icfg == 14: ## TkMu fake
    print "... doing TkMu fake"
    hname = 'TkMu_endcap_pos_genMuNoMatch'
    oname = "avg_TkMu_genMuNoMatch_vs_PU.pdf"
    title = "Average N_{TkMu} (fake #mu) in positive endcap"

if icfg == 15: ## TkMu Stub true
    print "... doing TkMuStub true"
    hname = 'TkMuStub_endcap_pos_genMuMatch'
    oname = "avg_TkMuStub_genMuMatch_vs_PU.pdf"
    title = "Average N_{TkMuStub} (true #mu) in positive endcap"

if icfg == 16: ## TkMu Stub fake
    print "... doing TkMuStub fake"
    hname = 'TkMuStub_endcap_pos_genMuNoMatch'
    oname = "avg_TkMuStub_genMuNoMatch_vs_PU.pdf"
    title = "Average N_{TkMuStub} (fake #mu) in positive endcap"

########################################

if icfg == 17: ## tracks
    print "... doing tracks pt > 5 GeV, chi2 < 50"
    hname = 'n_trk_ptgt5_ext_chi2lt50'
    oname = "avg_track5_vs_PU_chi2lt50.pdf"
    title = "Average N_{tracks} with p_{T} > 5 GeV, #chi^{2} < 50 and N_{stubs} #geq 4 in positive endcap"

if icfg == 18: ## tracks
    print "... doing tracks pt > 10 GeV, chi2 < 50"
    hname = 'n_trk_ptgt10_chi2lt50'
    oname = "avg_track10_vs_PU_chi2lt50.pdf"
    title = "Average N_{tracks} with p_{T} > 10 GeV, #chi^{2} < 50 and N_{stubs} #geq 4 in positive endcap"

if icfg == 19: ## tracks
    print "... doing tracks pt > 20 GeV, chi2 < 50"
    hname = 'n_trk_ptgt20_chi2lt50'
    oname = "avg_track20_vs_PU_chi2lt50.pdf"
    title = "Average N_{tracks} with p_{T} > 20 GeV, #chi^{2} < 50 and N_{stubs} #geq 4 in positive endcap"

#################

# if icfg == 20: ## tracks barrel
#     print "... doing tracks barrel pt > 5 GeV, chi2 < 50"
#     hname = 'n_trk_barr_ptgt5_ext_chi2lt50'
#     oname = "avg_track5_barr_vs_PU_chi2lt50.pdf"
#     title = "Average N_{tracks} with p_{T} > 5 GeV, #chi^{2} < 50 and N_{stubs} #geq 4  in barrel"

# if icfg == 21: ## tracks barrel
#     print "... doing tracks barrel pt > 10 GeV, chi2 < 50"
#     hname = 'n_trk_barr_ptgt10_chi2lt50'
#     oname = "avg_track10_barr_vs_PU_chi2lt50.pdf"
#     title = "Average N_{tracks} with p_{T} > 10 GeV, #chi^{2} < 50 and N_{stubs} #geq 4  in barrel"

# if icfg == 22: ## tracks barrel
#     print "... doing tracks barrel pt > 20 GeV, chi2 < 50"
#     hname = 'n_trk_barr_ptgt20_chi2lt50'
#     oname = "avg_track20_barr_vs_PU_chi2lt50.pdf"
#     title = "Average N_{tracks} with p_{T} > 20 GeV, #chi^{2} < 50 and N_{stubs} #geq 4  in barrel"

# ############


# if icfg == 23: ## tracks overlap
#     print "... doing tracks overlap pt > 5 GeV, chi2 < 50"
#     hname = 'n_trk_ovrl_ptgt5_ext_chi2lt50'
#     oname = "avg_track5_ovrl_vs_PU_chi2lt50.pdf"
#     title = "Average N_{tracks} with p_{T} > 5 GeV, #chi^{2} < 50 and N_{stubs} #geq 4  in positive overlap"

# if icfg == 24: ## tracks overlap
#     print "... doing tracks overlap pt > 10 GeV, chi2 < 50"
#     hname = 'n_trk_ovrl_ptgt10_chi2lt50'
#     oname = "avg_track10_ovrl_vs_PU_chi2lt50.pdf"
#     title = "Average N_{tracks} with p_{T} > 10 GeV, #chi^{2} < 50 and N_{stubs} #geq 4  in positive overlap"

# if icfg == 25: ## tracks overlap
#     print "... doing tracks overlap pt > 20 GeV, chi2 < 50"
#     hname = 'n_trk_ovrl_ptgt20_chi2lt50'
#     oname = "avg_track20_ovrl_vs_PU_chi2lt50.pdf"
#     title = "Average N_{tracks} with p_{T} > 20 GeV, #chi^{2} < 50 and N_{stubs} #geq 4  in positive overlap"

## retrieve the values
vals = []
for PU in [140, 200, 250, 300]:
    fIn = ROOT.TFile.Open(inputs[PU])
    hIn = fIn.Get(hname)
    y = hIn.GetMean()
    yerr = hIn.GetMeanError()
    vals.append((PU, y, yerr))
    fIn.Close()

#### now plot the values

ymin = 0
ymax = 1.15*max([x[1] for x in vals])

xmin = 0
xmax = 400

frame = ROOT.TH1D ('frame', '%s;PU;Average' % title, 100, xmin, xmax)
frame.SetMinimum(ymin)
frame.SetMaximum(ymax)

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
setStyle(frame, c1)
# c1.SetLogy()

gr = ROOT.TGraphAsymmErrors()
rates = []
for pt in vals:
    gr.SetPoint(gr.GetN(), pt[0], pt[1])
    gr.SetPointError(gr.GetN()-1, 0, 0, pt[2], pt[2])
    # h.SetDirectory(0)
    # h.Draw('same')

gr.SetMarkerStyle(8)
gr.SetMarkerSize(1.2)
gr.SetMarkerColor(ROOT.kBlue)
gr.SetLineColor(ROOT.kBlue)

# gr.Print()
# f = ROOT.TF1('lin', '[0]*x', 90, 300)
# f = ROOT.TF1('lin', '[0]*x', xmin, xmax)
# f.SetLineColor(ROOT.kGray)
# f.SetLineWidth(1)
# f.SetLineStyle(7)
# if dofit: gr.Fit(f, "N")

frame.Draw()
gr.Draw("P same")


# cmsheader_1 = ROOT.TLatex(0.15, 0.91, 'CMS')
# cmsheader_1.SetNDC(True)
# cmsheader_1.SetTextFont(62)
# cmsheader_1.SetTextSize(0.05)

# cmsheader_2 = ROOT.TLatex(0.27, 0.91, 'Phase-2 Simulation')
# cmsheader_2.SetNDC(True)
# cmsheader_2.SetTextFont(52)
# cmsheader_2.SetTextSize(0.05)

# cmsheader_1.Draw()
# cmsheader_2.Draw()

xtxt = 0.15
ytxt = 0.88 #0.91
textsize = 20

cmsheader_1 = ROOT.TLatex(xtxt, ytxt, 'CMS')
cmsheader_1.SetNDC(True)
cmsheader_1.SetTextFont(63)
cmsheader_1.SetTextSize(textsize)

cmsheader_2 = ROOT.TLatex(xtxt + 0.08, ytxt, 'Phase-2 Simulation')
cmsheader_2.SetNDC(True)
cmsheader_2.SetTextFont(53)
cmsheader_2.SetTextSize(textsize)

cmsheader_3 = ROOT.TLatex(0.9, ytxt, '14 TeV, 3000 fb^{-1}')
cmsheader_3.SetNDC(True)
cmsheader_3.SetTextFont(43)
cmsheader_3.SetTextAlign(31)
cmsheader_3.SetTextSize(textsize-2)

cmsheader_1.Draw()
cmsheader_2.Draw()
cmsheader_3.Draw()

if outfolder:
    oname = outfolder + '/' + oname
c1.Print(oname, 'pdf')
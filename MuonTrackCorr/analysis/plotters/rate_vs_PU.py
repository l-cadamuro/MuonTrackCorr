import ROOT
import collections
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

### TkMu
# PU_points[140] = ('../rate_EMTFpp_140PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
# PU_points[200] = ('../rate_EMTFpp_200PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
# PU_points[250] = ('../rate_EMTFpp_250PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
# oname = 'rate_vs_PU_TkMu.pdf'

### TkMuStub
PU_points[140] = ('../rate_EMTFpp_140PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
PU_points[200] = ('../rate_EMTFpp_200PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
PU_points[250] = ('../rate_EMTFpp_250PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
oname = 'rate_vs_PU_TkMuStub.pdf'

threshold = 20.0 # in GeV

##########################
## compute tot rate

orbitFreq    = 11.2456 # kHz
# nCollBunches = 1866
nCollBunches = 2748 #2808 is LHC Phase-1
khZconv      = 1 ### converts kHz to Hz : 1000 -> Hz, 1 -> kHz
scale        = khZconv * orbitFreq * nCollBunches
print "... rate scale is", scale

##########################

xmin = 0
xmax = 350

frame = ROOT.TH1D ('frame', ';PU;Rate [kHz]', 100, xmin, xmax)
frame.SetMinimum(0)
frame.SetMaximum(10)

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
setStyle(frame, c1)
# c1.SetLogy()

gr = ROOT.TGraphAsymmErrors()
rates = []
for PU, desc in PU_points.items():
    print '.... PU', PU, 'running on file', desc[0], 'histo name', desc[1]
    f = ROOT.TFile(desc[0])
    h = f.Get(desc[1])
    hpt = f.Get(desc[2])
    h.Scale(scale)
    b = h.FindBin(threshold)
    rate = h.GetBinContent(b)
    print PU, rate, h.GetBinContent(b-1), h.GetBinContent(b+1)
    rates.append(rate)
    err_rate = calc_rate_err(hpt, b, scale)
    # err_rate = h.GetBinError(b)
    # err_rate = 0.2
    gr.SetPoint(gr.GetN(), PU, rate)
    gr.SetPointError(gr.GetN()-1, 0, 0, err_rate[0]*rate, err_rate[1]*rate)
    # h.SetDirectory(0)
    # h.Draw('same')

gr.SetMarkerStyle(8)
gr.SetMarkerSize(0.8)
gr.SetMarkerColor(ROOT.kBlue)
gr.SetLineColor(ROOT.kBlue)

gr.Print()
# f = ROOT.TF1('lin', '[0]*x', 90, 300)
f = ROOT.TF1('lin', '[0]*x', xmin, xmax)
f.SetLineColor(ROOT.kGray)
f.SetLineWidth(1)
f.SetLineStyle(7)
gr.Fit(f)

frame.SetMaximum(1.15*max(rates))

frame.Draw()
f.Draw('same')
gr.Draw("P same")


cmsheader_1 = ROOT.TLatex(0.15, 0.91, 'CMS')
cmsheader_1.SetNDC(True)
cmsheader_1.SetTextFont(62)
cmsheader_1.SetTextSize(0.05)

cmsheader_2 = ROOT.TLatex(0.27, 0.91, 'Phase-2 Simulation')
cmsheader_2.SetNDC(True)
cmsheader_2.SetTextFont(52)
cmsheader_2.SetTextSize(0.05)

cmsheader_1.Draw()
cmsheader_2.Draw()




c1.Print(oname, 'pdf')

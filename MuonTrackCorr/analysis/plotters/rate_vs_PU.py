import ROOT
import sys
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

icfg = 0
if len(sys.argv) > 1:
    icfg = int(sys.argv[1])

### TkMu
if icfg == 0:
    PU_points[140] = ('../rate_EMTFpp_140PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
    PU_points[200] = ('../rate_EMTFpp_200PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
    PU_points[250] = ('../rate_EMTFpp_250PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
    PU_points[300] = ('../rate_EMTFpp_300PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
    dofit = False
    mcol = ROOT.kRed
    oname = 'TDR_plots/rate_vs_PU_TkMu.pdf'

### TkMuStub
if icfg == 1:
    PU_points[140] = ('../rate_EMTFpp_140PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
    PU_points[200] = ('../rate_EMTFpp_200PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
    PU_points[250] = ('../rate_EMTFpp_250PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
    PU_points[300] = ('../rate_EMTFpp_300PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
    mcol = ROOT.kGreen+2
    dofit = False
    oname = 'TDR_plots/rate_vs_PU_TkMuStub.pdf'

### EMTD
if icfg == 2:
    PU_points[140] = ('../rate_EMTFpp_140PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')
    PU_points[200] = ('../rate_EMTFpp_200PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')
    PU_points[250] = ('../rate_EMTFpp_250PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')
    PU_points[300] = ('../rate_EMTFpp_300PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')
    mcol = ROOT.kBlue
    dofit = False
    oname = 'TDR_plots/rate_vs_PU_EMTF.pdf'

### all together
if icfg == 3:
    MTFs  = ['EMTF',     'TkMuStub',           'TkMu']
    legs  = ['EMTF++',   'Track + muon stub',  'Track + muon']
    mcols = [ROOT.kBlue, ROOT.kGreen+2,        ROOT.kRed]
    
    PU_points_all = collections.OrderedDict()
    PU_points_all['EMTF']     = collections.OrderedDict()
    PU_points_all['TkMuStub'] = collections.OrderedDict()
    PU_points_all['TkMu']     = collections.OrderedDict()

    PU_points_all['EMTF'][140] = ('../rate_EMTFpp_140PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')
    PU_points_all['EMTF'][200] = ('../rate_EMTFpp_200PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')
    PU_points_all['EMTF'][250] = ('../rate_EMTFpp_250PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')
    PU_points_all['EMTF'][300] = ('../rate_EMTFpp_300PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')

    PU_points_all['TkMu'][140] = ('../rate_EMTFpp_140PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
    PU_points_all['TkMu'][200] = ('../rate_EMTFpp_200PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
    PU_points_all['TkMu'][250] = ('../rate_EMTFpp_250PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
    PU_points_all['TkMu'][300] = ('../rate_EMTFpp_300PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')

    PU_points_all['TkMuStub'][140] = ('../rate_EMTFpp_140PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
    PU_points_all['TkMuStub'][200] = ('../rate_EMTFpp_200PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
    PU_points_all['TkMuStub'][250] = ('../rate_EMTFpp_250PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
    PU_points_all['TkMuStub'][300] = ('../rate_EMTFpp_300PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')

    mcol = ROOT.kBlue
    dofit = False
    oname = 'TDR_plots/rate_vs_PU_allfinders.pdf'

### all together
if icfg == 4:
    MTFs  = ['EMTF',   'TkMu']
    legs  = ['EMTF++', 'Track + muon']
    mcols = [ROOT.kBlue, ROOT.kRed]
    
    PU_points_all = collections.OrderedDict()
    PU_points_all['EMTF']     = collections.OrderedDict()
    PU_points_all['TkMuStub'] = collections.OrderedDict()
    PU_points_all['TkMu']     = collections.OrderedDict()

    PU_points_all['EMTF'][140] = ('../rate_EMTFpp_140PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')
    PU_points_all['EMTF'][200] = ('../rate_EMTFpp_200PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')
    PU_points_all['EMTF'][250] = ('../rate_EMTFpp_250PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')
    PU_points_all['EMTF'][300] = ('../rate_EMTFpp_300PU.root', 'rate_EMTF_lead_mu_pt', 'EMTF_lead_mu_pt')

    PU_points_all['TkMu'][140] = ('../rate_EMTFpp_140PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
    PU_points_all['TkMu'][200] = ('../rate_EMTFpp_200PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
    PU_points_all['TkMu'][250] = ('../rate_EMTFpp_250PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')
    PU_points_all['TkMu'][300] = ('../rate_EMTFpp_300PU.root', 'rate_TPTkMu_lead_mu_pt', 'TPTkMu_lead_mu_pt')

    PU_points_all['TkMuStub'][140] = ('../rate_EMTFpp_140PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
    PU_points_all['TkMuStub'][200] = ('../rate_EMTFpp_200PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
    PU_points_all['TkMuStub'][250] = ('../rate_EMTFpp_250PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')
    PU_points_all['TkMuStub'][300] = ('../rate_EMTFpp_300PU.root', 'rate_TPTkMuStub_lead_mu_pt', 'TPTkMuStub_lead_mu_pt')

    mcol = ROOT.kBlue
    dofit = False
    oname = 'TDR_plots/rate_vs_PU_EMTF_TkMu.pdf'

######### mantra all detector
### all together
if icfg == 5:
    MTFs  = ['Mantra_barr', 'Mantra_ovrl', "Mantra_endc"]
    legs  = ['Mantra barrel', 'Mantra overlap', 'Mantra endcap']
    mcols = [ROOT.kRed, ROOT.kGreen+2, ROOT.kBlue]
    
    PU_points_all = collections.OrderedDict()
    PU_points_all['Mantra_barr']     = collections.OrderedDict()
    PU_points_all['Mantra_ovrl']     = collections.OrderedDict()
    PU_points_all['Mantra_endc']     = collections.OrderedDict()

    PU_points_all['Mantra_barr'][140] = ('../rate_alldetectors_140PU.root', 'rate_Mantra_TkMu_barr_lead_mu_pt', 'Mantra_TkMu_barr_lead_mu_pt')
    PU_points_all['Mantra_barr'][200] = ('../rate_alldetectors_200PU.root', 'rate_Mantra_TkMu_barr_lead_mu_pt', 'Mantra_TkMu_barr_lead_mu_pt')
    PU_points_all['Mantra_barr'][250] = ('../rate_alldetectors_250PU.root', 'rate_Mantra_TkMu_barr_lead_mu_pt', 'Mantra_TkMu_barr_lead_mu_pt')
    PU_points_all['Mantra_barr'][300] = ('../rate_alldetectors_300PU.root', 'rate_Mantra_TkMu_barr_lead_mu_pt', 'Mantra_TkMu_barr_lead_mu_pt')

    PU_points_all['Mantra_ovrl'][140] = ('../rate_alldetectors_140PU.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    PU_points_all['Mantra_ovrl'][200] = ('../rate_alldetectors_200PU.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    PU_points_all['Mantra_ovrl'][250] = ('../rate_alldetectors_250PU.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    PU_points_all['Mantra_ovrl'][300] = ('../rate_alldetectors_300PU.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')

    PU_points_all['Mantra_endc'][140] = ('../rate_alldetectors_140PU.root', 'rate_Mantra_TkMu_endc_lead_mu_pt', 'Mantra_TkMu_endc_lead_mu_pt')
    PU_points_all['Mantra_endc'][200] = ('../rate_alldetectors_200PU.root', 'rate_Mantra_TkMu_endc_lead_mu_pt', 'Mantra_TkMu_endc_lead_mu_pt')
    PU_points_all['Mantra_endc'][250] = ('../rate_alldetectors_250PU.root', 'rate_Mantra_TkMu_endc_lead_mu_pt', 'Mantra_TkMu_endc_lead_mu_pt')
    PU_points_all['Mantra_endc'][300] = ('../rate_alldetectors_300PU.root', 'rate_Mantra_TkMu_endc_lead_mu_pt', 'Mantra_TkMu_endc_lead_mu_pt')

    mcol = ROOT.kBlue
    dofit = False
    oname = 'TDR_plots/rate_vs_PU_Mantra.pdf'

### Mantra overlap - min dpt
if icfg == 6:
    PU_points[140] = ('../rate_alldetectors_140PU_mindpt.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    PU_points[200] = ('../rate_alldetectors_200PU_mindpt.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    PU_points[250] = ('../rate_alldetectors_250PU_mindpt.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    PU_points[300] = ('../rate_alldetectors_300PU_mindpt.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    mcol = ROOT.kGreen+1
    dofit = False
    oname = 'TDR_plots/rate_vs_PU_Mantra_Overlap_mindpt.pdf'
    frame_ymax = 11

### Mantra overlap - min dpt
if icfg == 7:
    PU_points[140] = ('../rate_alldetectors_140PU_maxpt.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    PU_points[200] = ('../rate_alldetectors_200PU_maxpt.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    PU_points[250] = ('../rate_alldetectors_250PU_maxpt.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    PU_points[300] = ('../rate_alldetectors_300PU_maxpt.root', 'rate_Mantra_TkMu_ovrl_lead_mu_pt', 'Mantra_TkMu_ovrl_lead_mu_pt')
    mcol = ROOT.kGreen+1
    dofit = False
    oname = 'TDR_plots/rate_vs_PU_Mantra_Overlap_maxpt.pdf'
    frame_ymax = 11


threshold = 20.0 # in GeV
etext = ROOT.TLatex(0.6, 0.2, "p_{T}^{#mu} > %.0f GeV" % threshold)
etext.SetNDC()
etext.SetTextFont(42)
etext.SetTextSize(0.05)

if len(sys.argv) > 2:
    threshold = float(sys.argv[2])
    oname = oname.replace('.pdf', '_thr%0f.pdf' % threshold)

#### summary

print " ... running on points : ", PU_points
print " ... threshold [GeV]   : ", threshold
print " ... output name       : ", oname

##########################
## compute tot rate

orbitFreq    = 11.246 ##11.2456 # kHz
# nCollBunches = 1866
nCollBunches = 2760 #2808 is LHC Phase-1
khZconv      = 1 ### converts kHz to Hz : 1000 -> Hz, 1 -> kHz
scale        = khZconv * orbitFreq * nCollBunches
print "... rate scale is", scale

##########################

xmin = 0
xmax = 400

frame = ROOT.TH1D ('frame', ';PU;Rate [kHz]', 100, xmin, xmax)
frame.SetMinimum(0)
frame.SetMaximum(10)

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
setStyle(frame, c1)
# c1.SetLogy()

### a single point
if len(PU_points) > 0:
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
    gr.SetMarkerSize(1.2)
    gr.SetMarkerColor(mcol)
    gr.SetLineColor(mcol)

    gr.Print()
    # f = ROOT.TF1('lin', '[0]*x', 90, 300)
    f = ROOT.TF1('lin', '[0]*x', xmin, xmax)
    f.SetLineColor(ROOT.kGray)
    f.SetLineWidth(1)
    f.SetLineStyle(7)
    if dofit: gr.Fit(f, "N")

    frame.SetMaximum(1.15*max(rates))
    try:
        frame_ymax
    except NameError:
        pass
    else:
        frame.SetMaximum(frame_ymax)

    frame.Draw()
    if dofit: f.Draw('same')
    gr.Draw("P same")

### multiple curves
else:
    mg = ROOT.TMultiGraph()
    graphs = []
    all_rates = []
    # for idx, (tkfinder, PU_points) in enumerate(PU_points_all.items()):

    #     if tkfinder not in MTFs:
    #         continue
    for idx, tkfinder in enumerate(MTFs):

        PU_points = PU_points_all[tkfinder]

        print '.... doing', tkfinder

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
        gr.SetMarkerSize(1.2)
        gr.SetMarkerColor(mcols[idx])
        gr.SetLineColor(mcols[idx])
        graphs.append(gr)
        mg.Add(gr)
        all_rates.append(rates)

    # gr.Print()
    # # f = ROOT.TF1('lin', '[0]*x', 90, 300)
    # f = ROOT.TF1('lin', '[0]*x', xmin, xmax)
    # f.SetLineColor(ROOT.kGray)
    # f.SetLineWidth(1)
    # f.SetLineStyle(7)
    # if dofit: gr.Fit(f, "N")

    maxs = [max(r) for r in all_rates]
    frame.SetMaximum(1.15*max(maxs))
    frame.SetMinimum(0)

    try:
        frame_ymax
    except NameError:
        pass
    else:
        frame.SetMaximum(frame_ymax)


    frame.Draw()
    if dofit: f.Draw('same')
    # mg.Draw("P same")
    for g in graphs:
        g.Draw('P same')

    leg = ROOT.TLegend(0.15, 0.65, 0.4, 0.88)
    for idx, tkfinder in enumerate(MTFs):
        leg.AddEntry(graphs[idx], legs[idx], 'pe')
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.045)
    leg.Draw()


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
ytxt = 0.91
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

etext.Draw()

c1.Print(oname, 'pdf')

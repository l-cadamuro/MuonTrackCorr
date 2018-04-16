import ROOT
import numpy
from array import array
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)

fIn = ROOT.TFile.Open('../plots_JFsynch_pt20_eta1p2_2p4_scaledPt_tree.root')
# fIn = ROOT.TFile.Open('../plots_JFsynch_pt20_eta1p2_2p4_scaledPt_singleMu_tree.root')
tIn = fIn.Get('tree')

# var_to_plot = 'gen_pt'
# xtitle = 'Gen #mu p_{t} [GeV]'

var_to_plot = 'gen_eta'
xtitle = 'Gen #mu |#eta|'


pt_to_cut = 'trk_pt'
# pt_to_cut = 'emtf_pt'
# pt_to_cut = 'emtf_xml_pt'
make_root = False

# binning = list(numpy.arange(start=0, stop=40, step = 0.2, dtype=float))
# binning += list(numpy.arange(start=40, stop=130, step = 1.0, dtype=float))
binning = list(numpy.linspace(start=1.2, stop=2.4, num = 100, dtype=float))
xmin = 1.1
xmax = 2.6

# frame = ROOT.TH1F('frame', ';Gen #mu p_{t} [GeV]; Efficiency', 1000, 0, 130)
frame = ROOT.TH1F('frame', ';%s; Efficiency' % xtitle, 1000, xmin, xmax)
thresholds = [0, 15, 30]
# thresholds = [0, 15, 20, 25, 30, 40]
# thresholds = [15, 16, 17, 18, 19, 20]
# colors = [ROOT.kRed, ROOT.kOrange+1, ROOT.kGreen+1, ROOT.kBlue, ROOT.kViolet, ROOT.kBlack]
colors = [ROOT.kGreen+3, ROOT.kGreen+2, ROOT.kGreen+1]

#####################################################

histos = []
for idx, th in enumerate(thresholds):
    # h = ROOT.TH1D('h_pass%i' % idx, '', 100, 0, 130)
    h = ROOT.TH1D('h_pass%i' % idx, '', len(binning)-1, array('d', binning))
    histos.append(h)
h_all = histos[0].Clone('h_all')

tIn.Draw('%s >> h_all' % var_to_plot)
for idx, th in enumerate(thresholds):
    tIn.Draw('%s >> h_pass%i' % (var_to_plot, idx) , '%s > %i' % (pt_to_cut, th))

##
turn_ons = []
for idx, h_pass in enumerate(histos):
    to = ROOT.TEfficiency(h_pass, h_all)
    if idx < len(colors):
        tcol = colors[idx]
    else:
        tcol = idx
    to.SetMarkerColor(tcol)
    to.SetLineColor(tcol)
    to.SetFillColor(tcol)
    to.SetLineStyle(1)
    to.SetMarkerStyle(8)
    to.SetMarkerSize(0.8)
    turn_ons.append(to)

c1.cd()
frame.Draw()
for idx, to in enumerate(turn_ons):
    to.Draw('psame')

leg = ROOT.TLegend(0.4, 0.15, 0.88, 0.45)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.04)
for idx, to in enumerate(turn_ons):
    leg.AddEntry(to, "p_{T} > %i GeV" % thresholds[idx], 'lp')
leg.Draw()

c1.Update()
c1.Print("comp_turnon.pdf", 'pdf')

if make_root:
    fOut = ROOT.TFile("comp_turnon.root", 'recreate')
    for idx, to in enumerate(turn_ons):
        to.SetName('turnon_%i_pt%i' % (idx, int(thresholds[idx])))
        to.Write()

import ROOT

def no_errs(h):
    for b in range(1, h.GetNbinsX()+1):
        h.SetBinError(b, 0)

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


#fIn = ROOT.TFile.Open('muon_trigger_rates_q99.root')
#fIn = ROOT.TFile.Open('muon_trigger_rates_preselTracks.root')
fIn = ROOT.TFile.Open('muon_trigger_rates_preselTracks_upd.root')
r_EMTF = fIn.Get('rate_EMTF_lead_mu_pt')
r_TPTkMu = fIn.Get('rate_TPTkMu_lead_mu_pt')
r_MyTPTkMu = fIn.Get('rate_MyTPTkMu_lead_mu_pt')
r_UpgTkMu = fIn.Get('rate_UpgTkMu_lead_mu_pt')

# plots = [
#     r_EMTF,
#     r_TPTkMu,
#     r_MyTPTkMu,
#     r_UpgTkMu,
# ]

plots = [
    r_EMTF,
    # r_TPTkMu,
    # r_MyTPTkMu,
    r_UpgTkMu,
]


legs = {
    r_EMTF     : 'EMTF standalone (all candidates)',
    r_TPTkMu   : 'TP correlator',
    r_MyTPTkMu : 'TP correlator (private impl.)',
    # r_UpgTkMu  : 'Upgrade correlator',
    # r_UpgTkMu  : 'p_{T}-dependent match',
    r_UpgTkMu  : 'Dynamic windows correlator',
}

xmin = 0.0
xmax = 60.0

# absScale = 1.0 ### scale y axis
absScale = 11.2455*1866

#####################
frame = ROOT.TH1D('frame', ';p_{T} threshold [GeV]; Rate reduction', 1000, xmin, xmax)
if absScale != 1:
    frame.GetYaxis().SetTitle("Rate [kHz]")
    print "... scalign to abs rate by", absScale
    for pl in plots:
        pl.Sumw2()
        pl.Scale(absScale)
        no_errs(pl)

mmaxs = [x.GetMaximum() for x in plots]
mmins = [x.GetMinimum() for x in plots]

frame.SetMaximum(10.*max(mmaxs)/2)
frame.SetMinimum(0.1*min(mmins)*2)
if frame.GetMinimum() == 0:
    frame.SetMinimum(1.e-5 * absScale)

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetLeftMargin(0.15)
c1.SetFrameLineWidth(3)
c1.SetLogy(True)

frame.Draw()
for pl in plots:
    pl.Draw('same')

leg = ROOT.TLegend(0.4, 0.6, 0.88, 0.88)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
for pl in plots:
    leg.AddEntry(pl, legs[pl], 'l')
leg.Draw()

c1.Update()
c1.Print('rate_plot.pdf', 'pdf')

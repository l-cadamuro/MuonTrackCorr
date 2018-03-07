import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

fIn = ROOT.TFile.Open('../test/TkMuNtuple.root')
tIn = fIn.Get('Ntuplizer/MuonTrackTree')

h_trks = ROOT.TH1D('h_trks', ';#eta;Events', 50, -3, 3)
h_mus  = ROOT.TH1D('h_mus', ';#eta;Events', 50, -3, 3)

for iEv in range(0, tIn.GetEntries()):
    tIn.GetEntry(iEv)
    
    for i in range(0, tIn.n_gen_mu):
        h_mus.Fill(tIn.gen_mu_eta.at(i))

    for i in range(0, tIn.n_L1TT_trk):
        h_trks.Fill(tIn.L1TT_trk_eta.at(i))

print 'Tree entries: ', tIn.GetEntries()
print 'h_trks.Integral() = ', h_trks.Integral()
print 'h_mus.Integral() = ', h_mus.Integral()

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)
c1.SetLeftMargin(0.13)

h_mus.SetLineColor(ROOT.kRed)

mmax = max((h_trks.GetMaximum(), h_mus.GetMaximum()))
h_trks.SetMaximum(1.15*mmax)
h_trks.Draw()
h_mus.Draw('same')

leg = ROOT.TLegend(0.12, 0.80, 0.88, 0.95)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.AddEntry(h_mus, "Generated muons", 'l')
leg.AddEntry(h_trks, "Reconstructed tracks", 'l')
leg.SetNColumns(2)
leg.SetTextFont(43)
leg.SetTextSize(20)
leg.Draw()

ttext = ROOT.TLatex(0.65, 0.92, "Single #mu - 0 PU")
ttext.SetNDC()
ttext.SetTextFont(43)
ttext.SetTextSize(22)
ttext.Draw()

c1.Update()
c1.Print('track_check.pdf', 'pdf')

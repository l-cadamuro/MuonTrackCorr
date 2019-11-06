import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def make_histogram(tIn, expr, cut, hname, bounds):
    hformat = 'h (%s)' % bounds
    tIn.Draw(expr + ' >> ' + hformat, cut) ## note: if using goff, I can't retrieve the histo
    myh = ROOT.gPad.GetPrimitive("h");
    out_h = myh.Clone(hname)
    out_h.SetDirectory(0)
    out_h.Sumw2()
    return out_h

toplot = ['PU0', 'PU200', 'PU300']

files = {
    'PU0'   : '../matchedTree_MuGun_PU0_EMTFpp.root',
    'PU200' : '../matchedTree_MuGun_PU200_EMTFpp.root',
    'PU300' : '../matchedTree_MuGun_PU300_EMTFpp.root',
}

colors = {
    'PU0'   : ROOT.kGreen+1,
    'PU200' : ROOT.kBlue,
    'PU300' : ROOT.kRed,
}

legentry = {
    'PU0'   : 'PU 0',
    'PU200' : 'PU 200',
    'PU300' : 'PU 300',
}

var = 'trk_chi2'
cut = 'trk_pt > 0'
title = "Single #mu gun;#chi^{2} tracks (endcap);a.u."
bounds = (300, 0, 300)

# oname = 'ZB_plots_vs_pt/chi_sq_vs_PU_singleMu.pdf'
# logy = False

oname = 'ZB_plots_vs_pt/chi_sq_vs_PU_singleMu_log.pdf'
logy = True

#######################

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)
c1.SetLogy(logy)

histos = {}
for tp in toplot:
    fIn = ROOT.TFile.Open(files[tp])
    tIn = fIn.Get('tree')
    h = make_histogram(tIn, var, cut, 'histo_%s' % tp, '{}, {}, {}'.format(*bounds))
    
    h.Scale(1./h.Integral())
    h.SetLineColor(colors[tp])
    h.SetMarkerColor(colors[tp])
    h.SetMarkerStyle(8)
    h.SetMarkerSize(0.5)

    histos[tp] = h
    fIn.Close()

frame = ROOT.TH1F('frame', title, *bounds)
frame.Draw()
mmaxs = [x.GetMaximum() for x in histos.values()]
frame.SetMaximum(1.15*max(mmaxs))

for tp in toplot:
    histos[tp].Draw('same')

leg = ROOT.TLegend(0.6, 0.6, 0.88, 0.88)
for tp in toplot:
    leg.AddEntry(histos[tp], legentry[tp], 'lp')
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

c1.Update()
c1.Print(oname, 'pdf')
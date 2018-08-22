import ROOT

def get_resol (tIn, gen_ptmin, gen_ptmax):
    hname = 'h_{:.3f}_{:.3f}'.format(gen_ptmin, gen_ptmax)
    h = ROOT.TH1D(hname, hname, 100, 0, 3)
    tIn.Draw('trk_pt / gen_pt >> %s' % hname, 'trk_pt > 0 && gen_pt > %f && gen_pt < %f' % (gen_ptmin, gen_ptmax))
    rms = h.GetRMS()
    erel = 1./ROOT.TMath.Sqrt(h.GetEntries()) if h.GetEntries() > 0 else 0
    err = erel * rms
    return (rms, erel)

def setStyle(frame, c1):
    c1.SetFrameLineWidth(3)
    c1.SetBottomMargin(0.13)
    c1.SetLeftMargin(0.15)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetLabelSize(0.045)

ROOT.gROOT.SetBatch(True)

# fIn = ROOT.TFile.Open('matched_tree_MuMu_flatPt_0PU_q99_relax0p5.root')
fIn = ROOT.TFile.Open('../matched_tree_MuMu_OneOverPt_0PU_forTrkRes.root')
tIn = fIn.Get('tree')

bins = [2, 3, 5, 7, 10, 15, 20, 30, 50, 100, 200, 500, 2000]

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetLogx(True)
c1.SetLogy(True)
gr = ROOT.TGraphAsymmErrors()
for i in range(len(bins)-1):
    ptlow = bins[i]
    pthigh = bins[i+1]
    rms, err = get_resol(tIn, ptlow, pthigh)
    gr.SetPoint(i, 0.5*(pthigh+ptlow), rms)
    gr.SetPointError(i, 0.5*(pthigh-ptlow), 0.5*(pthigh-ptlow), err, err)

gr.Draw('ap')
gr.SetTitle('; p_{T}^{gen} [GeV];p_{T} resolution')
setStyle(gr, c1)
gr.Draw('ap')

c1.Update()
c1.Print('trk_resol.pdf', 'pdf')
# raw_input()
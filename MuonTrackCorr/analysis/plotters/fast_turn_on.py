import ROOT
ROOT.gROOT.SetBatch(True)

def make_histogram(tIn, expr, cut, hname, bounds, sumw2=False):
    hformat = 'h (%s)' % bounds
    tIn.Draw(expr + ' >> ' + hformat, cut) ## note: if using goff, I can't retrieve the histo
    myh = ROOT.gPad.GetPrimitive("h");
    out_h = myh.Clone(hname)
    out_h.SetDirectory(0)
    if sumw2: out_h.Sumw2()
    return out_h

def make_eff(tIn, expr, cut, cutpass, bounds, eff_name):
    cpass = '(' + cut + ') && ' + cutpass if cut.strip() else cutpass
    # print 'cut:', cut
    # print 'cpass:', cpass
    hAll  = make_histogram(tIn, expr, cut   , eff_name + '_all',  bounds)
    hPass = make_histogram(tIn, expr, cpass , eff_name + '_pass', bounds)
    # print eff_name, hPass.Integral()
    oeff = ROOT.TEfficiency(hPass,hAll)
    oeff.SetName(eff_name)
    return oeff

def setStyle(frame, c1):
    c1.SetFrameLineWidth(3)
    c1.SetBottomMargin(0.13)
    c1.SetLeftMargin(0.13)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetLabelSize(0.045)

fIn = ROOT.TFile.Open('../matchedTree_MuGun_PU0_alldetector.root')
tIn = fIn.Get('tree')

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)

# expr    = 'gen_pt'
# bounds  = '100, 0, 100'
# presel  = 'TMath::Abs(gen_eta) > 0.8 && TMath::Abs(gen_eta) < 1.2 &&  gen_pt > 0'
# cutpass = 'tkmu_mantra_ovrl_pt > 0'

# expr    = 'TMath::Abs(gen_eta)'
# bounds  = '50, 0.6, 1.4'
# presel  = 'gen_pt > 25'
# cutpass = 'tkmu_mantra_ovrl_pt > 20'

expr    = 'TMath::Abs(gen_eta)'
bounds  = '100, 0.0, 3'
presel  = 'gen_pt > 25'
cutpass = 'tkmu_mantra_endc_pt > 20'


# expr    = 'TMath::Abs(gen_eta)'
# bounds  = '100, 0, 3'
# presel  = 'gen_pt > 20 && abs(gen_eta) > 0 && abs(gen_eta) < 3'
# cutpass = 'tkmu_mantra_ovrl_pt > 20'

# expr    = 'TMath::Abs(gen_eta)'
# bounds  = '100, 0.5, 1.5'
# presel  = 'gen_pt > 25 && TMath::Abs(gen_eta) > 0.8 &&  TMath::Abs(gen_eta) < 1.2'
# cutpass = 'ovrlap_pt > 25'


effplot = make_eff(tIn = tIn, expr = expr, cut = presel, cutpass = cutpass, bounds = bounds, eff_name = 'eff')

effplot.Draw()
c1.Print('eff_plot.pdf', 'pdf')

import ROOT
import argparse


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

def makeAllEffs (tIn, threshold, x_var, nbins, xmin, xmax, tag, presel=''):

    eff_emtf          = make_eff(tIn, x_var, presel, 'emtf_pt > %f'    % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_emtf_%s' % tag)
    eff_trk           = make_eff(tIn, x_var, presel, 'trk_pt > %f'     % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_trk_%s' % tag)
    eff_tkmu          = make_eff(tIn, x_var, presel, 'tkmu_pt > %f'    % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_tkmu_%s' % tag)
    eff_upgtkmu       = make_eff(tIn, x_var, presel, 'upgtkmu_pt > %f' % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_upgtkmu_%s' % tag)
    eff_myimpltkmu    = make_eff(tIn, x_var, presel, 'myimpltkmu_pt > %f' % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_myimpltkmu_%s' % tag)
    eff_tkmustub      = make_eff(tIn, x_var, presel, 'tkmustub_pt > %f'   % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_tkmustub_%s' % tag)
    ##
    eff_mantra_tkmu_barr = make_eff(tIn, x_var, presel, 'tkmu_mantra_barr_pt > %f'   % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_mantra_tkmu_barr_%s' % tag)
    eff_mantra_tkmu_ovrl = make_eff(tIn, x_var, presel, 'tkmu_mantra_ovrl_pt > %f'   % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_mantra_tkmu_ovrl_%s' % tag)
    eff_mantra_tkmu_endc = make_eff(tIn, x_var, presel, 'tkmu_mantra_endc_pt > %f'   % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_mantra_tkmu_endc_%s' % tag)
    ##
    eff_standalone_barr = make_eff(tIn, x_var, presel, 'barrel_pt > %f' % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_standalone_barr_%s' % tag)
    eff_standalone_ovrl = make_eff(tIn, x_var, presel, 'ovrlap_pt > %f' % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_standalone_ovrl_%s' % tag)
    eff_standalone_endc = make_eff(tIn, x_var, presel, 'emtf_pt > %f'   % float(threshold),  '%i, %f, %f' % (nbins, xmin, xmax), 'eff_standalone_endc_%s' % tag)

    eff_emtf.SetLineColor(ROOT.kRed)
    eff_trk.SetLineColor(ROOT.kGreen+1)
    eff_tkmu.SetLineColor(ROOT.kBlue)
    eff_upgtkmu.SetLineColor(ROOT.kBlack)
    eff_myimpltkmu.SetLineColor(ROOT.kCyan)
    eff_tkmustub.SetLineColor(ROOT.kGreen+2)
    
    eff_mantra_tkmu_barr.SetLineColor(ROOT.kRed)
    eff_mantra_tkmu_ovrl.SetLineColor(ROOT.kGreen+2)
    eff_mantra_tkmu_endc.SetLineColor(ROOT.kBlue)

    eff_standalone_barr.SetLineColor(ROOT.kOrange)
    eff_standalone_ovrl.SetLineColor(ROOT.kGreen)
    eff_standalone_endc.SetLineColor(ROOT.kAzure)

    return [eff_emtf, eff_trk, eff_tkmu, eff_upgtkmu, eff_myimpltkmu, eff_tkmustub,
        eff_mantra_tkmu_barr, eff_mantra_tkmu_ovrl, eff_mantra_tkmu_endc, eff_standalone_barr, eff_standalone_ovrl, eff_standalone_endc]

parser = argparse.ArgumentParser(description='Command line parser of plotting options')
#string opts
parser.add_argument('--input',  dest='input',  help='input file', required=True)
parser.add_argument('--output', dest='output', help='output file', required=True)
# parser.add_argument('--quit',   dest='quit',   help = 'quit at the end of the script, no interactive window', action='store_true', default=False)

args = parser.parse_args()

# if args.quit:
#     ROOT.gROOT.SetOptBatch(True)
ROOT.gROOT.SetBatch(True)

fIn = ROOT.TFile.Open(args.input)
tIn = fIn.Get('tree')

fOut = ROOT.TFile.Open(args.output, 'recreate')
print "... running on file:", fIn.GetName(), ', output is', fOut.GetName()

ROOT.gStyle.SetOptStat(0)
c1 = ROOT.TCanvas('c1', 'c1', 600, 600)

####### pt plots
effs = []

# effs += makeAllEffs(tIn, threshold=20, x_var='gen_pt', nbins=25, xmin=0, xmax=200, tag="vspt_ptgt20")
# effs += makeAllEffs(tIn, threshold=0,  x_var='gen_pt', nbins=25, xmin=0, xmax=200, tag="vspt_ptgt0")
# effs += makeAllEffs(tIn, threshold=20, x_var='gen_pt', nbins=100, xmin=0, xmax=200, tag="vspt_ptgt20")
# effs += makeAllEffs(tIn, threshold=0,  x_var='gen_pt', nbins=100, xmin=0, xmax=200, tag="vspt_ptgt0")
effs += makeAllEffs(tIn, threshold=0,  x_var='gen_pt', nbins=100, xmin=0, xmax=100, tag="vspt_ptgt0",  presel="gen_pt > 0   && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
effs += makeAllEffs(tIn, threshold=5,  x_var='gen_pt', nbins=100, xmin=0, xmax=100, tag="vspt_ptgt5",  presel="gen_pt > 0   && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
effs += makeAllEffs(tIn, threshold=20, x_var='gen_pt', nbins=100, xmin=0, xmax=100, tag="vspt_ptgt20", presel="gen_pt > 0   && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
#####
effs += makeAllEffs(tIn, threshold=0,  x_var='gen_eta', nbins=100, xmin=-3, xmax=3, tag="vseta_ptgt0",  presel="gen_pt > 0   && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
effs += makeAllEffs(tIn, threshold=5,  x_var='gen_eta', nbins=100, xmin=-3, xmax=3, tag="vseta_ptgt5",  presel="gen_pt > 5   && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
effs += makeAllEffs(tIn, threshold=20, x_var='gen_eta', nbins=100, xmin=-3, xmax=3, tag="vseta_ptgt20", presel="gen_pt > 20  && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
####
effs += makeAllEffs(tIn, threshold=0,  x_var='TMath::Abs(gen_eta)', nbins=100, xmin=1.0, xmax=3, tag="vsabseta_ptgt0",  presel="gen_pt > 0  && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
effs += makeAllEffs(tIn, threshold=5,  x_var='TMath::Abs(gen_eta)', nbins=100, xmin=1.0, xmax=3, tag="vsabseta_ptgt5",  presel="gen_pt > 5  && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
effs += makeAllEffs(tIn, threshold=20, x_var='TMath::Abs(gen_eta)', nbins=100, xmin=1.0, xmax=3, tag="vsabseta_ptgt20", presel="gen_pt > 20 && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
#### special
# effs += makeAllEffs(tIn, threshold=5, x_var='gen_eta',             nbins=100, xmin=-3,  xmax=3, tag="vseta_pt5to20",    presel = "gen_pt > 5 && gen_pt < 20 && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
effs += makeAllEffs(tIn, threshold=5, x_var='TMath::Abs(gen_eta)', nbins=100, xmin=1.0, xmax=3, tag="vsabseta_pt5to20", presel = "gen_pt > 5 && gen_pt < 20 && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")
# effs += makeAllEffs(tIn, threshold=20, x_var='gen_eta', nbins=50, xmin=-3, xmax=3, tag="vseta_ptgt20_gmugt10", presel = 'gen_pt > 10')
# effs += makeAllEffs(tIn, threshold=0,  x_var='gen_eta', nbins=50, xmin=-3, xmax=3, tag="vseta_ptgt0_gmugt5", presel = 'gen_pt > 5 && abs(gen_eta) > 1.3 && abs(gen_eta) < 2.3')
# effs += makeAllEffs(tIn, threshold=0,  x_var='gen_eta', nbins=50, xmin=-3, xmax=3, tag="vseta_ptgt0_gmugt10", presel = 'gen_pt > 10 && abs(gen_eta) > 1.3 && abs(gen_eta) < 2.3')
# effs += makeAllEffs(tIn, threshold=0,  x_var='gen_eta', nbins=50, xmin=-3, xmax=3, tag="vseta_ptgt0_gmugt20", presel = 'gen_pt > 20 && abs(gen_eta) > 1.3 && abs(gen_eta) < 2.3')


##### for the 3 regions
effs += makeAllEffs(tIn, threshold=20, x_var='TMath::Abs(gen_eta)', nbins=100, xmin=0, xmax=3, tag="vsabseta_ptgt20_all", presel = "gen_pt > 25 && abs(gen_eta) < 3")
effs += makeAllEffs(tIn, threshold=0,  x_var='TMath::Abs(gen_eta)', nbins=100, xmin=0, xmax=3, tag="vsabseta_ptgt0_all",  presel = "gen_pt > 0  && abs(gen_eta) < 3")

effs += makeAllEffs(tIn, threshold=20, x_var='gen_eta', nbins=200, xmin=-3, xmax=3, tag="vseta_ptgt20_all", presel = "gen_pt > 25 && abs(gen_eta) < 3")
effs += makeAllEffs(tIn, threshold=0,  x_var='gen_eta', nbins=200, xmin=-3, xmax=3, tag="vseta_ptgt0_all",  presel = "gen_pt > 0  && abs(gen_eta) < 3")

effs += makeAllEffs(tIn, threshold=0,  x_var='gen_pt', nbins=100, xmin=0, xmax=100, tag="vspt_ptgt0_eta0to0p8",    presel = "gen_pt > 0 && abs(gen_eta) < 0.8")
effs += makeAllEffs(tIn, threshold=0,  x_var='gen_pt', nbins=100, xmin=0, xmax=100, tag="vspt_ptgt0_eta0p8to1p2",  presel = "gen_pt > 0 && abs(gen_eta) > 0.8 && abs(gen_eta) < 1.2")
effs += makeAllEffs(tIn, threshold=0,  x_var='gen_pt', nbins=100, xmin=0, xmax=100, tag="vspt_ptgt0_eta1p2to2p4",  presel = "gen_pt > 0 && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")

effs += makeAllEffs(tIn, threshold=20, x_var='gen_pt', nbins=100, xmin=0, xmax=100, tag="vspt_ptgt20_eta0to0p8",   presel = "gen_pt > 0 && abs(gen_eta) < 0.8")
effs += makeAllEffs(tIn, threshold=20, x_var='gen_pt', nbins=100, xmin=0, xmax=100, tag="vspt_ptgt20_eta0p8to1p2", presel = "gen_pt > 0 && abs(gen_eta) > 0.8 && abs(gen_eta) < 1.2")
effs += makeAllEffs(tIn, threshold=20, x_var='gen_pt', nbins=100, xmin=0, xmax=100, tag="vspt_ptgt20_eta1p2to2p4", presel = "gen_pt > 0 && abs(gen_eta) > 1.2 && abs(gen_eta) < 2.4")

fOut.cd()
for e in effs:
    e.Write()
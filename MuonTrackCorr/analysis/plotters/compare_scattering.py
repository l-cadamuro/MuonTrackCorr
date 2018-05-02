import ROOT
import argparse
import numpy as np
import copy
import scipy, sys

def make_histogram(tIn, expr, cut, hbounds, hname, xscale=None, xshift=None):
    hformat = 'h (%s)' % hbounds
    if xscale: expr = str(xscale) + ' * (%s)' % expr
    if xshift: expr = str(xshift) + ' + (%s)' % expr
    print expr, "      ,      ", cut
    tIn.Draw(expr + ' >> ' + hformat, cut)
    myh = ROOT.gPad.GetPrimitive("h");
    # print 'prim ' , myh
    out_h = myh.Clone(hname)
    out_h.SetDirectory(0)
    return out_h

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

####################################

parser = argparse.ArgumentParser(description='Command line parser of plotting options')
parser.add_argument('--cut',   dest='cut', help='cut', default=None)
parser.add_argument('--xmin',  dest='xmin', help='xmin', type=float, default=0)
parser.add_argument('--xmax',  dest='xmax', help='xmax', type=float, default=1.5)
parser.add_argument('--nbins', dest='nbins', help='nbins', type=int, default=100)
parser.add_argument('--title', dest='title', help='title', default=';|#varphi_{hit} - #varphi_{gen}|;a.u.')
parser.add_argument('--oname', dest='oname', help='oname', default='scattering.pdf')
parser.add_argument('--shift-to-avg', dest='shifttoavg', help='shift events to average', default=False, action='store_true')
parser.add_argument('--input',  dest='input', help='input file', default=None)
parser.add_argument('--dtheta', dest='dtheta', help='plot dtheta instead of dphi', default=False, action='store_true')
# parser.add_argument('--no-abs', dest='abs', help='plot abs values', default=True, action='store_false')

args = parser.parse_args()

####################################

# fIn = ROOT.TFile.Open('../matched_tree_MuMu_OneOverPt_0PU_23Apr2018.root')
fIn = ROOT.TFile.Open(args.input)
tIn = fIn.Get("tree")

####################################


cut  = 'emtf_pt > 0 && {}_type == 1' ## CSC only
if args.cut: cut = (cut + ' && (%s)' % args.cut)
print cut
if not args.dtheta:
    # if args.abs:
    #     expr = 'abs(TVector2::Phi_mpi_pi({}_phi - gen_phi))' # to format with station name -- note the need to put difference in -pi, pi
    # else:
    #     expr = 'TVector2::Phi_mpi_pi({}_phi - gen_phi)' # to format with station name -- note the need to put difference in -pi, pi
    expr = 'TVector2::Phi_mpi_pi(gen_charge*({}_phi - gen_phi))' # to format with station name -- note the need to put difference in -pi, pi
else:
    # if args.abs:
    #     expr = 'abs({}_theta - gen_theta)'
    # else:
    #     expr = 'gen_charge * ({}_theta - gen_theta)'
     expr = '(gen_eta / abs(gen_eta)) * ({}_theta - gen_theta)'
     # expr = '{}_theta - gen_theta'
print expr
hbounds = "%i, %f, %f" % (args.nbins, args.xmin, args.xmax)
title = args.title
oname = args.oname
if args.shifttoavg:
    oname = oname.replace('.pdf', '_shifted.pdf')

####################################

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)

if not args.shifttoavg:
    h_S1 = make_histogram(tIn, expr.format("S1"), cut.format("S1") + " && has_S1", hbounds, 'hscat_S1')
    h_S2 = make_histogram(tIn, expr.format("S2"), cut.format("S2") + " && has_S2", hbounds, 'hscat_S2')
    h_S3 = make_histogram(tIn, expr.format("S3"), cut.format("S3") + " && has_S3", hbounds, 'hscat_S3')
    h_S4 = make_histogram(tIn, expr.format("S4"), cut.format("S4") + " && has_S4", hbounds, 'hscat_S4')

else:
    ## first determine average for each
    ##### copy the data to memory. This is super fast, excellent!!
    nevents = tIn.GetEntries()
    tIn.SetEstimate(nevents + 1);
    avgs = [0,0,0,0]
    for idx in range(4):
        print '... making averages', idx+1
        thecut = cut.format("S%i" % (idx+1)) + " && has_S%i" % (idx+1)
        print thecut
        tIn.Draw(expr.format("S%i") % (idx+1), thecut, "goff",nevents,0)
        temp = tIn.GetV1()
        nselected = tIn.GetEntries(thecut)
        print nselected
        data_buf = copy.deepcopy(scipy.frombuffer(buffer=temp,dtype='double',count=nselected))
        data     = np.asarray(data_buf)
        # print data
        # print min(data), max(data)
        avgs[idx] = np.average(data)
        print " >> avg " , avgs[idx]

    h_S1 = make_histogram(tIn, expr.format("S1"), cut.format("S1") + " && has_S1", hbounds, 'hscat_S1', xshift = -1. * avgs[0]) ## to be centred at 0
    h_S2 = make_histogram(tIn, expr.format("S2"), cut.format("S2") + " && has_S2", hbounds, 'hscat_S2', xshift = -1. * avgs[1]) ## to be centred at 0
    h_S3 = make_histogram(tIn, expr.format("S3"), cut.format("S3") + " && has_S3", hbounds, 'hscat_S3', xshift = -1. * avgs[2]) ## to be centred at 0
    h_S4 = make_histogram(tIn, expr.format("S4"), cut.format("S4") + " && has_S4", hbounds, 'hscat_S4', xshift = -1. * avgs[3]) ## to be centred at 0


print 'h_S1 : entries = ', h_S1.GetEntries(), ' avg = ', h_S1.GetMean()
print 'h_S2 : entries = ', h_S2.GetEntries(), ' avg = ', h_S2.GetMean()
print 'h_S3 : entries = ', h_S3.GetEntries(), ' avg = ', h_S3.GetMean()
print 'h_S4 : entries = ', h_S4.GetEntries(), ' avg = ', h_S4.GetMean()

h_S1.Scale(1./h_S1.Integral())
h_S2.Scale(1./h_S2.Integral())
h_S3.Scale(1./h_S3.Integral())
h_S4.Scale(1./h_S4.Integral())

h_S1.SetLineColor(ROOT.kRed)
h_S2.SetLineColor(ROOT.kBlue)
h_S3.SetLineColor(ROOT.kGreen+1)
h_S4.SetLineColor(ROOT.kBlack)

h_S1.SetMarkerColor(h_S1.GetLineColor())
h_S2.SetMarkerColor(h_S2.GetLineColor())
h_S3.SetMarkerColor(h_S3.GetLineColor())
h_S4.SetMarkerColor(h_S4.GetLineColor())

h_S1.SetMarkerStyle(8)
h_S2.SetMarkerStyle(8)
h_S3.SetMarkerStyle(8)
h_S4.SetMarkerStyle(8)

h_S1.SetMarkerSize(0.8)
h_S2.SetMarkerSize(0.8)
h_S3.SetMarkerSize(0.8)
h_S4.SetMarkerSize(0.8)

mmax = max(h_S1.GetMaximum(), h_S2.GetMaximum(), h_S3.GetMaximum(), h_S4.GetMaximum())
h_S1.SetMaximum(1.15*mmax)
h_S1.SetMinimum(0)

h_S1.SetTitle(title)
h_S1.Draw('lp')
h_S2.Draw('lp same')
h_S3.Draw('lp same')
h_S4.Draw('lp same')

leg = ROOT.TLegend(0.65, 0.65, 0.88, 0.88)
leg.AddEntry(h_S1, 'S1', 'lep')
leg.AddEntry(h_S2, 'S2', 'lep')
leg.AddEntry(h_S3, 'S3', 'lep')
leg.AddEntry(h_S4, 'S4', 'lep')
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

c1.Update()
c1.Print(oname, 'pdf')
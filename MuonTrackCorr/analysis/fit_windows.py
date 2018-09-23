import ROOT
import sys
import argparse

def buildLatexs(fitfunc, xstart, ystart, xoffset, yoffset, txtfont=42, txtsize=0.04, txtcolor=ROOT.kBlack):
    ### add parameters values
    txt = []
    for ip in range(0, fitfunc.GetNpar()):
        pname = fitfunc.GetParName(ip)
        pval  = fitfunc.GetParameter(ip)
        perr  = fitfunc.GetParError(ip)
        testo = '{:<4} = {:0.3e} #pm {:0.1e}'.format(pname, pval, perr)
        # print "...", pname, pval, perr
        txt .append(testo)
    latexs = []
    for idx, linea in enumerate(txt):
        ttext = ROOT.TLatex(xstart + idx*xoffset, ystart + idx*yoffset, linea)
        ttext.SetNDC(True)
        ttext.SetTextFont(txtfont)
        ttext.SetTextColor(txtcolor)
        ttext.SetTextSize(txtsize)
        latexs.append(ttext)
    return latexs

ROOT.gStyle.SetOptStat(0)

fIn = ROOT.TFile('matching_windows.root')


# dofit   = True
# rootOut = 'window_fits.root'## or set to none

xtitle = 'track p_{T} [GeV]'

### fixme: can replce with an argparse
# if len(sys.argv) > 1:
#     binN = int(sys.argv[1])  
# if len(sys.argv) > 2:
#     rootOut = sys.argv[2]
#     if rootOut == 'None': rootOut = None
# if len(sys.argv) > 3:
#     dofit = False if int(sys.argv[3]) == 0 else True
# if len(sys.argv) > 4:
#     plotType = int(sys.argv[4])
# if len(sys.argv) > 5:
#     quantile = int(sys.argv[5])

parser = argparse.ArgumentParser(description='Command line parser of plotting options')
parser.add_argument('--binN',    dest='binN',      help='bin number',  type=int, default=1)
parser.add_argument('--rootOut', dest='rootOut',   help='root output (can use None to disable)', default='window_fits.root')
parser.add_argument('--noFit',   dest='doFit',     help='do fit', default=True, action='store_false')
parser.add_argument('--plotType', dest='plotType',     help='plot type', type=int, default=0)
parser.add_argument('--quantile', dest='quantile', help='quantile', type=int, default=None)
parser.add_argument('--interactive',  dest='silent',     help='make interactive', default=True, action='store_false')
args = parser.parse_args()

silent  = args.silent
if silent:
    ROOT.gROOT.SetBatch(True)


print args

dofit   = args.doFit
rootOut = args.rootOut
if rootOut == 'None': rootOut = None
if not dofit and rootOut:
    rootOut = None
binN = args.binN
plotType = args.plotType
quantile = args.quantile

print 'dofit    : ', dofit   
print 'rootOut  : ', rootOut 
print 'binN     : ', binN
print 'plotType : ', plotType
print 'quantile : ', quantile
### write your default here

plotName  = 'h_dphi'
ytitle    = '#Delta #varphi [rad]'
ytitle_wd = '#Delta#varphi^{max} - #Delta#varphi^{min} [rad]'

if plotType == 0:
    plotName = 'h_dphi'
    ytitle = '#Delta #varphi [rad]'
    ytitle_wd = '#Delta#varphi^{max} - #Delta#varphi^{min} [rad]'

elif plotType == 1:
    plotName = 'h_dtheta'
    ytitle = '#Delta #theta [rad]'
    ytitle_wd = '#Delta#theta^{max} - #Delta#theta^{min} [rad]'

elif plotType == 2:
    plotName = 'h_deta'
    ytitle = '#Delta #eta [rad]'
    ytitle_wd = '#Delta#eta^{max} - #Delta#eta^{min} [rad]'

elif plotType == 3:
    plotName = 'h_dR'
    ytitle = '#Delta R [rad]'
    ytitle_wd = '#DeltaR^{max} - #DeltaR^{min} [rad]'


print "... using bin", binN

if dofit:
    func_doublepow = ROOT.TF1("func_doublepow", '[0] + [1]*TMath::Power(x,[2]) + [3]*TMath::Power(x,[4])')
    func_doublepow.SetParameters(0, 1, -1, 1, -1)
    func_doublepow.SetParLimits(0, -1, 10)
    func_doublepow.SetParLimits(1, 0, 10)
    func_doublepow.SetParLimits(2, -1.3, -0.8)
    func_doublepow.SetParLimits(3, 0, 10)
    func_doublepow.SetParLimits(4, -1.3, -0.8)
    func_doublepow.SetParNames("Const", "A1", "B1", "A2", "B2")


    func_monopow = ROOT.TF1("func_monopow", '[0] + [1]*TMath::Power(x,[2])')
    # func_monopow.SetParameters(0, 1, -1)
    # func_monopow.SetParLimits(0, -1, 10)
    # func_monopow.SetParLimits(1, 0, 10)
    # func_monopow.SetParLimits(2, -1.3, -0.8)
    # func_monopow.SetParNames("Const", "A", "B")

    func_monopow.SetParameters(0.01, 1.3, -2.0)
    func_monopow.SetParLimits(0, -1, 10)
    func_monopow.SetParLimits(1, 0, 10)
    func_monopow.SetParLimits(2, -10, -0.8)
    func_monopow.SetParNames("Const", "A", "B")

    

    ##########################################

    # fitfunc_l = func_doublepow
    # fitfunc_h = func_monopow

    fitfunc_l = fitfunc_c = fitfunc_h = func_monopow

    print '... fitting lower quantile with function: ', fitfunc_l.GetName(), ' --> ', fitfunc_l.GetTitle()
    print '... fitting lower quantile with function: ', fitfunc_h.GetName(), ' --> ', fitfunc_h.GetTitle()

c1 = ROOT.TCanvas("c1", "c1", 600, 600)
c1.SetLogx()
c1.SetLogy()
c1.SetFrameLineWidth(3)
c1.SetBottomMargin(0.15)
c1.SetLeftMargin(0.18)

if not quantile:
    p_l = fIn.Get(plotName + '_l')
    p_c = fIn.Get(plotName + '_c')
    p_h = fIn.Get(plotName + '_h')
else:
    p_l = fIn.Get(plotName + '_l' + str(quantile))
    p_c = fIn.Get(plotName + '_c') ### this is always the same
    p_h = fIn.Get(plotName + '_h' + str(quantile))    

eta_min = p_l.GetYaxis().GetBinLowEdge(binN)
eta_max = p_l.GetYaxis().GetBinLowEdge(binN+1)

p_l.SetLineColor(ROOT.kBlue+1)
p_c.SetLineColor(ROOT.kBlack)
p_h.SetLineColor(ROOT.kGreen+2)

h_l = p_l.ProjectionX('h_l_' + str(binN), binN, binN)
h_c = p_c.ProjectionX('h_c_' + str(binN), binN, binN)
h_h = p_h.ProjectionX('h_h_' + str(binN), binN, binN)

# gr_window_wh = ROOT.TGraph()
# gr_window_wl = ROOT.TGraph()
# gr_window_wh.SetName('gr_window_wh_' + str(binN))
# gr_window_wl.SetName('gr_window_wl_' + str(binN))
gr_window_w = ROOT.TGraph()
gr_window_w.SetName('gr_window_w_' + str(binN))
nsampling = 1000

if dofit:
    h_l.Fit(fitfunc_l, 'WL 0') ### low edge looks better (esp in theta) by using a likelihood fit
    of_l = fitfunc_l.Clone('fit_low_' + str(binN))
    h_c.Fit(fitfunc_c, '0')
    of_c = fitfunc_c.Clone('fit_cent_' + str(binN))
    h_h.Fit(fitfunc_h, '0')
    of_h = fitfunc_h.Clone('fit_high_' + str(binN))

    #### plot the width of the windows
    for i in range(0, nsampling):
        xmin = h_h.GetBinLowEdge(1)
        xmax = h_h.GetBinLowEdge(h_h.GetNbinsX()+1)
        step = (xmax-xmin)/nsampling
        xp = xmin + i*step
        yph = of_h.Eval(xp)
        ypl = of_l.Eval(xp)
        deltay = yph-ypl
        # gr_window_wh.SetPoint(i, xp, 0.5*deltay)
        # gr_window_wl.SetPoint(i, xp, -0.5*deltay)
        gr_window_w.SetPoint(i, xp, deltay)

of_l.SetLineColor(ROOT.kBlue)
of_c.SetLineColor(ROOT.kGray+1)
of_h.SetLineColor(ROOT.kGreen+1)
of_l.SetLineWidth(3)
of_c.SetLineWidth(3)
of_h.SetLineWidth(3)
of_l.SetLineStyle(1)
of_c.SetLineStyle(1)
of_h.SetLineStyle(1)

h_h.SetTitle('#eta bin [%.2f, %.2f];%s;%s' % (eta_min, eta_max, xtitle, ytitle))
h_h.GetXaxis().SetTitleOffset(1.2)
h_h.GetYaxis().SetTitleOffset(1.2)

mmax = max(h_h.GetMaximum(), h_l.GetMaximum())
mmin = min(h_h.GetMinimum(), h_l.GetMinimum())

# print mmin, mmax

h_h.SetMaximum(5.*mmax)
h_h.SetMinimum(0.5*mmin)

of_l.SetRange(h_h.GetBinLowEdge(0), h_h.GetBinLowEdge(h_h.GetNbinsX()+1))
of_c.SetRange(h_h.GetBinLowEdge(0), h_h.GetBinLowEdge(h_h.GetNbinsX()+1))
of_h.SetRange(h_h.GetBinLowEdge(0), h_h.GetBinLowEdge(h_h.GetNbinsX()+1))

h_h.Draw()
h_c.Draw('same')
h_l.Draw('same')
of_l.Draw('l same')
of_c.Draw('l same')
of_h.Draw('l same')

if dofit:
    lat_h = buildLatexs(fitfunc=of_h, xstart = 0.52, ystart = 0.86, xoffset = 0.0, yoffset = -0.04, txtsize = 0.03, txtcolor = h_h.GetLineColor())
    lat_l = buildLatexs(fitfunc=of_l, xstart = 0.52, ystart = 0.71, xoffset = 0.0, yoffset = -0.04, txtsize = 0.03, txtcolor = h_l.GetLineColor())

    for l in lat_h: l.Draw()
    for l in lat_l: l.Draw()


c1.Update()
if not silent: raw_input()
oname = 'corr_fits/fit_%s_%i.pdf' % (plotName, binN) if not quantile else 'corr_fits/fit_%s_%i_q%i.pdf' % (plotName, binN, quantile)
c1.Print(oname, 'pdf')

# c1.SetLogy(False)
gr_window_w.Draw('apl')
ax = gr_window_w.GetXaxis()
ay = gr_window_w.GetYaxis()

ymin = ay.GetXmin()
ymax = ay.GetXmax()
# ymin = gr_window_w.GetHistogram().GetMinimum()
# ymax = gr_window_w.GetHistogram().GetMaximum()

xmin = ax.GetXmin()
xmax = ax.GetXmax()

### ROOT e un programma di merda e tocca fare questa roba per avere un asse a dx
# frame = ROOT.TH1D('frame', '', 1000, xmin, xmax)
# frame.SetMinimum(ymin)
# frame.SetMaximum(ymax)
# frame.SetTitle(';%s;%s' % (xtitle, ytitle_wd))
# frame.GetXaxis().SetTitleOffset(1.4)
# frame.GetYaxis().SetTitleOffset(1.4)


### draw an axis in degrees on the right
# raxis = ROOT.TGaxis(ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax(), ymin,ymax,510,"+L");
# uymin = ROOT.gPad.GetUymin() if c1.GetLogy() else 10**ROOT.gPad.GetUymin()
# uymax = ROOT.gPad.GetUymax() if c1.GetLogy() else 10**ROOT.gPad.GetUymax()

# uxmin = ROOT.gPad.GetUxmin() if c1.GetLogy() else 10**ROOT.gPad.GetUxmin()
# uxmax = ROOT.gPad.GetUxmax() if c1.GetLogy() else 10**ROOT.gPad.GetUxmax()

# raxis = ROOT.TGaxis(uxmax, uymin, uxmax, uymax, ymin,ymax,510,"+LG");
# frame.Draw()
# gr_window_w.Draw('plsame')

gr_window_w.SetTitle(';%s;%s' % (xtitle, ytitle_wd))
gr_window_w.GetXaxis().SetTitleOffset(1.4)
gr_window_w.GetYaxis().SetTitleOffset(2.5)
gr_window_w.GetXaxis().SetMoreLogLabels(True)
gr_window_w.GetYaxis().SetMoreLogLabels(True)
gr_window_w.Draw('apl')
# raxis.Draw()


# gr_window_wh.Draw('apl')
# gr_window_wl.Draw('plsame')
c1.Update()
if not silent: raw_input()
oname = 'corr_fits/window_size_%s_%i.pdf' % (plotName, binN) if not quantile else 'corr_fits/window_size_%s_%i_q%i.pdf' % (plotName, binN, quantile)
c1.Print(oname, 'pdf')

if rootOut:
    fOut = ROOT.TFile.Open(rootOut, 'update') ## or set to none
    fOut.cd()
    of_l.Write()
    of_c.Write()
    of_h.Write()
    gr_window_w.Write()
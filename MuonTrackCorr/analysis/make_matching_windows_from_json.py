import ROOT
import json
import collections
import numpy as np 
import decimal
from array import array

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def make_plot(var, quantile, iy):

    histo = ROOT.TH1F('h_%s_%.4f_%i' % (var, quantile, iy), '', len(binningx)-1, array('d', binningx))
    for ix in range(0, len(binningx)-1):
        qkey = str(quantile) # because json indexes as str
        datafield = mw[var][qkey]
        key = str((ix,iy))
        if key in datafield:
            nev = datafield[key]['nev']
            if nev > 0:
                histo.SetBinContent (ix+1, iy+1, datafield[key]['val'])
                histo.SetBinError   (ix+1, iy+1, 1./np.sqrt(nev))
    return histo

### open the json with the results

region = 'barrel' ## barrel, overlap, endcap
jsonname   = 'matching_windows_%s.json' % region
output_dir = 'matching_windows_%s' % region

print "... running on json file :", jsonname
print "... saving results in    :", output_dir

with open(jsonname, 'r') as read_file:
    read_dicts = json.loads(read_file.read(), object_pairs_hook=collections.OrderedDict)
    print '... the file contains', len(read_dicts), 'dictionaries, will use first of the list'
    mw = read_dicts[0]

binningx = mw['binningx']
binningy = mw['binningy']

# vars_to_plot = mw['variables']
vars_to_plot = ['delta_phicharge', 'delta_thetaendc', 'pt_resol']
outfile_phi   = ROOT.TFile('%s/matching_windows_phi_q99.root' % output_dir, 'recreate')
outfile_theta = ROOT.TFile('%s/matching_windows_theta_q99.root' % output_dir, 'recreate')
outfile_bounds = ROOT.TFile('%s/matching_windows_boundaries.root' % output_dir, 'recreate')

# quantiles    = [0.005, 0.5, 0.995]

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetLogx()
# # c1.SetLogy()

for iy in range(len(binningy)-1):
    for var in vars_to_plot:
        h_h  = make_plot(var,   0.995, iy)
        h_c  = make_plot(var,   0.5,   iy)
        h_l  = make_plot(var,   0.005, iy)

        h_h.SetLineColor(ROOT.kGreen+1)
        h_c.SetLineColor(ROOT.kGray)
        h_l.SetLineColor(ROOT.kBlue)
       
        h_h.SetMarkerColor(ROOT.kGreen+1)
        h_c.SetMarkerColor(ROOT.kGray)
        h_l.SetMarkerColor(ROOT.kBlue)

        h_h.SetMarkerStyle(8)
        h_c.SetMarkerStyle(8)
        h_l.SetMarkerStyle(8)

        h_h.SetMarkerSize(0.8)
        h_c.SetMarkerSize(0.8)
        h_l.SetMarkerSize(0.8)

        ## fits
        dofit_phi   = False
        dofit_theta = False
        if var == 'delta_phicharge':
            dofit_phi = True
        if var == 'delta_thetaendc':
            dofit_theta = True


        if dofit_phi:
            print '... fitting bin', iy, 'var', var
            fitfunc_h = ROOT.TF1('fit_high_' + str(iy+1), '[0] + [1]*TMath::Power(x,[2])', 2, 100) # start counting from 1 to be backward-compatible  
            fitfunc_c = ROOT.TF1('fit_cent_' + str(iy+1), '[0] + [1]*TMath::Power(x,[2])', 2, 100)
            fitfunc_l = ROOT.TF1('fit_low_'  + str(iy+1), '[0] + [1]*TMath::Power(x,[2])', 2, 100)

            fitfunc_h.SetLineColor(ROOT.kGreen+1)
            fitfunc_c.SetLineColor(ROOT.kGray)
            fitfunc_l.SetLineColor(ROOT.kBlue)

            h_h.Fit('fit_high_' + str(iy+1), 'W0')
            h_c.Fit('fit_cent_' + str(iy+1), 'W0')
            h_l.Fit('fit_low_'  + str(iy+1), 'W0')

        if dofit_theta:
            if region == 'endcap':
                print '... fitting bin', iy, 'var', var
                fitfunc_h = ROOT.TF1('fit_high_' + str(iy+1), '[0] + [1]*TMath::Power(x,[2])', 2, 100) # start counting from 1 to be backward-compatible  
                fitfunc_c = ROOT.TF1('fit_cent_' + str(iy+1), '[0] + [1]*TMath::Power(x,[2])', 2, 100)
                fitfunc_l = ROOT.TF1('fit_low_'  + str(iy+1), '[0] + [1]*TMath::Power(x,[2])', 2, 100)

                fitfunc_h.SetLineColor(ROOT.kGreen+1)
                fitfunc_c.SetLineColor(ROOT.kGray)
                fitfunc_l.SetLineColor(ROOT.kBlue)

                h_h.Fit('fit_high_' + str(iy+1), 'W0')
                h_c.Fit('fit_cent_' + str(iy+1), 'W0')
                h_l.Fit('fit_low_'  + str(iy+1), 'W0')

            else: ## in barrel and overlap just a simple constant
                print '... constant for theta in', iy, 'var', var
                fitfunc_h = ROOT.TF1('fit_high_' + str(iy+1), '[0]', 1, 100) # start counting from 1 to be backward-compatible  
                fitfunc_c = ROOT.TF1('fit_cent_' + str(iy+1), '[0]', 1, 100)
                fitfunc_l = ROOT.TF1('fit_low_'  + str(iy+1), '[0]', 1, 100)

                fitfunc_h.SetParameter(0, 0.2)
                fitfunc_c.SetParameter(0, 0.0)
                fitfunc_l.SetParameter(0, -0.2)

                fitfunc_h.SetLineColor(ROOT.kGreen+1)
                fitfunc_c.SetLineColor(ROOT.kGray)
                fitfunc_l.SetLineColor(ROOT.kBlue)


        frame = ROOT.TH1F('frame_%s_%i' % (var, iy), '%s bin %i;p_{T} [GeV]; value' % (var, iy), 100, 2, 100)
        mmins = [h_l.GetMinimum(), h_c.GetMinimum(), h_h.GetMinimum()]
        mmaxs = [h_l.GetMaximum(), h_c.GetMaximum(), h_h.GetMaximum()]
        mmin = min(mmins)
        mmax = max(mmaxs)

        # if mmin > 0 : mmin = mmin/10.
        # else        : mmin = mmin * 10.

        # if mmax > 0 : mmax = mmax/10.
        # else        : mmax = mmax * 10.

        frame.SetMinimum(mmin)
        frame.SetMaximum(mmax)

        frame.Draw()
        h_h.Draw('pe same')
        h_c.Draw('pe same')
        h_l.Draw('pe same')

        if dofit_phi:
            fitfunc_h.Draw('same')
            fitfunc_c.Draw('same')
            fitfunc_l.Draw('same')
            outfile_phi.cd()
            fitfunc_h.Write()
            fitfunc_c.Write()
            fitfunc_l.Write()

        if dofit_theta:
            fitfunc_h.Draw('same')
            fitfunc_c.Draw('same')
            fitfunc_l.Draw('same')
            outfile_theta.cd()
            fitfunc_h.Write()
            fitfunc_c.Write()
            fitfunc_l.Write()

        # h_l.Draw('pe')
        c1.Print('%s/%s_bin%i.pdf' % (output_dir, var, iy), 'pdf')

        ### now make a plot with the matching windows only - to cross check them
        if dofit_phi:
            pre_logx = c1.GetLogx()
            pre_logy = c1.GetLogy()
            c1.SetLogx(True)
            c1.SetLogy(True)

            fitfunc_h.Draw()
            fitfunc_c.Draw('same')
            fitfunc_l.Draw('same')

            c1.Print('%s/fit_%s_bin%i.pdf' % (output_dir, var, iy), 'pdf')

            # reset values
            c1.SetLogx(pre_logx)
            c1.SetLogy(pre_logy)

        if dofit_theta:
            pre_logx = c1.GetLogx()
            pre_logy = c1.GetLogy()
            c1.SetLogx(True)
            c1.SetLogy(False)

            fitfunc_h.Draw()
            fitfunc_c.Draw('same')
            fitfunc_l.Draw('same')

            c1.Print('%s/fit_%s_bin%i.pdf' % (output_dir, var, iy), 'pdf')

            # reset values
            c1.SetLogx(pre_logx)
            c1.SetLogy(pre_logy)



#####################################
### finally, make the boundaries file for the correlator
### NB: it's a fake histo just for the name, keep the name for compatibility to CMSSW

histo_boundaries = ROOT.TH2D('h_dphi_l', 'Boundaries for correlator;p_{T} track;|#eta| track',
    len(binningx)-1, array('d', binningx), len(binningy)-1, array('d', binningy))

## fill with something just ot highlihgt binning
for ix in range(1, len(binningx)):
    for iy in range(1, len(binningy)):
        histo_boundaries.SetBinContent(ix, iy, iy)

outfile_bounds.cd()
histo_boundaries.Write()



        # margin = 0.2

        # frame.SetMinimum( (1 - margin*(mmin/abs(mmin) * ) ) )
        # frame.SetMaximum(max(mmaxs))
# # var      = 'delta_phicharge'
# var      = 'delta_phi'
# quantile = 0.995
# iy       = 1 ## as an array, counting starts from 0

# h_delta_phi        = make_plot('delta_phi',       quantile, iy)
# h_delta_phicharge  = make_plot('delta_phicharge', quantile, iy)
# h_delta_phicharge.SetLineColor(ROOT.kRed)
# h_delta_phicharge.Scale(-1.0)

# c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
# c1.SetLogx()
# # c1.SetLogy()
# h_delta_phi.Draw()
# h_delta_phicharge.Draw('same')
# # h_delta_phicharge.Draw()
# c1.Update()
# # raw_input()
# c1.Print('mw.pdf', 'pdf')

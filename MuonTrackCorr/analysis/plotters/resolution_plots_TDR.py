import ROOT
import collections
import sys

def redrawBorder(c1):
    # this little macro redraws the axis tick marks and the pad border lines.
    ROOT.gPad.Update();
    ROOT.gPad.RedrawAxis();
    l = ROOT.TLine ()
    l.SetLineWidth(c1.GetFrameLineWidth())
    l.DrawLine(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymax(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax());
    l.DrawLine(ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax());


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# fIn = ROOT.TFile.Open('../matched_tree_MuMu_flatPt_0PU_noSF.root')
# print "tree has", tIn.GetEntries(), "entries"

fIn_flatPt = ROOT.TFile.Open('../matchedTree_MuGun_PU200_EMTFpp.root')
tIn_flatPt = fIn_flatPt.Get('tree')

# fIn_oneOverPt = ROOT.TFile.Open('../matchedTree_MuGun_PU0_EMTFpp.root') ### temp FIX: unused
# tIn_oneOverPt = fIn_oneOverPt.Get('tree')

# print tIn_flatPt.GetEntries(), tIn_oneOverPt.GetEntries()
print tIn_flatPt.GetEntries()

fit = 'gaus' ## funcname or none

####
# pt_var = 'trk_pt'
pt_var = 'gen_pt'

icfg = 0

if len(sys.argv) > 1:
    icfg = int(sys.argv[1])

if icfg == 0:
    expr   = 'gen_charge * TVector2::Phi_mpi_pi(trk_phi - gen_phi)'
    title  = ';q^{gen} #times (#varphi^{trk} - #varphi^{gen}) [rad];a.u.'
    exist_cut = 'trk_pt > 0'
    gen_var_cut = 'gen_charge'
    gen_var_title = 'q^{gen}'
    nbins = 75
    xmin = -0.009
    xmax = 0.009
    draw_cumul = True
    oname = 'TDR_plots/dphi_trk.pdf'

if icfg == 1:
    expr   = 'trk_theta - gen_theta'
    title  = ';#theta^{trk} - #theta^{gen} [rad];a.u.'
    exist_cut = 'trk_pt > 0'
    gen_var_cut = 'gen_charge'
    gen_var_title = 'q^{gen}'
    nbins = 75
    xmin = -0.009
    xmax = 0.009
    draw_cumul = True
    oname = 'TDR_plots/dtheta_trk.pdf'

if icfg == 2:
    expr   = 'gen_charge * TVector2::Phi_mpi_pi(emtf_phi - gen_phi)'
    title  = ';q^{gen} #times (#varphi^{EMTF++} - #varphi^{gen}) [rad];a.u.'
    exist_cut = 'emtf_pt > 0'
    gen_var_cut = 'gen_charge'
    gen_var_title = 'q^{gen}'
    nbins = 200
    xmin = -1.5
    xmax = 1.5
    draw_cumul = True
    oname = 'TDR_plots/dphi_EMTF.pdf'

if icfg == 3:
    expr   = 'emtf_theta - gen_theta'
    title  = ';#theta^{EMTF++} - #theta^{gen} [rad];a.u.'
    exist_cut = 'emtf_pt > 0'
    gen_var_cut = 'gen_charge'
    gen_var_title = 'q^{gen}'
    nbins = 200
    xmin = -0.15
    xmax = 0.15
    draw_cumul = True
    oname = 'TDR_plots/dtheta_EMTF.pdf'

if icfg == 4:
    expr   = '(emtf_theta/TMath::Abs(emtf_theta)) * (emtf_theta - gen_theta)'
    title  = ';endcap sign #times (#theta^{EMTF++} - #theta^{gen}) [rad];a.u.'
    exist_cut = 'emtf_pt > 0'
    gen_var_cut = 'gen_charge'
    gen_var_title = 'q^{gen}'
    nbins = 200
    xmin = -0.15
    xmax = 0.15
    draw_cumul = True
    oname = 'TDR_plots/dtheta_times_endcapsign_EMTF.pdf'


# if icfg == 4:
#     expr   = 'emtf_theta - gen_theta'
#     title  = ';#theta^{EMTF++} - #theta^{gen} [rad];a.u.'
#     exist_cut = 'emtf_pt > 0'
#     gen_var_cut = 'gen_eta'
#     gen_var_title = '#eta^{gen}'
#     nbins = 200
#     xmin = -0.15
#     xmax = 0.15
#     draw_cumul = True

# if icfg == 5:
#     expr   = 'emtf_pt / gen_pt'
#     title  = ';p_{T}^{EMTF++} / p_{T}^{gen} [GeV];a.u.'
#     exist_cut = 'emtf_pt > 0'
#     gen_var_cut = 'gen_eta'
#     gen_var_title = '#eta^{gen}'
#     nbins = 100
#     xmin = 0
#     xmax = 3
#     draw_cumul = True

# if icfg == 6:
#     expr   = 'trk_pt / gen_pt'
#     title  = ';p_{T}^{trk} / p_{T}^{gen} [GeV];a.u.'
#     exist_cut = 'trk_pt > 0'
#     gen_var_cut = 'gen_eta'
#     gen_var_title = '#eta^{gen}'
#     nbins = 100
#     xmin = 0.8
#     xmax = 1.2
#     draw_cumul = True

print "... expr : ", expr
print "... title : ", title
print "... oname : ", oname


ROOT.TGaxis.SetMaxDigits(3)


########
# ranges = [
#     (2,3),
#     (2,5),
#     (3,5),
#     (5,10),
#     (10,20),
# ]

# ranges_flatPt = [
#     # (10,20),
# ]

# ranges_oneOverPt = [
#     (2,3),
#     # (2,5),
#     (3,5),
#     (5,10),
#     (10,20),
# ]

ranges_flatPt = [
    (2,5),
    (5,10),
    (10,20),
]

ranges_oneOverPt = [
]

ranges = ranges_flatPt + ranges_oneOverPt


# colors = {
#     (2,3) : ROOT.kRed+1,
#     (3,5) : ROOT.kOrange+1,
#     (5,10) : ROOT.kGreen+1,
#     (10,20) : ROOT.kBlue,
# }

colors = {
    (10,20) : ROOT.kRed+1,
    # (5,10) : ROOT.kOrange+1,
    (5,10) : ROOT.kBlue,
    # (3,5) : ROOT.kGreen+1,
    (2,5) : ROOT.kGreen+2,
}



###
histos = collections.OrderedDict()

for r in ranges:
    histos['h_qp_{}_{}'.format(r[0], r[1])] = ROOT.TH1D('h_qp_{}_{}'.format(r[0], r[1]), '', nbins, xmin, xmax)
    histos['h_qn_{}_{}'.format(r[0], r[1])] = ROOT.TH1D('h_qn_{}_{}'.format(r[0], r[1]), '', nbins, xmin, xmax)
    histos['h_qall_{}_{}'.format(r[0], r[1])] = ROOT.TH1D('h_qall_{}_{}'.format(r[0], r[1]), '', nbins, xmin, xmax)

frame = ROOT.TH1D('frame', title, nbins, xmin, xmax)
# for r in ranges:
#     tIn.Draw(expr + ' >> h_qp_{}_{}'.format(r[0], r[1])   , '{0} > {1} && {0} < {2}   && gen_charge > 0'.format(pt_var, r[0], r[1]))
#     tIn.Draw(expr + ' >> h_qn_{}_{}'.format(r[0], r[1])   , '{0} > {1} && {0} < {2}   && gen_charge < 0'.format(pt_var, r[0], r[1]))
for r in ranges_flatPt:
    tIn_flatPt.Draw(expr + ' >> h_qp_{}_{}'.format(r[0], r[1])   , '{0} > {1} && {0} < {2}   && {3} && {4} > 0'.format(pt_var, r[0], r[1], exist_cut, gen_var_cut))
    tIn_flatPt.Draw(expr + ' >> h_qn_{}_{}'.format(r[0], r[1])   , '{0} > {1} && {0} < {2}   && {3} && {4} < 0'.format(pt_var, r[0], r[1], exist_cut, gen_var_cut))
    tIn_flatPt.Draw(expr + ' >> h_qall_{}_{}'.format(r[0], r[1])   , '{0} > {1} && {0} < {2}   && {3}'.format(pt_var, r[0], r[1], exist_cut))

# for r in ranges_oneOverPt:
#     tIn_oneOverPt.Draw(expr + ' >> h_qp_{}_{}'.format(r[0], r[1])   , '{0} > {1} && {0} < {2} && {3} && {4} > 0'.format(pt_var, r[0], r[1], exist_cut, gen_var_cut))
#     tIn_oneOverPt.Draw(expr + ' >> h_qn_{}_{}'.format(r[0], r[1])   , '{0} > {1} && {0} < {2} && {3} && {4} < 0'.format(pt_var, r[0], r[1], exist_cut, gen_var_cut))
#     tIn_oneOverPt.Draw(expr + ' >> h_qall_{}_{}'.format(r[0], r[1])   , '{0} > {1} && {0} < {2} && {3}'.format(pt_var, r[0], r[1], exist_cut))


# histos['h_qp_2_3'   ] = ROOT.TH1D('h_qp_2_3', '', nbins, xmin, xmax)
# histos['h_qp_3_5'   ] = ROOT.TH1D('h_qp_3_5', '', nbins, xmin, xmax)
# histos['h_qp_5_10'  ] = ROOT.TH1D('h_qp_5_10', '', nbins, xmin, xmax)
# histos['h_qp_10_20' ] = ROOT.TH1D('h_qp_10_20', '', nbins, xmin, xmax)
# ###
# histos['h_qn_2_3'   ] = ROOT.TH1D('h_qn_2_3', '', nbins, xmin, xmax)
# histos['h_qn_3_5'   ] = ROOT.TH1D('h_qn_3_5', '', nbins, xmin, xmax)
# histos['h_qn_5_10'  ] = ROOT.TH1D('h_qn_5_10', '', nbins, xmin, xmax)
# histos['h_qn_10_20' ] = ROOT.TH1D('h_qn_10_20', '', nbins, xmin, xmax)

# tIn.Draw(expr + ' >> h_qp_2_3'   , '{0} > 2 && {0} < 3   && gen_charge > 0'.format(pt_var))
# tIn.Draw(expr + ' >> h_qp_3_5'   , '{0} > 3 && {0} < 5   && gen_charge > 0'.format(pt_var))
# tIn.Draw(expr + ' >> h_qp_5_10'  , '{0} > 5 && {0} < 10  && gen_charge > 0'.format(pt_var))
# tIn.Draw(expr + ' >> h_qp_10_20' , '{0} > 10 && {0} < 20 && gen_charge > 0'.format(pt_var))

# tIn.Draw(expr + ' >> h_qn_2_3'   , '{0} > 2 && {0} < 3   && gen_charge < 0'.format(pt_var))
# tIn.Draw(expr + ' >> h_qn_3_5'   , '{0} > 3 && {0} < 5   && gen_charge < 0'.format(pt_var))
# tIn.Draw(expr + ' >> h_qn_5_10'  , '{0} > 5 && {0} < 10  && gen_charge < 0'.format(pt_var))
# tIn.Draw(expr + ' >> h_qn_10_20' , '{0} > 10 && {0} < 20 && gen_charge < 0'.format(pt_var))

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)
c1.SetLeftMargin(0.15)
c1.SetBottomMargin(0.15)

for h in histos.values():
    if h.Integral() == 0:
        print h.GetName(), ' has integral of 0'
        continue
    print h.GetName(), '-->', h.Integral(), '(', h.Integral(-1,-1), ')'
    h.Scale(1./h.Integral())

mmaxs = [h.GetMaximum() for h in histos.values()]
frame.SetMaximum(1.15*max(mmaxs))
frame.GetXaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleSize(0.05)
frame.GetXaxis().SetTitleOffset(1.1)
frame.GetYaxis().SetTitleOffset(1.5)


frame.Draw()
# for idx, h in enumerate(histos.values()):
for idx, r in enumerate(ranges):
    if not draw_cumul:
        for sign in ['qp', 'qn']:        
            h = histos['h_{}_{}_{}'.format(sign, r[0], r[1])]
            col = colors[r] if r in colors else idx+1
            h.SetLineColor(col)
            h.SetLineWidth(2)
            h.SetMarkerColor(col)
            h.SetMarkerStyle(8)
            h.SetMarkerSize(0.8)
            if sign == 'qp':
                h.Draw('hist same')
            else:
                h.SetFillColor(col) ### for the legend after
                h.Draw('pl same')
    else:
        h = histos['h_{}_{}_{}'.format('qall', r[0], r[1])]
        col = colors[r] if r in colors else idx+1
        h.SetLineColor(col)
        h.SetLineWidth(3)
        h.SetMarkerColor(col)
        # h.SetFillColor(col) ### for the legend after
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.8)
        # h.Draw('pl same')
        h.Draw('hist same')

# histos['h_qp_2_5'].Draw('hist same')
# histos['h_qn_2_5'].Draw('pl same')

# histos['h_qp_10_20'].Draw('hist same')
# histos['h_qn_10_20'].Draw('pl same')

leg = ROOT.TLegend(0.6, 0.4, 0.88, 0.88)
for r in ranges:
    if not draw_cumul:
        h = histos['h_qn_{}_{}'.format(r[0], r[1])]
    else:
        h = histos['h_qall_{}_{}'.format(r[0], r[1])]
    
    if not draw_cumul:
        leg.AddEntry(h, '{} < p_{{T}}^{{#mu}} < {} GeV'.format(r[0], r[1]), 'f')
    else:
        leg.AddEntry(h, '{} < p_{{T}}^{{#mu}} < {} GeV'.format(r[0], r[1]), 'l')

leg.AddEntry(None, '', '')
fake_pos = histos['h_qp_{}_{}'.format(ranges[0][0], ranges[0][1])].Clone('fake_pos')
fake_neg = histos['h_qn_{}_{}'.format(ranges[0][0], ranges[0][1])].Clone('fake_neg')

fake_pos.SetLineColor(ROOT.kGray+1)
fake_neg.SetLineColor(ROOT.kGray+1)
fake_pos.SetMarkerColor(ROOT.kGray+1)
fake_neg.SetMarkerColor(ROOT.kGray+1)

if not draw_cumul:
    leg.AddEntry(fake_pos, '%s > 0' % gen_var_title, 'l')
    leg.AddEntry(fake_pos, '%s < 0' % gen_var_title, 'pe')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

xtxt = 0.15
ytxt = 0.91
textsize = 20

cmsheader_1 = ROOT.TLatex(xtxt, ytxt, 'CMS')
cmsheader_1.SetNDC(True)
cmsheader_1.SetTextFont(63)
cmsheader_1.SetTextSize(textsize)

cmsheader_2 = ROOT.TLatex(xtxt + 0.08, ytxt, 'Phase-2 Simulation')
cmsheader_2.SetNDC(True)
cmsheader_2.SetTextFont(53)
cmsheader_2.SetTextSize(textsize)

# cmsheader_3 = ROOT.TLatex(0.9, ytxt, '14 TeV, 3000 fb^{-1}, 200 PU')
cmsheader_3 = ROOT.TLatex(0.9, ytxt, '14 TeV, 200 PU')
cmsheader_3.SetNDC(True)
cmsheader_3.SetTextFont(43)
cmsheader_3.SetTextAlign(31)
cmsheader_3.SetTextSize(textsize-2)

cmsheader_1.Draw()
cmsheader_2.Draw()
cmsheader_3.Draw()

redrawBorder(c1)

c1.Print(oname, 'pdf')
import ROOT
import importlib
import sys

def setStyle(frame, c1):
    c1.SetFrameLineWidth(3)
    c1.SetBottomMargin(0.13)
    c1.SetLeftMargin(0.13)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetLabelSize(0.045)
    frame.GetYaxis().SetLabelSize(0.045)

###############################################################

if len(sys.argv) < 2:
    print "Usage: python draw_eff_plots.py cfgName outName"
cfg = sys.argv[1]
out = sys.argv[2]

# execfile('eff_plots_cfgs/turnon_PU0_pt0.py')
# execfile('eff_plots_cfgs/turnon_PU0_pt20.py')
# execfile('eff_plots_cfgs/turnon_PU200_pt0.py')
# execfile('eff_plots_cfgs/turnon_PU200_pt20.py')
# execfile('eff_plots_cfgs/eta_PU0_pt0.py')
# execfile('eff_plots_cfgs/eta_PU0_pt20.py')
# execfile('eff_plots_cfgs/eta_PU200_pt0.py')
# execfile('eff_plots_cfgs/eta_PU200_pt20.py')
execfile(cfg)

##############################


ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)
c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
setStyle(frame, c1)

frame.Draw()

openFiles = {}
leg = ROOT.TLegend(*leg_coords)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
for idx, entry in enumerate(inputs):
    fname = entry['file']
    if not fname in openFiles:
        openFiles[fname] = ROOT.TFile.Open(fname)
    ep = openFiles[fname].Get(entry['name'])
    col = entry['color'] if 'color' in entry else idx+1
    ep.SetLineColor(col)
    ep.SetMarkerColor(col)
    ep.SetMarkerStyle(8)
    ep.SetMarkerSize(0.8)
    ep.Draw('pe same')
    lname = entry['legend'] if 'legend' in entry else entry['name']
    leg.AddEntry(ep, lname, 'lep')

leg.Draw()

if testo:
    tt = ROOT.TLatex(0.88, 0.92, testo)
    tt.SetNDC(True)
    tt.SetTextAlign(31)
    tt.SetTextFont(43)
    tt.SetTextSize(21)
    tt.Draw()

try:
    cms_header
except NameError:
    pass
else:
    if cms_header:
        # cmsheader_1 = ROOT.TLatex(0.15, 0.91, 'CMS')
        # cmsheader_1.SetNDC(True)
        # cmsheader_1.SetTextFont(62)
        # cmsheader_1.SetTextSize(0.05)
        
        # cmsheader_2 = ROOT.TLatex(0.27, 0.91, 'Phase-2 Simulation')
        # cmsheader_2.SetNDC(True)
        # cmsheader_2.SetTextFont(52)
        # cmsheader_2.SetTextSize(0.05)

        # cmsheader_1.Draw()
        # cmsheader_2.Draw()

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

        cmsheader_3 = ROOT.TLatex(0.9, ytxt, '14 TeV, 3000 fb^{-1}, 200 PU')
        cmsheader_3.SetNDC(True)
        cmsheader_3.SetTextFont(43)
        cmsheader_3.SetTextAlign(31)
        cmsheader_3.SetTextSize(textsize-2)

        cmsheader_1.Draw()
        cmsheader_2.Draw()
        cmsheader_3.Draw()


c1.Update()
c1.Print(out, 'pdf')

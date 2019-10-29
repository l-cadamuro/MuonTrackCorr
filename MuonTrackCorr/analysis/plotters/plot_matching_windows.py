import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# def split_canvas(c1):
#     nx = 3
#     ny = 2
#     top_m    = 0.1
#     bottom_m = 0.1
#     left_m   = 0.1
#     right_m  = 0.1

fIn_phi   = ROOT.TFile.Open('/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/data-L1Trigger-L1TMuon/V01-01-04/L1Trigger/L1TMuon/data/emtf_luts/matching_windows_phi_q99.root')
fIn_theta = ROOT.TFile.Open('/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/data-L1Trigger-L1TMuon/V01-01-04/L1Trigger/L1TMuon/data/emtf_luts/matching_windows_theta_q99.root')

files   = [fIn_phi, fIn_theta]

xmin = 0
xmax = 200

## [phi, theta]
ymins = [2e-4, 2e-6]
ymaxs = [8, 0.8]
ytitles = ['#Delta#varphi [rad]', '#Delta#theta [rad]']

### eta boundaries:
# 1  1.2  1.32
# 2  1.32 1.44
# 3  1.44 1.56
# 4  1.56 1.68
# 5  1.68 1.8
# 6  1.8  1.92
# 7  1.92 2.04
# 8  2.04 2.16
# 9  2.16 2.28
# 10 2.28 2.4

to_read_proto = ['fit_{level}_1', 'fit_{level}_6', 'fit_{level}_10']
etexts        = ["1.2 < |#eta| < 1.32", "1.8 < |#eta| < 1.92", "2.28 < |#eta| < 2.4"]

c1 = ROOT.TCanvas('c1', 'c1', 1200, 600)
c1.SetFrameLineWidth(3)
# c1.SetLeftMargin(0)
# c1.SetRightMargin(0)
c1.Divide(3,2)

## canvas is now organised as
## 1 2 3
## 4 5 6

frames  = []
texts   = []

for iangle in range(len(files)): ## 0 : phi, 1: theta
    for ibin, tr in enumerate(to_read_proto):
        low  = files[iangle].Get(tr.format(level='low'))
        cent = files[iangle].Get(tr.format(level='cent'))
        high = files[iangle].Get(tr.format(level='high'))
        icanv = 3*iangle + ibin + 1
        print ".. in canvas nr:", icanv
        print " ...... file : ", files[iangle]
        print " ...... plot : ", tr
        c1.cd(icanv)
        ROOT.gPad.SetLogx()
        ROOT.gPad.SetLogy()
        ROOT.gPad.SetTopMargin(0.1)
        ROOT.gPad.SetBottomMargin(0.22)
        ROOT.gPad.SetRightMargin(0.05)
        ROOT.gPad.SetLeftMargin(0.18)
        # ROOT.gPad.SetLeftMargin(0)
        # ROOT.gPad.SetRightMargin(0)
        frame = ROOT.TH1F('frame_%i' % icanv, ';Track p_{T} [GeV]; %s' % ytitles[iangle], 100, xmin, xmax)
        frame.SetMinimum(ymins[iangle])
        frame.SetMaximum(ymaxs[iangle])

        frame.GetXaxis().SetTitleSize(0.07)
        frame.GetYaxis().SetTitleSize(0.07)
        frame.GetXaxis().SetLabelSize(0.065)
        frame.GetYaxis().SetLabelSize(0.065)
        frame.GetXaxis().SetTitleOffset(1.4)
        frame.GetYaxis().SetTitleOffset(1.2)

        frames.append(frame)
        frame.Draw()

        low.SetLineWidth(2)
        cent.SetLineWidth(2)
        high.SetLineWidth(2)

        low.Draw("L same")
        cent.Draw("L same")
        high.Draw("L same")

        etxt = ROOT.TLatex(0.7, 0.8, etexts[ibin])
        etxt.SetNDC(True)
        etxt.SetTextFont(42)
        etxt.SetTextSize(0.045)
        etxt.Draw()
        texts.append(etxt)

c1.Print('TDR_plots/matching_windows_TDR.pdf', 'pdf')
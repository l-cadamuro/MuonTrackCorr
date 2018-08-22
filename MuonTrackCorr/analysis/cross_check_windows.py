import ROOT
import uproot ## pip install uproot --user
import numpy as np

def to_mpi_pi (x):
    while (x >= np.pi): x -= 2.*np.pi;
    while (x < -np.pi): x += 2.*np.pi;
    return x

def findBin(thearr, val, closedLeft = True):
    if closedLeft:
        return findBinClosedLeft(thearr, val) # [min, max)
    else:
        return findBinClosedRight(thearr, val) # (min, max]

# [min, max)
def findBinClosedLeft (thearr, val):
    if val < thearr[0]:
        return -1
    if val >= thearr[-1]:
        return len(thearr)
    for i in range (len(thearr) -1 ):
        if val >= thearr[i] and val < thearr[i+1]:
            return i
    print "I should not be here!!"
    return 0

# (min, max]
def findBinClosedRight (thearr, val):
    if val <= thearr[0]:
        return -1
    if val > thearr[-1]:
        return len(thearr)
    for i in range (len(thearr) -1 ):
        if val > thearr[i] and val <= thearr[i+1]:
            return i
    print "I should not be here!!"
    return 0


ROOT.gROOT.SetBatch(True)

# fIn = ROOT.TFile.Open('matched_tree_MuMu_flatPt_0PU_23Apr2018.root')
# tIn = fIn.Get('tree')

tIn  = uproot.open('matched_tree_MuMu_flatPt_0PU_23Apr2018.root')['tree']
keys = tIn.keys()
data = tIn.arrays(keys)
totEvts = data['gen_pt'].size
print "tree has ", totEvts, 'entries', type(totEvts)

# fWindows = ROOT.TFile.Open('correlator_data/matching_windows.root')
fWindows = ROOT.TFile.Open('matching_windows.root')
h_dphi_l = fWindows.Get('h_dphi_l')
h_dphi_h = fWindows.Get('h_dphi_h')
h_dtheta_l = fWindows.Get('h_dtheta_l')
h_dtheta_h = fWindows.Get('h_dtheta_h')

nx = h_dphi_l.GetNbinsX()
ny = h_dphi_l.GetNbinsY()
print "pT  histo boundaries:", h_dphi_l.GetXaxis().GetBinLowEdge(1), h_dphi_l.GetXaxis().GetBinLowEdge(nx+1)
print "eta histo boundaries:", h_dphi_l.GetYaxis().GetBinLowEdge(1), h_dphi_l.GetYaxis().GetBinLowEdge(ny+1)

# nevents = tIn.GetEntries()
# print "Tree has", nevents, "events"

# print "Tree has", tIn.GetEntries(), "events"

# n_emtf  = tIn.GetEntries("emtf_pt > 0")
# n_trk   = tIn.GetEntries("trk_pt > 0")
# n_emtf_and_trk = tIn.GetEntries("trk_pt > 0 && emtf_pt > 0")

eff_plot_pt  = ROOT.TEfficiency("eff_plot_pt", ";gen p_{T}; #varepsilon",  100, 0, 500)
eff_plot_eta = ROOT.TEfficiency("eff_plot_eta", ";gen #eta; #varepsilon", 100, -3, 3)

nevents = 0
n_emtf = 0
n_trk = 0
n_emtf_and_trk = 0

n_pass_phi = 0
n_pass_theta = 0
n_pass_theta_and_phi = 0


for ibinx in range(1, nx+1):
    for ibiny in range(1, ny+1):
        t_phi_l = h_dphi_l.GetBinContent(ibinx, ibiny)
        t_phi_h = h_dphi_h.GetBinContent(ibinx, ibiny)
        t_theta_l = h_dtheta_l.GetBinContent(ibinx, ibiny)
        t_theta_h = h_dtheta_h.GetBinContent(ibinx, ibiny)
        print ibinx, ibiny, '{:6f} {:6f} {:6f} {:6f}'.format(t_phi_l, t_phi_h, t_theta_l, t_theta_h)


bins_trk_pt  = np.linspace(start = 2.0, stop = 202.0, num = 200+1)
bins_trk_eta = np.linspace(start = 1.2, stop = 2.4,   num = 10+1)

fOut = ROOT.TFile('cross_check_histos.root', 'recreate')
histos_dthetas = {}
histos_dphis = {}

#### copy the structure of the compariosn histos
fRootDTset = ROOT.TFile.Open('matching_windows.root')
for ix in range(len(bins_trk_pt)-1):
    for iy in range(len(bins_trk_eta)-1):
        ibinx = ix+1
        ibiny = iy+1
        histo_dtheta_XC = fRootDTset.Get('h_dthetas_%i_%i' % (ibinx, ibiny))
        histo_dphi_XC   = fRootDTset.Get('h_dphis_%i_%i' % (ibinx, ibiny))
        histo_dtheta = ROOT.TH1D('histo_dtheta_%i_%i' % (ibinx, ibiny), 'histo_dtheta_%i_%i' % (ibinx, ibiny), histo_dtheta_XC.GetNbinsX(), histo_dtheta_XC.GetBinLowEdge(1), histo_dtheta_XC.GetBinLowEdge(histo_dtheta_XC.GetNbinsX()+1))
        histo_dphi = ROOT.TH1D('histo_dphi_%i_%i' % (ibinx, ibiny), 'histo_dphi_%i_%i' % (ibinx, ibiny), histo_dphi_XC.GetNbinsX(), histo_dphi_XC.GetBinLowEdge(1), histo_dphi_XC.GetBinLowEdge(histo_dphi_XC.GetNbinsX()+1))
        histo_dtheta.SetDirectory(0)
        histo_dphi.SetDirectory(0)
        histos_dthetas[(ibinx, ibiny)] = histo_dtheta
        histos_dphis[(ibinx, ibiny)] = histo_dphi
fRootDTset.Close()

# for iEv in range(tIn.GetEntries()):
# for iEv in range(100000):
for iEv in range(totEvts):
    if iEv % 10000 == 0: print iEv
    # tIn.GetEntry(iEv)

    gen_pt  = data['gen_pt'][iEv]
    gen_eta = data['gen_eta'][iEv]

    #### possible preselection
    # if gen_pt < 200: continue
    if gen_pt > 200: continue ### to avoid biasing efficiencies
    # if abs(gen_eta) < 1.4: continue
    # if abs(gen_eta) > 2.2: continue
    #####

    nevents += 1
    
    pass_trk_pt  = (data['trk_pt'][iEv] > 0)
    pass_emtf_pt = (data['emtf_pt'][iEv] > 0)
    
    if pass_trk_pt: n_trk += 1
    if pass_emtf_pt: n_emtf += 1
    if pass_trk_pt and pass_emtf_pt: n_emtf_and_trk += 1

    if not (pass_trk_pt and pass_emtf_pt):
        continue

    trk_theta = data['trk_theta'][iEv]
    trk_eta   = data['trk_eta'][iEv]
    trk_phi   = data['trk_phi'][iEv]
    trk_pt    = data['trk_pt'][iEv]

    emtf_theta = data['emtf_theta'][iEv]
    emtf_eta   = data['emtf_eta'][iEv]
    emtf_phi   = data['emtf_phi'][iEv]

    binx = h_dphi_l.GetXaxis().FindBin(trk_pt)
    biny = h_dphi_l.GetYaxis().FindBin(abs(trk_eta))
    
    if binx == 0: binx = 1
    if binx > nx: binx = nx
    if biny == 0: biny = 1
    if biny > ny: biny = ny
    # if binx == 0: continue
    # if binx > nx: continue
    # if biny == 0: continue
    # if biny > ny: continue

    # nevents += 1

    # binx = findBin(bins_trk_pt)
    # biny = findBin(bins_trk_eta)

    # if binx == 0 or binx > nx or biny == 0 or biny > ny:
    #     print "under/over flow ", binx, biny, "(", trk_pt, trk_eta, ")", "from", nx, ny

    # if biny == 0 or biny > ny:
    #     print "under/over flow ", binx, biny, "(", trk_pt, trk_eta, ")", "from", nx, ny
    
    wd_theta_l = h_dtheta_l.GetBinContent(binx, biny)
    wd_theta_h = h_dtheta_h.GetBinContent(binx, biny)
    wd_phi_l = h_dphi_l.GetBinContent(binx, biny)
    wd_phi_h = h_dphi_h.GetBinContent(binx, biny)

    # dphi   = abs(abs(emtf_phi) - abs(trk_phi))
    dtheta = abs(abs(emtf_theta) - abs(trk_theta))
    dphi   = abs ( to_mpi_pi(emtf_phi - trk_phi) )

    pass_phi   = (dphi > wd_phi_l and dphi < wd_phi_h)
    pass_theta = (dtheta > wd_theta_l and dtheta < wd_theta_h)

    # print dphi, wd_phi_l, wd_phi_h, pass_phi
    # print dtheta, wd_theta_l, wd_theta_h, pass_theta
    # print ""

    if pass_phi:                 n_pass_phi            += 1
    if pass_theta:               n_pass_theta          += 1
    if pass_phi and pass_theta : n_pass_theta_and_phi  += 1

    eff_plot_pt.Fill ((pass_phi and pass_theta), gen_pt)
    eff_plot_eta.Fill ((pass_phi and pass_theta), gen_eta)

    ##### fill distros xcheck plots
    binx = findBin(bins_trk_pt, trk_pt)
    biny = findBin(bins_trk_eta, abs(trk_eta))

    if binx >= 0 and binx < len(bins_trk_pt) and biny >= 0 and biny < len(bins_trk_eta):
        binx += 1
        biny += 1
        histos_dthetas[(binx, biny)].Fill(dtheta)
        histos_dphis[(binx, biny)].Fill(dphi)


print "*** efficiencies [%] *** . From ", nevents , "preselected events"
print "EMTF             " , 100.*n_emtf         / nevents 
print "TRK              " , 100.*n_trk          / nevents 
print "EMTF + TRK       " , 100.*n_emtf_and_trk / nevents 
print "pass phi         " , 100.*n_pass_phi            / nevents
print "pass theta       " , 100.*n_pass_theta          / nevents
print "pass phi + theta " , 100.*n_pass_theta_and_phi  / nevents

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)

eff_plot_pt.Draw()
c1.Print('eff_plot_pt.pdf', 'pdf')

eff_plot_eta.Draw()
c1.Print('eff_plot_eta.pdf', 'pdf')

fOut.cd()
for h in histos_dthetas.values():
    h.Write()
for h in histos_dphis.values():
    h.Write()

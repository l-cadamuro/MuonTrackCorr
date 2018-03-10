import ROOT
# import math

class P4:
    """ same as a TLV, but store directly pt/eta/phi so that I do not need the mass """
    def __init__(self):
        self.pt  = 0.0
        self.eta = 0.0
        self.phi = 0.0
        self.m   = 0.0
    
    def set_p4(self, pt, eta, phi, m):
        self.pt  = pt
        self.eta = eta
        self.phi = phi
        self.m   = m

    def deltaR(self, otherP4):
        deta = self.eta-otherP4.eta
        dphi = ROOT.TVector2.Phi_mpi_pi(self.phi-otherP4.phi)
        return ROOT.TMath.Sqrt( deta*deta+dphi*dphi);

class EffPlot:
    def __init__(self, name, title, nbinsx, xmin, xmax):
        self.h_all  = ROOT.TH1F('h_all_'+name,  title,  nbinsx, xmin, xmax)
        self.h_pass = ROOT.TH1F('h_pass_'+name, title,  nbinsx, xmin, xmax)
        self.h_pass.SetLineColor(ROOT.kRed)
        self.name = name
    
    def feed (self, val, accept):
        self.h_all.Fill(val)
        if accept:
            self.h_pass.Fill(val)

    def makeEffPlot (self):
        self.effPlot = ROOT.TGraphAsymmErrors()
        self.effPlot.SetName('eff_'+self.name)
        self.effPlot.BayesDivide(self.h_pass, self.h_all)
        self.effPlot.SetMarkerStyle(8)
        self.effPlot.SetMarkerSize(0.8)

    def saveToFile(self, fOut):
        fOut.cd()
        self.h_all.Write()
        self.h_pass.Write()
        self.effPlot.Write()

#######################################

def parseInputFileList (fileName) :
    filelist = []
    with open (fileName) as fIn:
        for line in fIn:
            line = (line.split("#")[0]).strip()
            if line:
                filelist.append(line)
    return filelist

#######################################

def sign(x):
    return 1 if x >= 0 else -1

#######################################

def dumpEvt(ch):
    print "*** gen particles :", ch.n_gen_mu, "***"
    for i in range(0, ch.n_gen_mu):
        print "{:<3} {:<20} {:<20} {:<20}".format(i, ch.gen_mu_pt.at(i), ch.gen_mu_eta.at(i), ch.gen_mu_phi.at(i))
    print ''

    print "*** L1TT tracks :", ch.n_L1TT_trk, "***"
    for i in range(0, ch.n_L1TT_trk):
        print "{:<3} {:<20} {:<20} {:<20}".format(i, ch.L1TT_trk_pt.at(i), ch.L1TT_trk_eta.at(i), ch.L1TT_trk_phi.at(i))
    print ''

    print "*** EMTF tracks :", ch.n_EMTF_mu, "***"
    for i in range(0, ch.n_EMTF_mu):
        print "{:<3} {:<20} {:<20} {:<20}".format(i, ch.EMTF_mu_pt.at(i), ch.EMTF_mu_eta.at(i), ch.EMTF_mu_phi.at(i))
    print ''
    
    print '\n'

ch = ROOT.TChain('Ntuplizer/MuonTrackTree')
flist = parseInputFileList('filelist/MuMu_flatPt_0PU_9Mar2018_muinfo.txt')
for fl in flist:
    ch.Add(fl)

maxEvts = 10000

#######
fOut = ROOT.TFile("EMTF_resolution_plots.root", 'recreate')
# h_trk_eff  = ROOT.TH1F('h_trk_eff',  ';gen #mu p_{T} [GeV];Tracker efficiency', 100, 0, 100)
# h_emtf_eff = ROOT.TH1F('h_emtf_eff', ';gen #mu p_{T} [GeV];EMTF efficiency', 100, 0, 100)
# h_comb_eff = ROOT.TH1F('h_comb_eff', ';gen #mu p_{T} [GeV];Combined efficiency', 100, 0, 100)
h_emtf_resol = ROOT.TH1D('emtf_resol',  ';EMTF p_{T} / gen #mu p_{T};a.u.', 100, 0, 5)


pT_thres = 22.0

iEv = -1
while True:
    iEv += 1
    if iEv % 1000 == 0:
    # if True:
        print '... processing', iEv

    if maxEvts >= 0:
        if iEv > maxEvts:
            break

    got = ch.GetEntry(iEv)
    if (got == 0):
        break

    if ch.n_gen_mu != 2:
        print "** WARNING: Event", iEv , "has", ch.n_gen_mu, "gen muons, skipping..."
        continue
    
    gen_mus = [
        P4(),
        P4(),
    ]
    
    for i in (0,1):
        gen_mus[i].set_p4( ch.gen_mu_pt.at(i), ch.gen_mu_eta.at(i), ch.gen_mu_phi.at(i), 0.105658)

    ### pos --> 0
    ### neg --> 1
    if sign(gen_mus[0].eta) < 0:
        print "mu 0 is in negative endcap?? skipping..."
        continue
        # print sign(gen_mus[0].eta)
        # print gen_mus[0].pt, gen_mus[0].eta, gen_mus[0].phi
        # print gen_mus[1].pt, gen_mus[1].eta, gen_mus[1].phi
        # print "...."

    p4_pos = []
    p4_neg = []
    for imu in range(0, ch.n_EMTF_mu):
        mu_p4 = P4()
        mu_p4.set_p4( ch.EMTF_mu_pt_xml.at(imu), ch.EMTF_mu_eta.at(imu), ch.EMTF_mu_phi.at(imu), 0.105658 )
        if sign(mu_p4.eta) > 0:
            p4_pos.append(mu_p4)
        else:
            p4_pos.append(mu_p4)

    if len(p4_pos) == 1 and gen_mus[0].pt > pT_thres:
        h_emtf_resol.Fill(p4_pos[-1].pt / gen_mus[0].pt)
    if len(p4_neg) == 1 and gen_mus[1].pt > pT_thres:
        h_emtf_resol.Fill(p4_neg[-1].pt / gen_mus[1].pt)

fOut.cd()    
h_emtf_resol.Write()
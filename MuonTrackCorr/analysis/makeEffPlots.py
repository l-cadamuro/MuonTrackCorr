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
        self.name = name
    
    def feed (self, val, accept):
        self.h_all.Fill(val)
        if accept:
            self.h_pass.Fill(val)

    def makeEffPlot (self):
        self.effPlot = ROOT.TGraphAsymmErrors()
        self.effPlot.SetName('eff_'+self.name)
        self.effPlot.BayesDivide(self.h_pass, self.h_all)

    def saveToFile(self, fOut):
        fOut.cd()
        self.h_all.Write()
        self.h_pass.Write()
        self.effPlot.Write()

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
ch.Add('/uscms/home/lcadamur/nobackup/MuonTrackCorr932/CMSSW_9_3_2/src/TkMuNtuple.root')

#######
fOut = ROOT.TFile("eff_plots.root", 'recreate')
# h_trk_eff  = ROOT.TH1F('h_trk_eff',  ';gen #mu p_{T} [GeV];Tracker efficiency', 100, 0, 100)
# h_emtf_eff = ROOT.TH1F('h_emtf_eff', ';gen #mu p_{T} [GeV];EMTF efficiency', 100, 0, 100)
# h_comb_eff = ROOT.TH1F('h_comb_eff', ';gen #mu p_{T} [GeV];Combined efficiency', 100, 0, 100)
h_trk_eff  = EffPlot('trk',  ';gen #mu p_{T} [GeV];Tracker efficiency', 100, 0, 100)
h_emtf_eff = EffPlot('emtf', ';gen #mu p_{T} [GeV];EMTF efficiency',    100, 0, 100)
h_comb_eff = EffPlot('comb', ';gen #mu p_{T} [GeV];Combined efficiency', 100, 0, 100)

#####################################################

iEv = -1
while True:
    iEv += 1
    # if iEv % 1000 == 0:
    if True:
        print '... processing', iEv

    got = ch.GetEntry(iEv)
    if (got == 0):
        break
    
    if ch.n_gen_mu != 2:
        print "** WARNING: Event", iEv , "has", ch.n_gen_mu, "gen muons, skipping..."
        continue
    
    print "DEV DEB", ch.n_L1TT_trk

    gen_mus = [
        P4(),
        P4(),
    ]
    for i in (0,1):
        gen_mus[i].set_p4( ch.gen_mu_pt.at(i), ch.gen_mu_eta.at(i), ch.gen_mu_phi.at(i), 0.105658)

    if abs(gen_mus[0].eta) < 1.2 and abs(gen_mus[1].eta) < 1.2: ## not a single mu in the endcap
        continue

    got_EMTF = [
        False,
        False
    ]
    got_trk = [
        False,
        False
    ]
    
    ### EMTF efficiency
    #### --> I need the phi coordinate

    ### trk efficiency6
    for itrk in range(0, ch.n_L1TT_trk):
        trk_p4 = P4()
        trk_p4.set_p4( ch.L1TT_trk_pt.at(i), ch.L1TT_trk_eta.at(i), ch.L1TT_trk_phi.at(i), 0.105658 )
        for igm in (0,1):
            if trk_p4.deltaR(gen_mus[igm]) < 0.5:
                got_trk[igm] = True

    for igm in (0,1):
        # print "... this mu has eta", igm, gen_mus[igm].eta
        if abs(gen_mus[igm].eta) < 1.2:
            continue ## was not in the endcap
        
        # print "... feeding", igm, gen_mus[igm].pt, got_trk[igm]

        h_trk_eff.feed(gen_mus[igm].pt, got_trk[igm])
        
        ## debug
        if not got_trk[igm]:
            print "did not get trk muon", igm
            dumpEvt(ch)
        else:
            print 'got it rght!!!'

#####################################################

h_trk_eff.makeEffPlot()
h_emtf_eff.makeEffPlot()
h_comb_eff.makeEffPlot()

h_trk_eff.saveToFile(fOut)
h_emtf_eff.saveToFile(fOut)
h_comb_eff.saveToFile(fOut)

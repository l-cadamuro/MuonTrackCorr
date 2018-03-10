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
flist = parseInputFileList('filelist/MuMu_flatPt_0PU_9Mar2018_erasEmul.txt')
for fl in flist:
    ch.Add(fl)

maxEvts = -1

# ch.Add('/uscms/home/lcadamur/nobackup/MuonTrackCorr932/CMSSW_9_3_2/src/TkMuNtuple.root')

#######
fOut = ROOT.TFile("eff_plots.root", 'recreate')
# h_trk_eff  = ROOT.TH1F('h_trk_eff',  ';gen #mu p_{T} [GeV];Tracker efficiency', 100, 0, 100)
# h_emtf_eff = ROOT.TH1F('h_emtf_eff', ';gen #mu p_{T} [GeV];EMTF efficiency', 100, 0, 100)
# h_comb_eff = ROOT.TH1F('h_comb_eff', ';gen #mu p_{T} [GeV];Combined efficiency', 100, 0, 100)
h_trk_eff  = EffPlot('trk',  ';gen #mu p_{T} [GeV];Tracker efficiency', 400, 0, 400)
h_emtf_eff = EffPlot('emtf', ';gen #mu p_{T} [GeV];EMTF efficiency',    400, 0, 400)
h_emtf_eff_nopt = EffPlot('emtf_nopt', ';gen #mu p_{T} [GeV];EMTF efficiency',    400, 0, 400)
h_comb_eff = EffPlot('comb', ';gen #mu p_{T} [GeV];Combined efficiency', 400, 0, 400)

#####################################################

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

    # if ch.n_gen_mu != ch.gen_mu_pt.size():
    #     print "GEN MU ? ", ch.n_gen_mu, ch.gen_mu_pt.size()
    # if ch.n_L1TT_trk != ch.L1TT_trk_pt.size():
    #     print "GEN MU ? ", ch.n_L1TT_trk, ch.L1TT_trk_pt.size()
    # if ch.n_EMTF_mu != ch.EMTF_mu_pt.size():
    #     print "GEN MU ? ", ch.n_EMTF_mu, ch.EMTF_mu_pt.size()
    
    if ch.n_gen_mu != 2:
        print "** WARNING: Event", iEv , "has", ch.n_gen_mu, "gen muons, skipping..."
        continue
    
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
    got_EMTF_nopt = [
        False,
        False
    ]
    got_trk = [
        False,
        False
    ]

    
    ### EMTF efficiency
    for imu in range(0, ch.n_EMTF_mu):
        mu_p4 = P4()
        mu_p4.set_p4( ch.EMTF_mu_pt_xml.at(imu), ch.EMTF_mu_eta.at(imu), ch.EMTF_mu_phi.at(imu), 0.105658 )
        mode = ch.EMTF_mu_mode.at(imu)
        pass_single_mu = True if (mode == 11 or mode == 13 or mode == 14 or mode == 15) else False;
        if not pass_single_mu:
            continue
        for igm in (0,1):
            # if mu_p4.deltaR(gen_mus[igm]) < 0.5 and mu_p4.pt > pT_thres :
            if sign(mu_p4.eta) == sign(gen_mus[igm].eta):
                got_EMTF_nopt[igm] = True
                if mu_p4.pt > pT_thres :
                    got_EMTF[igm] = True
                # else:
                #     if gen_mus[igm].pt > 40:
                #         print "OOOOH /?? "
                #         dumpEvt(ch)

    ### trk efficiency6
    for itrk in range(0, ch.n_L1TT_trk):
        trk_p4 = P4()
        trk_p4.set_p4( ch.L1TT_trk_pt.at(itrk), ch.L1TT_trk_eta.at(itrk), ch.L1TT_trk_phi.at(itrk), 0.105658 )
        for igm in (0,1):
            if trk_p4.deltaR(gen_mus[igm]) < 0.5 and trk_p4.pt > pT_thres :
                got_trk[igm] = True

    for igm in (0,1):
        # print "... this mu has eta", igm, gen_mus[igm].eta
        if abs(gen_mus[igm].eta) < 1.2:
            continue ## was not in the endcap
        
        # print "... feeding", igm, gen_mus[igm].pt, got_trk[igm]

        h_trk_eff.feed(gen_mus[igm].pt, got_trk[igm])
        h_emtf_eff.feed(gen_mus[igm].pt, got_EMTF[igm])
        h_emtf_eff_nopt.feed(gen_mus[igm].pt, got_EMTF_nopt[igm])
        h_comb_eff.feed(gen_mus[igm].pt, got_trk[igm] and got_EMTF_nopt[igm])
        
        ## debug
        # if not got_trk[igm]:
        #     print "did not get trk muon", igm
        #     dumpEvt(ch)
        # else:
        #     print 'got it rght!!!'

#####################################################

h_trk_eff.makeEffPlot()
h_emtf_eff.makeEffPlot()
h_emtf_eff_nopt.makeEffPlot()
h_comb_eff.makeEffPlot()

h_trk_eff.saveToFile(fOut)
h_emtf_eff.saveToFile(fOut)
h_emtf_eff_nopt.saveToFile(fOut)
h_comb_eff.saveToFile(fOut)

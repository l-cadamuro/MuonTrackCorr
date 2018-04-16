import ROOT
import argparse
from array import array
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

def deg_to_rad(x):
    return (x * ROOT.TMath.Pi()/180.)

def eta_to_theta(x):
    ''' give theta in rad '''
    return (2 * ROOT.TMath.ATan(ROOT.TMath.Exp(-1.*x)))

def to_mpio2_pio2(x):
    ''' put the angle in radians between -pi/2 and pi/2 '''
    while x >= 0.5*ROOT.TMath.Pi():
        x -= ROOT.TMath.Pi()
    while x < -0.5*ROOT.TMath.Pi():
        x += ROOT.TMath.Pi()
    return x

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


#######################################

parser = argparse.ArgumentParser(description='Command line parser of plotting options')
parser.add_argument('--output', dest='output', help='output file name', default="eff_plots.root")
parser.add_argument('--input',  dest='input',  help='input filelist',   default='filelist/MuMu_flatPt_0PU_9Mar2018_erasEmul.txt')
parser.add_argument('--maxEvts', dest='maxEvts', help='max events (-1 for all, default)',  type=int, default = -1)
parser.add_argument('--no-xml-pt', dest='xmlpt', help='use standard pt instead of xml one for EMTF muons', action='store_false', default=True)
parser.add_argument('--pt-thresh', dest='ptthresh', help='pT threshold for turn-on', type=float, default=22.0)
parser.add_argument('--single-mu-qual', dest='singlemuqual', help='use single mu qual', action='store_true', default=False)
parser.add_argument('--make-tree', dest='maketree', help='make a tree as output (do not apply pt cut on it)', action='store_true', default=False)
args = parser.parse_args()



ch = ROOT.TChain('Ntuplizer/MuonTrackTree')
print '... running on file list: ', args.input
flist = parseInputFileList(args.input)
for fl in flist:
    ch.Add(fl)
# ch.Add('/uscms/home/lcadamur/nobackup/MuonTrackCorr1000/CMSSW_10_0_0/src/MuonTrackCorr/MuonTrackCorr/test/TkMuNtuple_eras_muonly_bugfix.root')

maxEvts = args.maxEvts

### restrict to muons in this range for eff plots - to be tuned
# fiducial_eta_min = 1.3
# fiducial_eta_max = 1.8
fiducial_eta_min = 1.2
fiducial_eta_max = 2.4


#######
fOut = ROOT.TFile(args.output, 'recreate')
# h_trk_eff  = ROOT.TH1F('h_trk_eff',  ';gen #mu p_{T} [GeV];Tracker efficiency', 100, 0, 100)
# h_emtf_eff = ROOT.TH1F('h_emtf_eff', ';gen #mu p_{T} [GeV];EMTF efficiency', 100, 0, 100)
# h_comb_eff = ROOT.TH1F('h_comb_eff', ';gen #mu p_{T} [GeV];Combined efficiency', 100, 0, 100)
h_trk_eff  = EffPlot('trk',  ';gen #mu p_{T} [GeV];Tracker efficiency', 400, 0, 400)
h_emtf_eff = EffPlot('emtf', ';gen #mu p_{T} [GeV];EMTF efficiency',    400, 0, 400)
h_emtf_eff_nopt = EffPlot('emtf_nopt', ';gen #mu p_{T} [GeV];EMTF efficiency',    400, 0, 400)
h_comb_eff = EffPlot('comb', ';gen #mu p_{T} [GeV];Combined efficiency', 400, 0, 400)

h_trk_eff_eta  = EffPlot('trk_eta',  ';gen #mu #eta;Tracker efficiency', 100, -3.0, 3.0)
h_emtf_eff_eta = EffPlot('emtf_eta', ';gen #mu #eta;EMTF efficiency',    100, -3.0, 3.0)
h_emtf_eff_nopt_eta = EffPlot('emtf_nopt_eta', ';gen #mu #eta;EMTF efficiency',    100, -3.0, 3.0)
h_comb_eff_eta = EffPlot('comb_eta', ';gen #mu #eta;Combined efficiency', 100, -3.0, 3.0)

if args.maketree:
    ## tree to fill twice per event (1 per positive + 1 per negative endcap)
    ## note: if no match, will set pt to < 0
    ## note2: expressing all the values in radians
    
    tOut = ROOT.TTree('tree', 'tree')
    
    b_gen_pt     = array( 'd', [0] )
    b_gen_eta    = array( 'd', [0] )
    b_gen_theta  = array( 'd', [0] )
    b_gen_phi    = array( 'd', [0] )
    
    b_trk_pt     = array( 'd', [0] )
    b_trk_eta    = array( 'd', [0] )
    b_trk_theta  = array( 'd', [0] )
    b_trk_phi    = array( 'd', [0] )
    b_trk_mult   = array( 'i', [0] )
    
    b_emtf_pt      = array( 'd', [0] )
    b_emtf_xml_pt  = array( 'd', [0] )
    b_emtf_eta     = array( 'd', [0] )
    b_emtf_theta   = array( 'd', [0] )
    b_emtf_phi     = array( 'd', [0] )
    b_emtf_mode    = array( 'i', [0] )
    b_emtf_mult    = array( 'i', [0] )
    
    tOut.Branch('gen_pt', b_gen_pt, 'gen_pt/D')
    tOut.Branch('gen_eta', b_gen_eta, 'gen_eta/D')
    tOut.Branch('gen_theta', b_gen_theta, 'gen_theta/D')
    tOut.Branch('gen_phi', b_gen_phi, 'gen_phi/D')
    # tOut.Branch('gen_z',  b_gen_z, 'gen_z/D')
    
    tOut.Branch('trk_pt', b_trk_pt, 'trk_pt/D')
    tOut.Branch('trk_eta', b_trk_eta, 'trk_eta/D')
    tOut.Branch('trk_theta', b_trk_theta, 'trk_theta/D')
    tOut.Branch('trk_phi', b_trk_phi, 'trk_phi/D')
    tOut.Branch('trk_mult', b_trk_mult, 'trk_mult/I') ### how many valid trk were found in the event
    # tOut.Branch('trk_z', b_trk_z, 'trk_z/D')

    tOut.Branch('emtf_pt', b_emtf_pt, 'emtf_pt/D')
    tOut.Branch('emtf_xml_pt', b_emtf_xml_pt, 'emtf_xml_pt/D')
    tOut.Branch('emtf_eta', b_emtf_eta, 'emtf_eta/D')
    tOut.Branch('emtf_theta', b_emtf_theta, 'emtf_theta/D')
    tOut.Branch('emtf_phi', b_emtf_phi, 'emtf_phi/D')
    tOut.Branch('emtf_mode', b_emtf_mode, 'emtf_mode/I')
    tOut.Branch('emtf_mult', b_emtf_mult, 'emtf_mult/I')  ### how many valid trk were found in the event


#####################################################

pT_thres = args.ptthresh

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

    # if abs(gen_mus[0].eta) < fiducial_eta_min and abs(gen_mus[1].eta) < fiducial_eta_min: ## not a single mu in the fid
    #     continue

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

    ### the p$ objects for the tree
    EMTF_sel = [
        [],
        [],
    ]
    trk_sel = [
        [],
        [],
    ]

    
    ### EMTF efficiency
    for imu in range(0, ch.n_EMTF_mu):
        mu_p4 = P4()
        if args.xmlpt:
            mu_p4.set_p4( ch.EMTF_mu_pt_xml.at(imu), ch.EMTF_mu_eta.at(imu), ch.EMTF_mu_phi.at(imu), 0.105658 )
        else:
            mu_p4.set_p4( ch.EMTF_mu_pt.at(imu), ch.EMTF_mu_eta.at(imu), ch.EMTF_mu_phi.at(imu), 0.105658 )
        mode = ch.EMTF_mu_mode.at(imu)
        pass_single_mu = True if (mode == 11 or mode == 13 or mode == 14 or mode == 15) else False;
        if not pass_single_mu and args.singlemuqual:
            continue
        for igm in (0,1):
            # if mu_p4.deltaR(gen_mus[igm]) < 0.5 and mu_p4.pt > pT_thres :
            if sign(mu_p4.eta) == sign(gen_mus[igm].eta):
                EMTF_sel[igm].append(mu_p4)
                EMTF_sel[igm][-1].scaledPt = ch.EMTF_mu_pt.at(imu)
                EMTF_sel[igm][-1].xmlPt    = ch.EMTF_mu_pt_xml.at(imu)
                EMTF_sel[igm][-1].theta    = ch.EMTF_mu_theta.at(imu)
                EMTF_sel[igm][-1].mode     = mode
                got_EMTF_nopt[igm] = True
                if mu_p4.pt > pT_thres :
                    got_EMTF[igm] = True
                # else:
                #     if gen_mus[igm].pt > 40:
                #         print "**** Event with bad EMTF pT assignment"
                #         dumpEvt(ch)

    ### trk efficiency6
    for itrk in range(0, ch.n_L1TT_trk):
        trk_p4 = P4()
        trk_p4.set_p4( ch.L1TT_trk_pt.at(itrk), ch.L1TT_trk_eta.at(itrk), ch.L1TT_trk_phi.at(itrk), 0.105658 )
        for igm in (0,1):
            if trk_p4.deltaR(gen_mus[igm]) < 0.5:
                trk_sel[igm].append(trk_p4)
            if trk_p4.deltaR(gen_mus[igm]) < 0.5 and trk_p4.pt > pT_thres :
                got_trk[igm] = True

    for igm in (0,1):
        # print "... this mu has eta", igm, gen_mus[igm].eta
        if abs(gen_mus[igm].eta) < fiducial_eta_min or abs(gen_mus[igm].eta) > fiducial_eta_max:
            continue ## was not in the fiducial region
        
        # print "... feeding", igm, gen_mus[igm].pt, got_trk[igm]

        h_trk_eff.feed(gen_mus[igm].pt, got_trk[igm])
        h_emtf_eff.feed(gen_mus[igm].pt, got_EMTF[igm])
        h_emtf_eff_nopt.feed(gen_mus[igm].pt, got_EMTF_nopt[igm])
        h_comb_eff.feed(gen_mus[igm].pt, got_trk[igm] and got_EMTF_nopt[igm])

        h_trk_eff_eta.feed(gen_mus[igm].eta, got_trk[igm])
        h_emtf_eff_eta.feed(gen_mus[igm].eta, got_EMTF[igm])
        h_emtf_eff_nopt_eta.feed(gen_mus[igm].eta, got_EMTF_nopt[igm])
        h_comb_eff_eta.feed(gen_mus[igm].eta, got_trk[igm] and got_EMTF_nopt[igm])
        
        if args.maketree:
            ## if many matched, keep only the highest pT one
            # print "**** debug. I had"
            # for pp4 in EMTF_sel[igm]: print pp4.pt
            EMTF_sel[igm].sort(key = lambda x: x.pt, reverse=True)
            # print "**** debug. Now I have"
            # for pp4 in EMTF_sel[igm]: print pp4.pt
            trk_sel[igm].sort(key = lambda x: x.pt, reverse=True)
            b_gen_pt[0]    =                            gen_mus[igm].pt
            b_gen_eta[0]   =                            gen_mus[igm].eta
            b_gen_theta[0] = to_mpio2_pio2(eta_to_theta(gen_mus[igm].eta))
            b_gen_phi[0]   =                            gen_mus[igm].phi
            
            b_trk_pt[0]    =                            trk_sel[igm][0].pt    if trk_sel[igm] else -999
            b_trk_eta[0]   =                            trk_sel[igm][0].eta   if trk_sel[igm] else -999
            b_trk_theta[0] = to_mpio2_pio2(eta_to_theta(trk_sel[igm][0].eta)) if trk_sel[igm] else -999
            b_trk_phi[0]   =                            trk_sel[igm][0].phi   if trk_sel[igm] else -999
            b_trk_phi[0]   =                            trk_sel[igm][0].phi   if trk_sel[igm] else -999
            b_trk_mult[0]   =                            len(trk_sel[igm])
            
            b_emtf_pt[0]     =                                       EMTF_sel[igm][0].scaledPt if EMTF_sel[igm] else -999
            b_emtf_xml_pt[0] =                                       EMTF_sel[igm][0].xmlPt    if EMTF_sel[igm] else -999
            b_emtf_eta[0]    =                                       EMTF_sel[igm][0].eta      if EMTF_sel[igm] else -999
            b_emtf_theta[0]  =            to_mpio2_pio2(eta_to_theta(EMTF_sel[igm][0].eta))    if EMTF_sel[igm] else -999
            b_emtf_phi[0]    =                            deg_to_rad(EMTF_sel[igm][0].phi)     if EMTF_sel[igm] else -999
            b_emtf_mode[0]   =                                       EMTF_sel[igm][0].mode     if EMTF_sel[igm] else -999
            b_emtf_mult[0]   =                                       len(EMTF_sel[igm])

            # if EMTF_sel[igm]:
            #     # print "xcheck: ", to_mpio2_pio2(eta_to_theta(b_emtf_eta[0])), deg_to_rad(EMTF_sel[igm][0].theta)
            #     if (to_mpio2_pio2(eta_to_theta(b_emtf_eta[0])) - deg_to_rad(EMTF_sel[igm][0].theta)) > 0.0001:
            #         print "????", to_mpio2_pio2(eta_to_theta(b_emtf_eta[0])), deg_to_rad(EMTF_sel[igm][0].theta)

            tOut.Fill()

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

h_trk_eff_eta.makeEffPlot()
h_emtf_eff_eta.makeEffPlot()
h_emtf_eff_nopt_eta.makeEffPlot()
h_comb_eff_eta.makeEffPlot()


h_trk_eff.saveToFile(fOut)
h_emtf_eff.saveToFile(fOut)
h_emtf_eff_nopt.saveToFile(fOut)
h_comb_eff.saveToFile(fOut)

h_trk_eff_eta.saveToFile(fOut)
h_emtf_eff_eta.saveToFile(fOut)
h_emtf_eff_nopt_eta.saveToFile(fOut)
h_comb_eff_eta.saveToFile(fOut)

fOut.cd()
tOut.Write()

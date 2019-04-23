import ROOT

fIn = ROOT.TFile.Open('root://cmseos.fnal.gov//store/user/lcadamur/L1MuTrks_ntuples/Ds_Tau3Mu_PU0_17Apr_Tau3MuSamples/output/ntuple_0.root')
tIn = fIn.Get("Ntuplizer/MuonTrackTree")

# restrict all to events that have exactly 3mu - so I know that I have a single Ds decay

nEntries = tIn.GetEntries()
nTot     = tIn.GetEntries('n_gen_mu == 3')

n_oneinEndcap   = tIn.GetEntries('Sum$(abs(gen_mu_eta)>1.3 && abs(gen_mu_eta)<2.4) >= 1 && n_gen_mu == 3') ## at least one muon in the endcap
n_twoinEndcap   = tIn.GetEntries('Sum$(abs(gen_mu_eta)>1.3 && abs(gen_mu_eta)<2.4) >= 2 && n_gen_mu == 3') ## at least two muons in the endcap
n_threeinEndcap = tIn.GetEntries('Sum$(abs(gen_mu_eta)>1.3 && abs(gen_mu_eta)<2.4) >= 3 && n_gen_mu == 3') ## at least three muons in the endcap

n_oneinBarr = tIn.GetEntries('Sum$(abs(gen_mu_eta)<0.8) >= 1 && n_gen_mu == 3') ## at least one muon in the endcap
n_oneinOvrl = tIn.GetEntries('Sum$(abs(gen_mu_eta)>0.8 && abs(gen_mu_eta)<1.3) >= 1 && n_gen_mu == 3') ## at least one muon in the endcap
n_oneinME0  = tIn.GetEntries('Sum$(abs(gen_mu_eta)>2.4 && abs(gen_mu_eta)<2.8) >= 1 && n_gen_mu == 3') ## at least one muon in the endcap
n_oneOutisde = tIn.GetEntries('Sum$(abs(gen_mu_eta)>2.8) >= 1 && n_gen_mu == 3') ## at least one muon in the endcap

print 'entries', nEntries
print 'tot events considered', nTot
print 'oneinEndcap = {} - {:.2f}%'.format(n_oneinEndcap, 100.*n_oneinEndcap/nTot)
print 'twoinEndcap = {} - {:.2f}%'.format(n_twoinEndcap, 100.*n_twoinEndcap/nTot)
print 'threeinEndcap = {} - {:.2f}%'.format(n_threeinEndcap, 100.*n_threeinEndcap/nTot)
print 'oneinBarr = {} - {:.2f}%'.format(n_oneinBarr, 100.*n_oneinBarr/nTot)
print 'oneinOvrl = {} - {:.2f}%'.format(n_oneinOvrl, 100.*n_oneinOvrl/nTot)
print 'oneinME0 = {} - {:.2f}%'.format(n_oneinME0, 100.*n_oneinME0/nTot)
print 'oneOutisde = {} - {:.2f}%'.format(n_oneOutisde, 100.*n_oneOutisde/nTot)

#### basic macro to plot occupancies from the Ntuplizer inputs

from plotutils import plotUtils
from plotutils import plotMaker
import collections
import ROOT
import sys

ROOT.gROOT.SetBatch(True)

ch    = ROOT.TChain("Ntuplizer/MuonTrackTree")
# flist = '../filelist/prova.txt'

# flist = '../filelist/TauTau_pm_Tau3Mu_FlatPt1To10_PU0_15Apr_Tau3MuSamples.txt'
# flist = '../filelist/TauTau_pm_Tau3Mu_FlatPt1To10_PU0_15Apr_Tau3MuSamples_short.txt'
# tag   = 'taugun'

# flist = '../filelist/Ds_Tau3Mu_PU0_17Apr_Tau3MuSamples_short.txt'
# tag   = 'DsToTau'

# plotUtils.load_from_filelist(ch, flist, maxFiles = 1)

## block for ZB plots
PU = 0
if len(sys.argv) > 1:
    PU = int(sys.argv[1])

# flist = '../filelist/TDR_MC_EMTFpp/NuGun_200PU.txt'
# tag = 'ZB_PU200'

flist = '../filelist/TDR_MC_EMTFpp/NuGun_%iPU.txt' % PU
tag = 'ZB_PU%i' % PU

print flist
print tag


plotUtils.load_from_filelist(ch, flist, maxFiles = 100)

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)

pm = plotMaker.plotMaker()

# h = plotMaker.histo(name='h', title='prova', expr='n_gen_mu', cut='', nbins=10, range_binning=(0, 10))
# h = plotMaker.histo(name='h', title='prova', expr='n_gen_mu', cut='', nbins=10, range_binning=(0, 10))
# h.build_histo(ch)

###################################################################################

## filtering on gen mu eta
# gen_mu_1p4_2p4_gt2 = plotMaker.cut('Sum$(abs(gen_mu_eta)>1.4 && abs(gen_mu_eta)<2.4) > 2')
# gen_mu_1p4_1p8_gt2 = plotMaker.cut('Sum$(abs(gen_mu_eta)>1.4 && abs(gen_mu_eta)<1.8) > 2')
# inclusive          = plotMaker.cut('')

# restrict to the positive endcap
gen_mu_1p4_2p4_gt2 = plotMaker.cut('Sum$(gen_mu_eta>1.4 && gen_mu_eta<2.4) > 2')
gen_mu_1p4_1p8_gt2 = plotMaker.cut('Sum$(gen_mu_eta>1.4 && gen_mu_eta<1.8) > 2')
inclusive          = plotMaker.cut('Sum$(gen_mu_eta>0)')
nocut             = plotMaker.cut('1==1')


# gen_mu_cut = inclusive
# plot_name_proto = '%s_plots_tau3mu_inclusive/{hname}.pdf' % tag

# gen_mu_cut = gen_mu_1p4_2p4_gt2
# plot_name_proto = '%s_plots_tau3mu_gen_mu_1p4_2p4_gt2/{hname}.pdf' % tag


gen_mu_cut = nocut
plot_name_proto = '%s_plots_ZeroBias/{hname}.pdf' % tag
rootOut = '%s_plots_ZeroBias/histos.root' % tag

rootFileOut = ROOT.TFile(rootOut, 'recreate')

# gen_mu_cut = gen_mu_1p4_1p8_gt2
# plot_name_proto = '%s_plots_tau3mu_gen_mu_1p4_1p8_gt2/{hname}.pdf' % tag


histos = collections.OrderedDict()
# histos['n_gen_mu'] = {
#     'name'  : 'n_gen_mu',
#     'title' : ';N gen #mu;a.u.',
#     'expr'  : 'n_gen_mu',
#     'nbins' : 10,
#     'xmin'  : 0,
#     'xmax'  : 10,   
#     'cut'   : gen_mu_cut.cut,
# }
# histos['n_gen_mu_pos_eta'] = {
#     'name'  : 'n_gen_mu_pos_eta',
#     'title' : ';N gen #mu with #eta > 0;a.u.',
#     'expr'  : 'Sum$(gen_mu_eta > 0)',
#     'nbins' : 10,
#     'xmin'  : 0,
#     'xmax'  : 10,   
#     'cut'   : gen_mu_cut.cut,
# }
# histos['gen_mu_eta'] = {
#     'name'  : 'gen_mu_eta',
#     'title' : ';Gen #mu #eta;a.u.',
#     'expr'  : 'gen_mu_eta',
#     'nbins' : 100,
#     'xmin'  : -4,
#     'xmax'  : 4,   
#     'cut'   : gen_mu_cut.cut,
# }
# histos['gen_mu_pt'] = {
#     'name'  : 'gen_mu_pt',
#     'title' : ';Gen #mu p_{T} [GeV];a.u.',
#     'expr'  : 'gen_mu_pt',
#     'nbins' : 100,
#     'xmin'  : 0,
#     'xmax'  : 10,   
#     'cut'   : gen_mu_cut.cut,
# }
# histos['n_gen_mu_eta1p4_2p4'] = {
#     'name'  : 'n_gen_mu_eta1p4_2p4',
#     'title' : ';N gen #mu with 1.4 < |#eta| < 2.4;a.u.',
#     'expr'  : 'Sum$(abs(gen_mu_eta)>1.4 && abs(gen_mu_eta)<2.4)',
#     'nbins' : 10,
#     'xmin'  : 0,
#     'xmax'  : 10,   
#     # 'cut'   : 'n_gen_mu == 3', ## restrict to events with exactly one tau -> 3mu
#     'cut'   : gen_mu_cut.cut,
# }
############################################
# histos['n_gen_tau'] = {
#     'name'  : 'n_gen_tau',
#     'title' : ';N gen #tau;a.u.',
#     'expr'  : 'n_gen_tau',
#     'nbins' : 10,
#     'xmin'  : 0,
#     'xmax'  : 10,   
#     'cut'   : gen_mu_cut.cut,
# }
# histos['gen_tau_pt'] = {
#     'name'  : 'gen_tau_pt',
#     'title' : ';Gen #tau p_{T} [GeV];a.u.',
#     'expr'  : 'gen_tau_pt',
#     'nbins' : 100,
#     'xmin'  : 0,
#     'xmax'  : 20,   
#     'cut'   : gen_mu_cut.cut,
# }
# histos['gen_tau_eta'] = {
#     'name'  : 'gen_tau_eta',
#     'title' : ';Gen #tau #eta;a.u.',
#     'expr'  : 'gen_tau_eta',
#     'nbins' : 100,
#     'xmin'  : -6,
#     'xmax'  : 6,   
#     'cut'   : gen_mu_cut.cut,
# }
############################################
histos['n_EMTF_mu'] = {
    'name'  : 'n_EMTF_mu',
    'title' : ';N EMTF #mu;a.u.',
    'expr'  : 'n_EMTF_mu',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'cut'   : gen_mu_cut.cut,
    'norm'  : 1.0,  
}
histos['EMTF_mu_endcap_pos'] = {
    'name'  : 'EMTF_mu_endcap_pos',
    'title' : ';N EMTF #mu in positive endcap;a.u.',
    'expr'  : 'Sum$(EMTF_mu_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'cut'   : gen_mu_cut.cut,
    'norm'  : 1.0,  
}
histos['EMTF_mu_pt'] = {
    'name'  : 'EMTF_mu_pt_endcap_pos',
    'title' : ';EMTF #mu p_{T} in positive endcap [GeV];a.u.',
    'expr'  : 'EMTF_mu_pt',
    'nbins' : 50,
    'xmin'  : 0,
    'xmax'  : 10,
    'cut'   : (gen_mu_cut + 'EMTF_mu_eta > 0').cut, ## restrict the EMTF candidates to pos eta
    'norm'  : 1.0,  
}
histos['EMTF_mu_eta'] = {
    'name'  : 'EMTF_mu_eta_endcap_pos',
    'title' : ';EMTF #mu #eta in positive endcap;a.u.',
    'expr'  : 'EMTF_mu_pt',
    'nbins' : 50,
    'xmin'  : -4,
    'xmax'  : 4,
    'cut'   : (gen_mu_cut + 'EMTF_mu_eta > 0').cut, ## restrict the EMTF candidates to pos eta
    'norm'  : 1.0,  
}
############################################
histos['TkMu_endcap_pos'] = {
    'name'  : 'TkMu_endcap_pos',
    'title' : ';N TkMu in positive endcap;a.u.',
    'expr'  : 'Sum$(L1_TkMu_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'cut'   : gen_mu_cut.cut,
    'norm'  : 1.0,  
}
histos['TkMuStub_endcap_pos'] = {
    'name'  : 'TkMuStub_endcap_pos',
    'title' : ';N TkMuStub in positive endcap;a.u.',
    'expr'  : 'Sum$(L1_TkMuStub_eta > 0)',
    'nbins' : 100,
    'xmin'  : 0,
    'xmax'  : 100,
    'cut'   : gen_mu_cut.cut,
    'norm'  : 1.0,  
}
############################################
histos['n_CSC_S1'] = {
    'name'  : 'n_CSC_S1',
    'title' : ';N CSC hits in S1 (pos. endcap);a.u.',
    'expr'  : 'Sum$(mu_hit_station==1 && mu_hit_type==1 && mu_hit_sim_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
histos['n_CSC_S1_ext'] = {
    'name'  : 'n_CSC_S1_ext',
    'title' : ';N CSC hits in S1 (pos. endcap);a.u.',
    'expr'  : 'Sum$(mu_hit_station==1 && mu_hit_type==1 && mu_hit_sim_eta > 0)',
    'nbins' : 50,
    'xmin'  : 0,
    'xmax'  : 50,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
histos['n_CSC_S2'] = {
    'name'  : 'n_CSC_S2',
    'title' : ';N CSC hits in S2 (pos. endcap);a.u.',
    'expr'  : 'Sum$(mu_hit_station==2 && mu_hit_type==1 && mu_hit_sim_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
histos['n_CSC_S3'] = {
    'name'  : 'n_CSC_S3',
    'title' : ';N CSC hits in S3 (pos. endcap);a.u.',
    'expr'  : 'Sum$(mu_hit_station==3 && mu_hit_type==1 && mu_hit_sim_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
histos['n_CSC_S4'] = {
    'name'  : 'n_CSC_S4',
    'title' : ';N CSC hits in S4 (pos. endcap);a.u.',
    'expr'  : 'Sum$(mu_hit_station==4 && mu_hit_type==1 && mu_hit_sim_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
############################################
histos['n_RPC_S1'] = {
    'name'  : 'n_RPC_S1',
    'title' : ';N RPC hits in S1 (pos. endcap);a.u.',
    'expr'  : 'Sum$(mu_hit_station==1 && mu_hit_type==2 && mu_hit_sim_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
histos['n_RPC_S2'] = {
    'name'  : 'n_RPC_S2',
    'title' : ';N RPC hits in S2 (pos. endcap);a.u.',
    'expr'  : 'Sum$(mu_hit_station==2 && mu_hit_type==2 && mu_hit_sim_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
histos['n_RPC_S3'] = {
    'name'  : 'n_RPC_S3',
    'title' : ';N RPC hits in S3 (pos. endcap);a.u.',
    'expr'  : 'Sum$(mu_hit_station==3 && mu_hit_type==2 && mu_hit_sim_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
histos['n_RPC_S4'] = {
    'name'  : 'n_RPC_S4',
    'title' : ';N RPC hits in S4 (pos. endcap);a.u.',
    'expr'  : 'Sum$(mu_hit_station==4 && mu_hit_type==2 && mu_hit_sim_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
##################################################################################
# histos['n_trk_ptgt0'] = {
#     'name'  : 'n_trk_ptgt0',
#     'title' : ';N tracks (pos. endcap);a.u.',
#     'expr'  : 'Sum$(L1TT_trk_eta > 0  && L1TT_trk_pt > 0)',
#     'nbins' : 100,
#     'xmin'  : 0,
#     'xmax'  : 100,
#     'norm'  : 1.0,
#     'cut'   : gen_mu_cut.cut,
# }
histos['n_trk_ptgt5'] = {
    'name'  : 'n_trk_ptgt5',
    'title' : ';N tracks (pos. endcap);a.u.',
    'expr'  : 'Sum$(L1TT_trk_eta > 1.2  && L1TT_trk_pt > 5)',
    'nbins' : 50,
    'xmin'  : 0,
    'xmax'  : 50,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
histos['n_trk_ptgt5_ext'] = {
    'name'  : 'n_trk_ptgt5_ext',
    'title' : ';N tracks (pos. endcap);a.u.',
    'expr'  : 'Sum$(L1TT_trk_eta > 1.2  && L1TT_trk_pt > 5)',
    'nbins' : 150,
    'xmin'  : 0,
    'xmax'  : 150,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
histos['n_trk_ptgt10'] = {
    'name'  : 'n_trk_ptgt10',
    'title' : ';N tracks (pos. endcap);a.u.',
    'expr'  : 'Sum$(L1TT_trk_eta > 1.2  && L1TT_trk_pt > 10)',
    'nbins' : 50,
    'xmin'  : 0,
    'xmax'  : 50,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}
histos['n_trk_ptgt20'] = {
    'name'  : 'n_trk_ptgt20',
    'title' : ';N tracks (pos. endcap);a.u.',
    'expr'  : 'Sum$(L1TT_trk_eta > 1.2  && L1TT_trk_pt > 20)',
    'nbins' : 50,
    'xmin'  : 0,
    'xmax'  : 50,
    'norm'  : 1.0,
    'cut'   : gen_mu_cut.cut,
}


###################################################################################

overlays = {}
overlays['n_CSC'] = {
    'parts'   : ['n_CSC_S1', 'n_CSC_S2', 'n_CSC_S3', 'n_CSC_S4'],
    'leg'     : {
        'n_CSC_S1' : 'S1',
        'n_CSC_S2' : 'S2',
        'n_CSC_S3' : 'S3',
        'n_CSC_S4' : 'S4',
    },
    'title' : ';N CSC hits in positive endcap;a.u.',
    'logy'   : False,
}
overlays['n_RPC'] = {
    'parts'   : ['n_RPC_S1', 'n_RPC_S2', 'n_RPC_S3', 'n_RPC_S4'],
    'leg'     : {
        'n_RPC_S1' : 'S1',
        'n_RPC_S2' : 'S2',
        'n_RPC_S3' : 'S3',
        'n_RPC_S4' : 'S4',
    },
    'title' : ';N RPC hits in positive endcap;a.u.',
    'logy'   : False,
}
overlays['n_trk'] = {
    # 'parts'   : ['n_trk_ptgt0', 'n_trk_ptgt5', 'n_trk_ptgt10', 'n_trk_ptgt20'],
    'parts'   : ['n_trk_ptgt5', 'n_trk_ptgt10', 'n_trk_ptgt20'],
    'leg'     : {
        # 'n_trk_ptgt0'  : 'p_{T} > 0 GeV',
        'n_trk_ptgt5'  : 'p_{T} > 5 GeV',
        'n_trk_ptgt10' : 'p_{T} > 10 GeV',
        'n_trk_ptgt20' : 'p_{T} > 20 GeV',
    },
    'title' : ';N tracks in positive endcap;a.u.',
    'logy'   : False,
}



pm.load_histos(histos)
pm.build_histos(ch)
pm.set_overlays(overlays)
pm.plot_name_proto = plot_name_proto
pm.rootfile_output = rootFileOut
pm.c1 = c1

# pm.histos['n_CSC_S1'].histo.Draw()
# c1.Print('prova.pdf', 'pdf')

pm.plot_all(do_png=True)

# h.histo.Draw()
# c1.Print('prova.pdf', 'pdf')
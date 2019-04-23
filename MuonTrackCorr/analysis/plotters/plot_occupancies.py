#### basic macro to plot occupancies from the Ntuplizer inputs

from plotutils import plotUtils
from plotutils import plotMaker
import collections
import ROOT

ROOT.gROOT.SetBatch(True)

ch    = ROOT.TChain("Ntuplizer/MuonTrackTree")
# flist = '../filelist/prova.txt'

# flist = '../filelist/TauTau_pm_Tau3Mu_FlatPt1To10_PU0_15Apr_Tau3MuSamples.txt'
# flist = '../filelist/TauTau_pm_Tau3Mu_FlatPt1To10_PU0_15Apr_Tau3MuSamples_short.txt'
# tag   = 'taugun'

flist = '../filelist/Ds_Tau3Mu_PU0_17Apr_Tau3MuSamples_short.txt'
tag   = 'DsToTau'

plotUtils.load_from_filelist(ch, flist)

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


# gen_mu_cut = inclusive
# plot_name_proto = '%s_plots_tau3mu_inclusive/{hname}.pdf' % tag

gen_mu_cut = gen_mu_1p4_2p4_gt2
plot_name_proto = '%s_plots_tau3mu_gen_mu_1p4_2p4_gt2/{hname}.pdf' % tag

# gen_mu_cut = gen_mu_1p4_1p8_gt2
# plot_name_proto = '%s_plots_tau3mu_gen_mu_1p4_1p8_gt2/{hname}.pdf' % tag


histos = collections.OrderedDict()
histos['n_gen_mu'] = {
    'name'  : 'n_gen_mu',
    'title' : ';N gen #mu;a.u.',
    'expr'  : 'n_gen_mu',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,   
    'cut'   : gen_mu_cut.cut,
}
histos['n_gen_mu_pos_eta'] = {
    'name'  : 'n_gen_mu_pos_eta',
    'title' : ';N gen #mu with #eta > 0;a.u.',
    'expr'  : 'Sum$(gen_mu_eta > 0)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,   
    'cut'   : gen_mu_cut.cut,
}
histos['gen_mu_eta'] = {
    'name'  : 'gen_mu_eta',
    'title' : ';Gen #mu #eta;a.u.',
    'expr'  : 'gen_mu_eta',
    'nbins' : 100,
    'xmin'  : -4,
    'xmax'  : 4,   
    'cut'   : gen_mu_cut.cut,
}
histos['gen_mu_pt'] = {
    'name'  : 'gen_mu_pt',
    'title' : ';Gen #mu p_{T} [GeV];a.u.',
    'expr'  : 'gen_mu_pt',
    'nbins' : 100,
    'xmin'  : 0,
    'xmax'  : 10,   
    'cut'   : gen_mu_cut.cut,
}
histos['n_gen_mu_eta1p4_2p4'] = {
    'name'  : 'n_gen_mu_eta1p4_2p4',
    'title' : ';N gen #mu with 1.4 < |#eta| < 2.4;a.u.',
    'expr'  : 'Sum$(abs(gen_mu_eta)>1.4 && abs(gen_mu_eta)<2.4)',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,   
    # 'cut'   : 'n_gen_mu == 3', ## restrict to events with exactly one tau -> 3mu
    'cut'   : gen_mu_cut.cut,
}
############################################
histos['n_gen_tau'] = {
    'name'  : 'n_gen_tau',
    'title' : ';N gen #tau;a.u.',
    'expr'  : 'n_gen_tau',
    'nbins' : 10,
    'xmin'  : 0,
    'xmax'  : 10,   
    'cut'   : gen_mu_cut.cut,
}
histos['gen_tau_pt'] = {
    'name'  : 'gen_tau_pt',
    'title' : ';Gen #tau p_{T} [GeV];a.u.',
    'expr'  : 'gen_tau_pt',
    'nbins' : 100,
    'xmin'  : 0,
    'xmax'  : 20,   
    'cut'   : gen_mu_cut.cut,
}
histos['gen_tau_eta'] = {
    'name'  : 'gen_tau_eta',
    'title' : ';Gen #tau #eta;a.u.',
    'expr'  : 'gen_tau_eta',
    'nbins' : 100,
    'xmin'  : -6,
    'xmax'  : 6,   
    'cut'   : gen_mu_cut.cut,
}
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



pm.load_histos(histos)
pm.build_histos(ch)
pm.set_overlays(overlays)
pm.plot_name_proto = plot_name_proto
pm.c1 = c1

# pm.histos['n_CSC_S1'].histo.Draw()
# c1.Print('prova.pdf', 'pdf')

pm.plot_all(do_png=True)

# h.histo.Draw()
# c1.Print('prova.pdf', 'pdf')
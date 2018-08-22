import ROOT
import operator
import numpy as np
import scipy, sys
import copy
from array import array
import pandas as pd
import matplotlib.pyplot as plt
import uproot

def show(data, data_format, ientry):
    print '==== EVENT', ientry, '===='
    for idx in range(0, len(data_format)):
        print data_format[idx][0], data_format[idx][1], data[idx][ientry]

def df_idx (dataformat, name):
    idxs = [item for item in dataformat if item[0] == name]
    if len(idxs) == 1:
        return idxs[0]
    raise ValueError('Cannot state idx of' + name + 'in data format')

def to_mpi_pi (x):
    while (x >= np.pi): x -= 2.*np.pi;
    while (x < -np.pi): x += 2.*np.pi;
    return x

# [min, max)
# def findBin (thearr, val):
#     if val < thearr[0]:
#         return -1
#     if val >= thearr[-1]:
#         return len(thearr)
#     for i in range (len(thearr) -1 ):
#         if val >= thearr[i] and val < thearr[i+1]:
#             return i
#     print "I should not be here!!"
#     return 0


fIn = ROOT.TFile.Open('matched_tree_MuMu_flatPt_0PU_23Apr2018.root')
tIn = fIn.Get('tree')
nevents = tIn.GetEntries()
print "Tree has", nevents, "events"
# nevents = 10000

# can parse epression in the usual ROOT style
## the second entry of the dataformat, if valid, means that the type must be converted from 'double'
data_format = (
    ('gen_pt'           , None),
    ('abs(gen_eta)'     , None),
    ('abs(gen_theta)'   , None),
    ('gen_phi'          , None),
    ('gen_charge'       , int),
    ##
    ('trk_pt'           , None),
    ('abs(trk_eta)'     , None),
    ('abs(trk_theta)'   , None),
    ('trk_phi'          , None),
    ##
    ('emtf_pt'          , None),
    ('emtf_xml_pt'      , None),
    ('abs(emtf_eta)'    , None),
    ('abs(emtf_theta)'  , None),
    ('emtf_phi'         , None),
    ('emtf_charge'      , int),
    ##
    ('has_S1'           , bool),
    ('S1_type'          , int),
    ('S1_phi'           , None),
    ('S1_eta'           , None),
    ('S1_theta'         , None),
)

print "... going to fetch data from tree"

##### copy the data to memory. This is super fast, excellent!!
data_buf = [None] * len(data_format)
tIn.SetEstimate(nevents + 1);
for idx, df in enumerate(data_format):
    print '... reading data in', df[0]
    tIn.Draw(df[0],"","goff",nevents,0)
    temp=tIn.GetV1()
    data_buf[idx]=copy.deepcopy(scipy.frombuffer(buffer=temp,dtype='double',count=nevents))

data = np.asarray(data_buf)
dataframe = pd.DataFrame(data, index=[x[0] for x in data_format])
pd.set_option('expand_frame_repr', False)
pd.options.display.max_rows = 10

print "... data moved to memory"
# print data
# print dataframe

### transpose, so that row ==> evt index, column ==> property
dataframe = dataframe.transpose()

print "... dataset transposed"
print dataframe
print dataframe.shape

for name, ttype in data_format:
    if ttype:
        print name , " double --> ", ttype
        dataframe[name] = dataframe[name].astype(ttype)
print ".. types adjusted"

print "... dataset modified"
good_emtf = dataframe['emtf_pt'] > 0
good_trk  = dataframe['trk_pt'] > 0
# dummy_cut = dataframe['trk_pt'] > -999999
dataframe = dataframe[good_emtf & good_trk].copy()
print dataframe
print dataframe.shape

print dataframe.info()
print '...dataframe has', len(dataframe.index), 'events'

print "... adding extra info"
### getting columns, operating, and adding to the dataframe is much faster than jusing dataframe.apply
col_dphi   = dataframe.loc[ : , 'emtf_phi'].subtract(dataframe.loc[ : , 'trk_phi']).apply(to_mpi_pi).abs()
col_deta   = dataframe.loc[ : , 'abs(emtf_eta)'].subtract(dataframe.loc[ : , 'abs(trk_eta)']).abs()
col_dtheta = dataframe.loc[ : , 'abs(emtf_theta)'].subtract(dataframe.loc[ : , 'abs(trk_theta)']).abs()
col_dR     = np.sqrt((col_dphi*col_dphi)+(col_deta*col_deta)) # mega figo! realizza a catena tutte le operazioni

print '...dataframe has', len(dataframe.index), 'events'

print '... appending to df'
dataframe.loc[:, 'delta_phi']   = col_dphi
dataframe.loc[:, 'delta_eta']   = col_deta
dataframe.loc[:, 'delta_theta'] = col_dtheta
dataframe.loc[:, 'delta_R']     = col_dR
print '... appended'

print dataframe
print '...dataframe has', len(dataframe.index), 'events'

print '... making groups'
### definisco il; binning
bins_trk_pt  = np.linspace(start = 2.0, stop = 202.0, num = 200+1)
bins_trk_eta = np.linspace(start = 1.2, stop = 2.4,   num = 10+1)
print '\nbins in pT track:'
print bins_trk_pt
print '\nbins in eta track:'
print bins_trk_eta

print '...dataframe has', len(dataframe.index), 'events'

### definisco categorie sul dataset in base al binning


cut_trk_pt = pd.cut(dataframe.loc[:,'trk_pt'], bins_trk_pt, labels=range(len(bins_trk_pt)-1))
cut_trk_eta = pd.cut(dataframe.loc[:,'abs(trk_eta)'], bins_trk_eta, labels=range(len(bins_trk_eta)-1))

# lab1 = [str(x) for x in range(len(bins_trk_pt)-1)]
# lab2 = [str(x) for x in range(len(bins_trk_eta)-1)]
# cut_trk_pt = pd.cut(dataframe.loc[:,'trk_pt'], bins_trk_pt, labels=lab1)
# cut_trk_eta = pd.cut(dataframe.loc[:,'abs(trk_eta)'], bins_trk_eta, labels=lab2)

### raggruppo il dataset in base alle categorie sopra definite
gpb = dataframe.groupby([cut_trk_pt, cut_trk_eta])

print "...done grouping..."
print '...dataframe has', len(dataframe.index), 'events'

# qA = 'emtf_pt'
# qB = 'abs(emtf_eta)'

qA = 'emtf_pt'
qB = 'abs(emtf_eta)'

toplot_quant = 'delta_R'
quantile_l90 = 0.05
quantile_l99 = 0.005
quantile_l = 0.025 ### 95%
quantile_c = 0.5
quantile_h = 0.975 ### 95%
quantile_h90 = 0.95
quantile_h99 = 0.995

# dataframe.reindex()

# print dataframe.loc[:,'trk_pt']
# print dataframe.loc[0,:]
# print dataframe.columns
# print dataframe.index

# print gpb.indices[0,0]
# print gpb.indices['0','0']

################ nota importante!!!!
###  dataframe.groupby.indices restituisce il NUMERO della riga, e non la chiave che indicizza le righe
###  quindi se ho tagliato su dataset, devo recuperare i singoli bin con iloc e non con loc, o ottengo numeri a caso

# print "... checking by hand"
# for i, idx in enumerate(gpb.indices[0,0]):
# # for i, idx in enumerate(gpb.indices['0','0']):
#     if i < 3:
#         print '..... ', idx
#         print dataframe.loc[idx, :]            
# print dataframe.loc[2578, :]
# print dataframe.loc[78747, :]
# print dataframe.loc[108417, :]

################

print '\n\n================= SUMMARY =================\n\n'
# for ix in range(len(bins_trk_pt)-1):
#     for iy in range(len(bins_trk_eta)-1):
#         print "{:.3f}-{:.3f} {:.3f}-{:.3f} --> pt in {:.3f} {:.3f}, eta in {:.3f} {:.3f}, quantiles {} {} nevents {}".format(
#             bins_trk_pt[ix], bins_trk_pt[ix+1],
#             bins_trk_eta[iy], bins_trk_eta[iy+1],
#             dataframe.loc[ :, qA].iloc[gpb.indices[ix,iy]].min(),
#             dataframe.loc[ :, qA].iloc[gpb.indices[ix,iy]].max(),
#             dataframe.loc[ :, qB].iloc[gpb.indices[ix,iy]].min(),
#             dataframe.loc[ :, qB].iloc[gpb.indices[ix,iy]].max(),
#             dataframe.loc[ :, toplot_quant].iloc[gpb.indices[ix,iy]].quantile(quantile_l),
#             dataframe.loc[ :, toplot_quant].iloc[gpb.indices[ix,iy]].quantile(quantile_h),
#             dataframe.loc[ :, qB].iloc[gpb.indices[ix,iy]].size
#         )


###### dump to an histogram, so that I have a record of the quantiles
###### FIXME: there is maybe a better data format? (e.g., json?)





print '... dumping to histograms'

binning_params = [len(bins_trk_pt)-1, array('d', bins_trk_pt), len(bins_trk_eta)-1, array('d', bins_trk_eta)]

fOut = ROOT.TFile('matching_windows.root', 'recreate')

h_nev      = ROOT.TH2D('h_nev',      'Number of events ;Track p_{T};Track |#eta|', *binning_params)

h_dphi_l   = ROOT.TH2D('h_dphi_l',   '#Delta#varphi   (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l), *binning_params)
h_dtheta_l = ROOT.TH2D('h_dtheta_l', '#Delta#theta    (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l), *binning_params)
h_deta_l   = ROOT.TH2D('h_deta_l',   '#Delta#eta      (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l), *binning_params)
h_dR_l     = ROOT.TH2D('h_dR_l',     '#DeltaR         (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l), *binning_params)

h_dphi_c   = ROOT.TH2D('h_dphi_c',   '#Delta#varphi   (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_c), *binning_params)
h_dtheta_c = ROOT.TH2D('h_dtheta_c', '#Delta#theta    (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_c), *binning_params)
h_deta_c   = ROOT.TH2D('h_deta_c',   '#Delta#eta      (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_c), *binning_params)
h_dR_c     = ROOT.TH2D('h_dR_c',     '#DeltaR         (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_c), *binning_params)

h_dphi_h   = ROOT.TH2D('h_dphi_h',   '#Delta#varphi   (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h), *binning_params)
h_dtheta_h = ROOT.TH2D('h_dtheta_h', '#Delta#theta    (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h), *binning_params)
h_deta_h   = ROOT.TH2D('h_deta_h',   '#Delta#eta      (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h), *binning_params)
h_dR_h     = ROOT.TH2D('h_dR_h',     '#DeltaR         (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h), *binning_params)

h_dphi_delta   = ROOT.TH2D('h_dphi_delta',   '#Delta#varphi   (%.4f window) ;Track p_{T};Track |#eta|' % (quantile_h - quantile_l), *binning_params)
h_dtheta_delta = ROOT.TH2D('h_dtheta_delta', '#Delta#theta    (%.4f window) ;Track p_{T};Track |#eta|' % (quantile_h - quantile_l), *binning_params)
h_deta_delta   = ROOT.TH2D('h_deta_delta',   '#Delta#eta      (%.4f window) ;Track p_{T};Track |#eta|' % (quantile_h - quantile_l), *binning_params)
h_dR_delta     = ROOT.TH2D('h_dR_delta',     '#DeltaR         (%.4f window) ;Track p_{T};Track |#eta|' % (quantile_h - quantile_l), *binning_params)

#### other quantiles
h_dphi_l90   = ROOT.TH2D('h_dphi_l90',   '#Delta#varphi   (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l90), *binning_params)
h_dtheta_l90 = ROOT.TH2D('h_dtheta_l90', '#Delta#theta    (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l90), *binning_params)
h_deta_l90   = ROOT.TH2D('h_deta_l90',   '#Delta#eta      (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l90), *binning_params)
h_dR_l90     = ROOT.TH2D('h_dR_l90',     '#DeltaR         (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l90), *binning_params)

h_dphi_l99   = ROOT.TH2D('h_dphi_l99',   '#Delta#varphi   (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l99), *binning_params)
h_dtheta_l99 = ROOT.TH2D('h_dtheta_l99', '#Delta#theta    (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l99), *binning_params)
h_deta_l99   = ROOT.TH2D('h_deta_l99',   '#Delta#eta      (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l99), *binning_params)
h_dR_l99     = ROOT.TH2D('h_dR_l99',     '#DeltaR         (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_l99), *binning_params)

h_dphi_h90   = ROOT.TH2D('h_dphi_h90',   '#Delta#varphi   (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h90), *binning_params)
h_dtheta_h90 = ROOT.TH2D('h_dtheta_h90', '#Delta#theta    (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h90), *binning_params)
h_deta_h90   = ROOT.TH2D('h_deta_h90',   '#Delta#eta      (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h90), *binning_params)
h_dR_h90     = ROOT.TH2D('h_dR_h90',     '#DeltaR         (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h90), *binning_params)

h_dphi_h99   = ROOT.TH2D('h_dphi_h99',   '#Delta#varphi   (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h99), *binning_params)
h_dtheta_h99 = ROOT.TH2D('h_dtheta_h99', '#Delta#theta    (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h99), *binning_params)
h_deta_h99   = ROOT.TH2D('h_deta_h99',   '#Delta#eta      (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h99), *binning_params)
h_dR_h99     = ROOT.TH2D('h_dR_h99',     '#DeltaR         (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h99), *binning_params)


h_effs_cumul_phi = ROOT.TH1D('h_effs_cumul_phi', "h_effs_cumul_phi", 200, 0.80, 1.0)
h_effs_cumul_theta = ROOT.TH1D('h_effs_cumul_theta', "h_effs_cumul_theta", 200, 0.80, 1.0)
# h_effs_cumul_both = ROOT.TH1D('h_effs_cumul_both', "h_effs_cumul_both", 200, 0.80, 1.0)

histos_dphis = []
histos_dthetas = []

arr_dphi_l   = np.zeros((len(bins_trk_pt)-1, len(bins_trk_eta)-1))
arr_dtheta_l = np.zeros((len(bins_trk_pt)-1, len(bins_trk_eta)-1))
arr_dphi_h   = np.zeros((len(bins_trk_pt)-1, len(bins_trk_eta)-1))
arr_dtheta_h = np.zeros((len(bins_trk_pt)-1, len(bins_trk_eta)-1))

n_tot_used = 0
n_tot_sel_dphi = 0
n_tot_sel_dtheta = 0

for ix in range(len(bins_trk_pt)-1):
    for iy in range(len(bins_trk_eta)-1):
        ibinx = ix+1
        ibiny = iy+1
        nev = dataframe.loc[ :, 'delta_R'].iloc[gpb.indices[ix,iy]].size
        n_tot_used += nev

        erel = 1./np.sqrt(nev) ### not sure this is a good estimation of the error... probably I should xcheck with toys

        h_nev       .SetBinContent(ibinx, ibiny, nev)
        h_dphi_l    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_l))
        h_dtheta_l  .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_l))
        h_deta_l    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_eta']   .iloc[gpb.indices[ix,iy]].quantile(quantile_l))
        h_dR_l      .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_R']     .iloc[gpb.indices[ix,iy]].quantile(quantile_l))
        h_dphi_c    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_c))
        h_dtheta_c  .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_c))
        h_deta_c    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_eta']   .iloc[gpb.indices[ix,iy]].quantile(quantile_c))
        h_dR_c      .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_R']     .iloc[gpb.indices[ix,iy]].quantile(quantile_c))
        h_dphi_h    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_h))
        h_dtheta_h  .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_h))
        h_deta_h    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_eta']   .iloc[gpb.indices[ix,iy]].quantile(quantile_h))
        h_dR_h      .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_R']     .iloc[gpb.indices[ix,iy]].quantile(quantile_h))

        h_dphi_l90    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_l90))
        h_dtheta_l90  .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_l90))
        h_deta_l90    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_eta']   .iloc[gpb.indices[ix,iy]].quantile(quantile_l90))
        h_dR_l90      .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_R']     .iloc[gpb.indices[ix,iy]].quantile(quantile_l90))
        h_dphi_l99    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_l99))
        h_dtheta_l99  .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_l99))
        h_deta_l99    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_eta']   .iloc[gpb.indices[ix,iy]].quantile(quantile_l99))
        h_dR_l99      .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_R']     .iloc[gpb.indices[ix,iy]].quantile(quantile_l99))

        h_dphi_h90    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_h90))
        h_dtheta_h90  .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_h90))
        h_deta_h90    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_eta']   .iloc[gpb.indices[ix,iy]].quantile(quantile_h90))
        h_dR_h90      .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_R']     .iloc[gpb.indices[ix,iy]].quantile(quantile_h90))
        h_dphi_h99    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_h99))
        h_dtheta_h99  .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_h99))
        h_deta_h99    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_eta']   .iloc[gpb.indices[ix,iy]].quantile(quantile_h99))
        h_dR_h99      .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_R']     .iloc[gpb.indices[ix,iy]].quantile(quantile_h99))


        h_nev       .SetBinError(ibinx, ibiny, erel * h_nev.      GetBinContent(ibinx, ibiny))
        h_dphi_l    .SetBinError(ibinx, ibiny, erel * h_dphi_l.   GetBinContent(ibinx, ibiny))
        h_dtheta_l  .SetBinError(ibinx, ibiny, erel * h_dtheta_l. GetBinContent(ibinx, ibiny))
        h_deta_l    .SetBinError(ibinx, ibiny, erel * h_deta_l.   GetBinContent(ibinx, ibiny))
        h_dR_l      .SetBinError(ibinx, ibiny, erel * h_dR_l.     GetBinContent(ibinx, ibiny))
        h_dphi_c    .SetBinError(ibinx, ibiny, erel * h_dphi_c.   GetBinContent(ibinx, ibiny))
        h_dtheta_c  .SetBinError(ibinx, ibiny, erel * h_dtheta_c. GetBinContent(ibinx, ibiny))
        h_deta_c    .SetBinError(ibinx, ibiny, erel * h_deta_c.   GetBinContent(ibinx, ibiny))
        h_dR_c      .SetBinError(ibinx, ibiny, erel * h_dR_c.     GetBinContent(ibinx, ibiny))
        h_dphi_h    .SetBinError(ibinx, ibiny, erel * h_dphi_h.   GetBinContent(ibinx, ibiny))
        h_dtheta_h  .SetBinError(ibinx, ibiny, erel * h_dtheta_h. GetBinContent(ibinx, ibiny))
        h_deta_h    .SetBinError(ibinx, ibiny, erel * h_deta_h.   GetBinContent(ibinx, ibiny))
        h_dR_h      .SetBinError(ibinx, ibiny, erel * h_dR_h.     GetBinContent(ibinx, ibiny))

        h_dphi_l90    .SetBinError(ibinx, ibiny, erel * h_dphi_l90.   GetBinContent(ibinx, ibiny))
        h_dtheta_l90  .SetBinError(ibinx, ibiny, erel * h_dtheta_l90. GetBinContent(ibinx, ibiny))
        h_deta_l90    .SetBinError(ibinx, ibiny, erel * h_deta_l90.   GetBinContent(ibinx, ibiny))
        h_dR_l90      .SetBinError(ibinx, ibiny, erel * h_dR_l90.     GetBinContent(ibinx, ibiny))
        h_dphi_l99    .SetBinError(ibinx, ibiny, erel * h_dphi_l99.   GetBinContent(ibinx, ibiny))
        h_dtheta_l99  .SetBinError(ibinx, ibiny, erel * h_dtheta_l99. GetBinContent(ibinx, ibiny))
        h_deta_l99    .SetBinError(ibinx, ibiny, erel * h_deta_l99.   GetBinContent(ibinx, ibiny))
        h_dR_l99      .SetBinError(ibinx, ibiny, erel * h_dR_l99.     GetBinContent(ibinx, ibiny))
        h_dphi_h90    .SetBinError(ibinx, ibiny, erel * h_dphi_h90.   GetBinContent(ibinx, ibiny))
        h_dtheta_h90  .SetBinError(ibinx, ibiny, erel * h_dtheta_h90. GetBinContent(ibinx, ibiny))
        h_deta_h90    .SetBinError(ibinx, ibiny, erel * h_deta_h90.   GetBinContent(ibinx, ibiny))
        h_dR_h90      .SetBinError(ibinx, ibiny, erel * h_dR_h90.     GetBinContent(ibinx, ibiny))
        h_dphi_h99    .SetBinError(ibinx, ibiny, erel * h_dphi_h99.   GetBinContent(ibinx, ibiny))
        h_dtheta_h99  .SetBinError(ibinx, ibiny, erel * h_dtheta_h99. GetBinContent(ibinx, ibiny))
        h_deta_h99    .SetBinError(ibinx, ibiny, erel * h_deta_h99.   GetBinContent(ibinx, ibiny))
        h_dR_h99      .SetBinError(ibinx, ibiny, erel * h_dR_h99.     GetBinContent(ibinx, ibiny))

        #### making a cross check about the quantiles
        
        t_phi_l = h_dphi_l.GetBinContent(ibinx, ibiny)
        t_phi_h = h_dphi_h.GetBinContent(ibinx, ibiny)
        t_theta_l = h_dtheta_l.GetBinContent(ibinx, ibiny)
        t_theta_h = h_dtheta_h.GetBinContent(ibinx, ibiny)

        # arr_dphi_l   [ix, iy] = dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_l)
        # arr_dtheta_l [ix, iy] = dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_l)
        # arr_dphi_h   [ix, iy] = dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_h)
        # arr_dtheta_h [ix, iy] = dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_h)

        arr_dphi_l   [ix, iy] = t_phi_l
        arr_dtheta_l [ix, iy] = t_theta_l
        arr_dphi_h   [ix, iy] = t_phi_h
        arr_dtheta_h [ix, iy] = t_theta_h


        ### priting the thresholds as a xc
        # print ibinx, ibiny, '{:6f} {:6f} {:6f} {:6f}'.format(t_phi_l, t_phi_h, t_theta_l, t_theta_h)
        
        therow_phi   = dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]]
        therow_theta = dataframe.loc[ :, 'delta_theta']   .iloc[gpb.indices[ix,iy]]

        n_in_phi   = ( (therow_phi > t_phi_l)   & (therow_phi < t_phi_h) ).sum()
        n_in_theta = ( (therow_theta > t_theta_l) & (therow_theta < t_theta_h) ).sum()

        n_tot_sel_dphi += n_in_phi
        n_tot_sel_dtheta += n_in_theta
        
        #### cross check
        # n_in_phi_xc = 0
        # n_in_theta_xc = 0
        # for vv in dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]]:
        #     if vv > t_phi_l and vv < t_phi_h: n_in_phi_xc += 1
        # for vv in dataframe.loc[ :, 'delta_theta']   .iloc[gpb.indices[ix,iy]]:
        #     if vv > t_theta_l and vv < t_theta_h: n_in_theta_xc += 1

        # print n_in_phi, ' =?=' , n_in_phi_xc
        # print n_in_theta, ' =?=' , n_in_theta_xc

        h_effs_cumul_phi.Fill(1.*n_in_phi/therow_phi.size)
        h_effs_cumul_theta.Fill(1.*n_in_theta/therow_theta.size)

        h_dphis = ROOT.TH1D("h_dphis_%i_%i" % (ibinx, ibiny), "h_dphis_%i_%i" % (ibinx, ibiny), 500, 0.5*therow_phi.min(), 1.5*therow_phi.max())
        h_dthetas = ROOT.TH1D("h_dthetas_%i_%i" % (ibinx, ibiny), "h_dthetas_%i_%i" % (ibinx, ibiny), 500, 0.5*therow_theta.min(), 1.5*therow_theta.max())

        for nn in therow_phi: h_dphis.Fill(nn)
        for nn in therow_theta: h_dthetas.Fill(nn)

        histos_dphis.append(h_dphis)
        histos_dthetas.append(h_dthetas)

        # red_phi    = ( (therow_phi > t_phi_l)   & (therow_phi < t_phi_h) )
        # red_theta  = ( (therow_theta > t_theta_l) & (therow_theta < t_theta_h) )


        #### very suspicious... red_phi and red_theta vectors are not the same, but "True" entries are always in the same number        
        # for i in range(red_phi.size):
        #     print i, red_phi.iloc[i], red_theta.iloc[i]

        # n_in_phi_bis = 0
        # n_in_theta_bis = 0
        # for i in red_phi:
        #     if i:
        #         n_in_phi_bis += 1
        # for i in red_theta:
        #     if i:
        #         n_in_theta_bis += 1

        # print n_in_phi, n_in_phi_bis 
        # print n_in_theta, n_in_theta_bis 
        # print ""

        # print "ptbin ", ibinx, "etabin ", ibiny
        # print "eff phi :", 100.*n_in_phi/therow_phi.size, "%"
        # print "eff theta :", 100.*n_in_theta/therow_theta.size, "%"
        # print ""

        # print t_phi_l
        # print t_phi_h
        # print t_theta_l
        # print t_theta_h

        # print n_in_phi
        # print n_in_theta
        # print therow_phi
        # print therow_theta
        # print ( (therow_phi > t_phi_l)   & (therow_phi < t_phi_h) )
        # print ( (therow_theta > t_theta_l) & (therow_theta < t_theta_h) )
        # print ""

print "\n\n\n =============================== \n\n\n"
for ix in range(len(bins_trk_pt)-1):
    for iy in range(len(bins_trk_eta)-1):
        ibinx = ix+1
        ibiny = iy+1
        t_phi_l = h_dphi_l.GetBinContent(ibinx, ibiny)
        t_phi_h = h_dphi_h.GetBinContent(ibinx, ibiny)
        t_theta_l = h_dtheta_l.GetBinContent(ibinx, ibiny)
        t_theta_h = h_dtheta_h.GetBinContent(ibinx, ibiny)

        ### priting the thresholds as a xc
        print ibinx, ibiny, '{:6f} {:6f} {:6f} {:6f}'.format(t_phi_l, t_phi_h, t_theta_l, t_theta_h)


## compute the deltas
h_dphi_delta.Add(h_dphi_h)
h_dtheta_delta.Add(h_dtheta_h)
h_deta_delta.Add(h_deta_h)
h_dR_delta.Add(h_dR_h)
h_dphi_delta.Add(h_dphi_l, -1)
h_dtheta_delta.Add(h_dtheta_l, -1)
h_deta_delta.Add(h_deta_l, -1)
h_dR_delta.Add(h_dR_l, -1)



print '... drawing the plots'
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetBorderSize(3)
c1.SetLeftMargin(0.15)
c1.SetRightMargin(0.15)
c1.SetBottomMargin(0.15)
c1.SetLogz()

h_nev.Draw('colz')
c1.Print('matching_plots/h_nev.pdf', 'pdf')

h_dphi_l.Draw('colz')
c1.Print('matching_plots/h_dphi_l.pdf', 'pdf')

h_dtheta_l.Draw('colz')
c1.Print('matching_plots/h_dtheta_l.pdf', 'pdf')

h_dR_l.Draw('colz')
c1.Print('matching_plots/h_dR_l.pdf', 'pdf')

h_dphi_h.Draw('colz')
c1.Print('matching_plots/h_dphi_h.pdf', 'pdf')

h_dtheta_h.Draw('colz')
c1.Print('matching_plots/h_dtheta_h.pdf', 'pdf')

h_dR_h.Draw('colz')
c1.Print('matching_plots/h_dR_h.pdf', 'pdf')

h_dphi_delta.Draw('colz')
c1.Print('matching_plots/h_dphi_delta.pdf', 'pdf')

h_dtheta_delta.Draw('colz')
c1.Print('matching_plots/h_dtheta_delta.pdf', 'pdf')

h_dR_delta.Draw('colz')
c1.Print('matching_plots/h_dR_delta.pdf', 'pdf')

fOut.Write()

print "... done. I used in total", n_tot_used, 'events out of a preselected dataset of', dataframe.shape, 'events'
print "... cumulative eff in dphi is", 100.*n_tot_sel_dphi/n_tot_used, '% (' , n_tot_sel_dphi, '/', n_tot_used, ')'
print "... cumulative eff in dtheta is", 100.*n_tot_sel_dtheta/n_tot_used, '% (' , n_tot_sel_dtheta, '/', n_tot_used, ')'

############################################################################################
############################################################################################
############################################################################################
### cross check the efficiencies

if True:
    print "...... NOW A CROSS CHECK"

    tIn_xc  = uproot.open('matched_tree_MuMu_flatPt_0PU_23Apr2018.root')['tree']
    keys = tIn_xc.keys()
    data = tIn_xc.arrays(keys)
    totEvts = data['gen_pt'].size
    print "tree has ", totEvts, 'entries', type(totEvts)

    nx = h_dphi_l.GetNbinsX()
    ny = h_dphi_l.GetNbinsY()
    print "pT  histo boundaries:", h_dphi_l.GetXaxis().GetBinLowEdge(1), h_dphi_l.GetXaxis().GetBinLowEdge(nx+1)
    print "eta histo boundaries:", h_dphi_l.GetYaxis().GetBinLowEdge(1), h_dphi_l.GetYaxis().GetBinLowEdge(ny+1)

    nevents = 0
    n_emtf = 0
    n_trk = 0
    n_emtf_and_trk = 0
    n_pass_phi = 0
    n_pass_theta = 0
    n_pass_theta_and_phi = 0

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

        # if binx == 0 or binx > nx or biny == 0 or biny > ny:
        #     print "under/over flow ", binx, biny, "(", trk_pt, trk_eta, ")", "from", nx, ny

        # if biny == 0 or biny > ny:
        #     print "under/over flow ", binx, biny, "(", trk_pt, trk_eta, ")", "from", nx, ny

        ## read from the histos --> same result as xcheck        
        # wd_theta_l = h_dtheta_l.GetBinContent(binx, biny)
        # wd_theta_h = h_dtheta_h.GetBinContent(binx, biny)
        # wd_phi_l = h_dphi_l.GetBinContent(binx, biny)
        # wd_phi_h = h_dphi_h.GetBinContent(binx, biny)

        ### use stored floats
        wd_theta_l = arr_dtheta_l[binx-1][biny-1]
        wd_theta_h = arr_dtheta_h[binx-1][biny-1]
        wd_phi_l = arr_dphi_l[binx-1][biny-1]
        wd_phi_h = arr_dphi_h[binx-1][biny-1]

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

        # eff_plot_pt.Fill ((pass_phi and pass_theta), gen_pt)
        # eff_plot_eta.Fill ((pass_phi and pass_theta), gen_eta)

        ##### fill distros xcheck plots
        # binx = findBin(bins_trk_pt, trk_pt)
        # biny = findBin(bins_trk_eta, abs(trk_eta))

        # if binx >= 0 and binx < len(bins_trk_pt) and biny >= 0 and biny < len(bins_trk_eta):
        #     binx += 1
        #     biny += 1
        #     histos_dthetas[(binx, biny)].Fill(dtheta)
        #     histos_dphis[(binx, biny)].Fill(dphi)


    print "*** efficiencies [%] *** . From ", nevents , "preselected events"
    print "EMTF             " , 100.*n_emtf         / nevents 
    print "TRK              " , 100.*n_trk          / nevents 
    print "EMTF + TRK       " , 100.*n_emtf_and_trk / nevents 
    print "pass phi         " , 100.*n_pass_phi            / nevents, '(', n_pass_phi, '/', nevents, ')'
    print "pass theta       " , 100.*n_pass_theta          / nevents, '(', n_pass_theta, '/', nevents, ')'
    print "pass phi + theta " , 100.*n_pass_theta_and_phi  / nevents, '(', n_pass_theta_and_phi, '/', nevents, ')'
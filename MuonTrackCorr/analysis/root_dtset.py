import ROOT
import operator
import numpy as np
import scipy, sys
import copy
from array import array
import pandas as pd
import matplotlib.pyplot as plt

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
quantile_l = 0.025
quantile_h = 0.975

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
h_dphi_h   = ROOT.TH2D('h_dphi_h',   '#Delta#varphi   (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h), *binning_params)
h_dtheta_h = ROOT.TH2D('h_dtheta_h', '#Delta#theta    (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h), *binning_params)
h_deta_h   = ROOT.TH2D('h_deta_h',   '#Delta#eta      (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h), *binning_params)
h_dR_h     = ROOT.TH2D('h_dR_h',     '#DeltaR         (%.4f quantile) ;Track p_{T};Track |#eta|' % (quantile_h), *binning_params)

h_dphi_delta   = ROOT.TH2D('h_dphi_delta',   '#Delta#varphi   (%.4f window) ;Track p_{T};Track |#eta|' % (quantile_h - quantile_l), *binning_params)
h_dtheta_delta = ROOT.TH2D('h_dtheta_delta', '#Delta#theta    (%.4f window) ;Track p_{T};Track |#eta|' % (quantile_h - quantile_l), *binning_params)
h_deta_delta   = ROOT.TH2D('h_deta_delta',   '#Delta#eta      (%.4f window) ;Track p_{T};Track |#eta|' % (quantile_h - quantile_l), *binning_params)
h_dR_delta     = ROOT.TH2D('h_dR_delta',     '#DeltaR         (%.4f window) ;Track p_{T};Track |#eta|' % (quantile_h - quantile_l), *binning_params)


for ix in range(len(bins_trk_pt)-1):
    for iy in range(len(bins_trk_eta)-1):
        ibinx = ix+1
        ibiny = iy+1
        nev = dataframe.loc[ :, 'delta_R'].iloc[gpb.indices[ix,iy]].size
        
        erel = 1./np.sqrt(nev) ### not sure this is a good estimation of the error... probably I should xcheck with toys

        h_nev       .SetBinContent(ibinx, ibiny, nev)
        h_dphi_l    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_l))
        h_dtheta_l  .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_l))
        h_deta_l    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_eta']   .iloc[gpb.indices[ix,iy]].quantile(quantile_l))
        h_dR_l      .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_R']     .iloc[gpb.indices[ix,iy]].quantile(quantile_l))
        h_dphi_h    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_phi']   .iloc[gpb.indices[ix,iy]].quantile(quantile_h))
        h_dtheta_h  .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_theta'] .iloc[gpb.indices[ix,iy]].quantile(quantile_h))
        h_deta_h    .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_eta']   .iloc[gpb.indices[ix,iy]].quantile(quantile_h))
        h_dR_h      .SetBinContent(ibinx, ibiny, dataframe.loc[ :, 'delta_R']     .iloc[gpb.indices[ix,iy]].quantile(quantile_h))

        h_nev       .SetBinError(ibinx, ibiny, erel * h_nev.      GetBinContent(ibinx, ibiny))
        h_dphi_l    .SetBinError(ibinx, ibiny, erel * h_dphi_l.   GetBinContent(ibinx, ibiny))
        h_dtheta_l  .SetBinError(ibinx, ibiny, erel * h_dtheta_l. GetBinContent(ibinx, ibiny))
        h_deta_l    .SetBinError(ibinx, ibiny, erel * h_deta_l.   GetBinContent(ibinx, ibiny))
        h_dR_l      .SetBinError(ibinx, ibiny, erel * h_dR_l.     GetBinContent(ibinx, ibiny))
        h_dphi_h    .SetBinError(ibinx, ibiny, erel * h_dphi_h.   GetBinContent(ibinx, ibiny))
        h_dtheta_h  .SetBinError(ibinx, ibiny, erel * h_dtheta_h. GetBinContent(ibinx, ibiny))
        h_deta_h    .SetBinError(ibinx, ibiny, erel * h_deta_h.   GetBinContent(ibinx, ibiny))
        h_dR_h      .SetBinError(ibinx, ibiny, erel * h_dR_h.     GetBinContent(ibinx, ibiny))

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
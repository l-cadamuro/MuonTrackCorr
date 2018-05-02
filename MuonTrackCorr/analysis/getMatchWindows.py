import ROOT
import operator
import numpy as np
import scipy, sys
import copy
from array import array
import pandas as pd

def show(data, data_format, ientry):
    print '==== EVENT', ientry, '===='
    for idx in range(0, len(data_format)):
        print data_format[idx][0], data_format[idx][1], data[idx][ientry]

def df_idx (dataformat, name):
    idxs = [item for item in dataformat if item[0] == name]
    if len(idxs) == 1:
        return idxs[0]
    raise ValueError('Cannot state idx of' + name + 'in data format')

fIn = ROOT.TFile.Open('plots_JFsynch_pt20_eta1p2_2p4_scaledPt_tree.root')
tIn = fIn.Get('tree')
nevents = tIn.GetEntries()
print "Tree has", nevents, "events"
# nevents = 10000


##### FIXME: a preselection of events might be needed

######### dump all the data to memory
# data_format = (
#     ('gen_pt'        , 'double'),
#     ('gen_eta'       , 'double'),
#     ('gen_theta'     , 'double'),
#     ('gen_phi'       , 'double'),
#     ('trk_pt'        , 'double'),
#     ('trk_eta'       , 'double'),
#     ('trk_theta'     , 'double'),
#     ('trk_phi'       , 'double'),
#     ('emtf_pt'       , 'double'),
#     ('emtf_xml_pt'   , 'double'),
#     ('emtf_eta'      , 'double'),
#     ('emtf_theta'    , 'double'),
#     ('emtf_phi'      , 'double'),
# )

# can parse epression in the usual ROOT style
data_format = (
    ('gen_pt'           , 'double'),
    ('abs(gen_eta)'     , 'double'),
    ('abs(gen_theta)'   , 'double'),
    ('gen_phi'          , 'double'),
    ('trk_pt'           , 'double'),
    ('abs(trk_eta)'     , 'double'),
    ('abs(trk_theta)'   , 'double'),
    ('trk_phi'          , 'double'),
    ('emtf_pt'          , 'double'),
    ('emtf_xml_pt'      , 'double'),
    ('abs(emtf_eta)'    , 'double'),
    ('abs(emtf_theta)'  , 'double'),
    ('emtf_phi'         , 'double'),
)

print "... going to fetch data from tree"

##### copy the data to memory. This is super fast, excellent!!
data_buf = [None] * len(data_format)
tIn.SetEstimate(nevents + 1);
for idx, df in enumerate(data_format):
    print '... reading data in', df[0]
    tIn.Draw(df[0],"","goff",nevents,0)
    temp=tIn.GetV1()
    data_buf[idx]=copy.deepcopy(scipy.frombuffer(buffer=temp,dtype=df[1],count=nevents))

data = np.asarray(data_buf)
dataframe = pd.DataFrame(data, index=[x[0] for x in data_format])

print "... data moved to memory"
# print data
# print dataframe

### transpose, so that row ==> evt index, column ==> property
dataframe = dataframe.transpose()
### with the following llines, results make no sense
# good1 = dataframe['emtf_pt'] > 0.0
# good2 = dataframe['trk_pt'] > 0.0
# dataframe = dataframe[dataframe['emtf_pt'] > 0.0]
#dataframe = dataframe[dataframe['emtf_pt'] > 0]

print "... dataset transposed"
print dataframe
# print "... adding separations"
# print '...dphi'
# dataframe['delta_phi'] = dataframe.apply(lambda x: ROOT.TVector2.Phi_mpi_pi(x['emtf_phi'] - x['trk_phi']), axis=1)
# print '...deta'
# dataframe['delta_eta'] = dataframe.apply(lambda x:                          x['abs(emtf_eta)'] - x['abs(trk_eta)'],  axis=1)
# print '...dR'
# dataframe['delta_R']   = dataframe.apply(lambda x: ROOT.TMath.Sqrt(x['delta_phi']*x['delta_phi'] + x['delta_eta']*x['delta_eta']), axis=1)

print "... extra info added"

# print 'running pandas version:', pd.__version__

# show(data, data_format, nevents-1)

# print "LAST EVENT OF DATAFRAME"
# print dataframe[nevents-1]
print
print dataframe.info()
print
# ## and the data are OK!
# # show(data, data_format, 0)
# # print ''
# # show(data, data_format, 10)
# # print ''
# # show(data, data_format, 100)

# ### and also the length
# # ts = 0
# # for i in range(0,nevents):
# #     ts += data[3][i]
# # print ts
# # for i in range(0,len(data)):
# #     print len(data[i])

# ##### make bins of the phase space
# #### note that this makes nsteps, but I want nbins so ask num=nbin+1

bins_trk_pt  = np.linspace(start = 2.0, stop = 202.0, num = 200+1)
bins_trk_eta = np.linspace(start = 1.2, stop = 2.4,   num = 20+1)

print 'bins_trk_pt'
print bins_trk_pt
print
print 'bins_trk_eta'
print bins_trk_eta
print

print "...making cut..."

### create the cuts that will define caregories in my dataset
### note that I am explicitely giving a progressive bin number as labels so that is easy to index afterwards
cut_trk_pt = pd.cut(dataframe['trk_pt'], bins_trk_pt, labels=range(len(bins_trk_pt)-1))
cut_trk_eta = pd.cut(dataframe['abs(trk_eta)'], bins_trk_eta, labels=range(len(bins_trk_eta)-1))

print "...cut done..."
print type(dataframe['trk_pt'])
print type(cut_trk_pt)
print type(cut_trk_eta)
print 'cut_trk_pt'
print cut_trk_pt
# print cut_trk_pt.labels
print 
print 'cut_trk_eta'
print cut_trk_eta

print "...going to group..."

# quantity = dataframe['emtf_phi'] ### FIXME - to replace with deltaR/deltaPhi/etc...
# quantity = dataframe
# print quantity
# print "TIPO::: ", type(quantity)
gpb = dataframe.groupby([cut_trk_pt, cut_trk_eta])

print "...done grouping..."

# print type(gpb.indices)
# print gpb.keys
# print gpb.indices
# print gpb.indices

#### tutti gli indici nel bin 0,0
print '...idxs...'
print gpb.indices[0,0]
#### tutti i valori nel bin 0,0
print '...values...'
print dataframe['trk_pt'][gpb.indices[0,0]].min(), dataframe['trk_pt'][gpb.indices[0,0]].max()
print dataframe['abs(trk_eta)'][gpb.indices[0,0]].min(), dataframe['abs(trk_eta)'][gpb.indices[0,0]].max()

print dataframe['emtf_pt'][gpb.indices[0,0]].quantile(0.05), dataframe['emtf_pt'][gpb.indices[0,0]].quantile(0.95)

###################
print '\n\n================= SUMMARY =================\n\n'
for ix in range(len(bins_trk_pt)-1):
    for iy in range(len(bins_trk_eta)-1):
        print "{:.3f}-{:.3f} {:.3f}-{:.3f} --> {:.3f} {:.3f}".format(
            bins_trk_pt[ix], bins_trk_pt[ix+1],
            bins_trk_eta[iy], bins_trk_eta[iy+1],
            dataframe['emtf_pt'][gpb.indices[ix,iy]].mean(),
            dataframe['abs(emtf_eta)'][gpb.indices[ix,iy]].mean()
        )
        # print dataframe['emtf_pt'][gpb.indices[ix,iy]]


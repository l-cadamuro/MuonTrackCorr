import ROOT
# import root_numpy ## to dump a tree into numpy array
import uproot ## to dump a tree into numpy array

def vals_to_ostring(data, df, iEv, itype, iobj, valFormat = '{:10.1f}'):
    ostring = "{:10} {:10} {:10}"
    for ifield in range(len(df)):
        ostring += ' ' + valFormat
    data = [float(x) for x in data]
    ostring = ostring.format(iEv, itype, iobj, *data)
    return ostring

def eta_to_theta(x):
    #  give theta in rad 
    return (2. * ROOT.TMath.ATan(ROOT.TMath.Exp(-1.*x)))

def deg_to_rad(x):
    return (x * ROOT.TMath.Pi()/180.)

def to_mpi_pi(x):
    pi    = ROOT.TMath.Pi()
    twopi = 2.*pi
    while (x >= pi):
        x = x - twopi
    while (x < -pi):
        x = x + twopi;
    return x

def saturate(n, nbits):
    max_v = 2**nbits -1
    if n > max_v:
        n = max_v
    return n

def quantize(n, scale):
    x = float(n)/float(scale)
    r = int(round(x))
    
    return r


# trk_obj  = ['L1TT_trk_pt', 'L1TT_trk_eta', 'L1TT_trk_phi', 'L1TT_trk_charge', 'L1TT_trk_chi2', 'L1TT_trk_nstubs']
trk_obj  = ['L1TT_trk_pt', 'L1TT_trk_eta', 'L1TT_trk_phi', 'L1TT_trk_charge', 'L1TT_trk_chi2']
# muon_obj = ['EMTF_mu_pt',  'EMTF_mu_eta', 'EMTF_mu_phi', 'EMTF_mu_charge']
muon_obj = ['L1_TkMu_pt',  'L1_TkMu_eta', 'L1_TkMu_phi', 'L1_TkMu_charge']
# muon_obj = ['EMTF_mu_pt', 'EMTF_mu_theta', 'EMTF_mu_phi', 'EMTF_mu_charge']

## functions that will be applied on the value of the number extracted above
transformations_to_apply = {
    'EMTF_mu_phi'     : (lambda x: to_mpi_pi(deg_to_rad(x)) ),
    'L1TT_trk_phi'    : to_mpi_pi, 
    'EMTF_mu_charge'  : (lambda x: 1 if x > 0 else 0),
    'L1TT_trk_charge' : (lambda x: 1 if x > 0 else 0),
}

## for quantisations
pi = ROOT.TMath.Pi()
lsb_nbits = {
    'L1TT_trk_pt'     : (0.25,      15),
    'L1TT_trk_eta'    : (2.*pi/2**9, 9),
    'L1TT_trk_phi'    : (2.*pi/2**9, 9),
    'L1TT_trk_charge' : (1, 1),
    'L1TT_trk_chi2'   : (1, 4), # FIXME
    ###
    'EMTF_mu_pt'      : (0.25,      15),
    'EMTF_mu_eta'     : (2.*pi/2**9, 9),  
    'EMTF_mu_phi'     : (2.*pi/2**9, 9),  
    'EMTF_mu_charge'  : (1, 1),
    ###
    'L1_TkMu_pt'      : (0.25,      15),
    'L1_TkMu_eta'     : (2.*pi/2**9, 9),  
    'L1_TkMu_phi'     : (2.*pi/2**9, 9),  
    'L1_TkMu_charge'  : (1, 1),

}


print '... starting'

# values = root_numpy.root2array('root://cmseos.fnal.gov//store/user/lcadamur/L1MuTrks_ntuples/SingleMu_FlatPt-2to100_L1TPU200_12Ott_DWcorr_CMSSWdefaultNoRelax/output/ntuple_0.root',
#         'Ntuplizer/MuonTrackTree')

values    = uproot.open('ntuple_singleMu_200.root')['Ntuplizer/MuonTrackTree']
print '... input opened'

ofilename = 'mu_track_infolist.txt'
fout = open(ofilename, 'w')

nEv = -1
if nEv > len(values) and nEv > 0:
    print "... you requeste", nEv, "events but input tree only has", len(values), "values"
    nEv = len(values)

#############################################################################

ntrk_per_clk = 18 # 18 tracks per clokc
ntmt         = 18 # number of tmt periods over which a track gets sent

ntrk = ntrk_per_clk * ntmt
nmu  = 18 ## 18 muons

debug = False

#############################################################################


# n_trk  = values[iEv]['n_L1TT_trk']
# n_muon = values[iEv]['n_EMTF_mu']

# dataset   = values.pandas.df(entrystop = nEv)
dataset   = values.pandas.df()

if nEv < 0:
    nEv = len(dataset)

print '... will generate patterns for ', nEv, 'events'

for iEv in range(0, nEv):

    if iEv % 500 == 0:
        print "...", iEv, '/', nEv

    ## dicts with key -> all tracks_prop
    trk_vals = {field : dataset[field][iEv] for field in trk_obj}
    mu_vals  = {field : dataset[field][iEv] for field in muon_obj}

    n_trk_read = len(trk_vals.values()[0])
    n_mu_read  = len(mu_vals.values()[0])

    ## now dump all to a file
    #1) muons first

    null_mu  = [0 for x in muon_obj]
    null_trk = [0 for x in trk_obj]

    ## the list of all the values to write
    ## each value is a list of values
    mus_to_write = []
    trks_to_write = []

    ## prepare all the nmu output muons
    
    for imu in range(0, nmu):
        this_mu = list(null_mu)
        if imu < n_mu_read:
            for ifield, field in enumerate(muon_obj):

                v = mu_vals[field][imu]
                if field in transformations_to_apply:
                    v = transformations_to_apply[field](v)
                
                lsb, nbits = lsb_nbits[field]
                v = quantize(v, lsb)
                v = saturate(v, nbits)
                v = int(v)

                this_mu[ifield] = v

            if debug:
                print ".... EV nr ", iEv, ' imu : ', imu, 'vals = ', this_mu
        
        mus_to_write.append(this_mu)

    for itrk in range(0, ntrk):
        this_trk = list(null_trk)
        if itrk < n_trk_read:
            for ifield, field in enumerate(trk_obj):
                v = trk_vals[field][itrk]
                if field in transformations_to_apply:
                    v = transformations_to_apply[field](v)

                lsb, nbits = lsb_nbits[field]
                v = quantize(v, lsb)
                v = saturate(v, nbits)
                v = int(v)

                this_trk[ifield] = v
        trks_to_write.append(this_trk)

    for imu, dmu in enumerate(mus_to_write):
        ostr = vals_to_ostring(data=dmu, df=muon_obj, iEv=iEv, itype=0, iobj=imu, valFormat='{:10.0f}')
        fout.write(ostr + '\n')
    for itrk, trk in enumerate(trks_to_write):
        ostr = vals_to_ostring(data=trk, df=trk_obj, iEv=iEv, itype=0, iobj=itrk, valFormat='{:10.0f}')
        fout.write(ostr + '\n')

print '... finished and saved in', ofilename

import ROOT
import root_numpy ## to dump a tree into numpy array

## format to read. If you change their position, you need to change the index where values are accessed below --> just append at the end
trk_obj  = ['L1TT_trk_pt', 'L1TT_trk_eta', 'L1TT_trk_phi', 'L1TT_trk_charge', 'L1TT_trk_chi2', 'L1TT_trk_nstubs']
muon_obj = ['EMTF_mu_pt', 'EMTF_mu_theta', 'EMTF_mu_phi', 'EMTF_mu_charge']

def to_binary(n, nbits):
    form_str = "{0:0%ib}"%(nbits)
    ret_str = form_str.format(n)
    if len(ret_str) != nbits:
        raise RuntimeError ("binary conversion of {n} onto {nbits} bits failed giving the wrong lenght of output word {ret_str}. Please check that you have enough bits".format(n=n, nbits=nbits, ret_str=ret_str)) 
    return ret_str

def saturate(n, nbits):
    max_v = 2**nbits -1
    if n > max_v:
        n = max_v
    return n

def quantize(n, scale):
    x = float(n)/float(scale)
    r = int(round(x))
    
    #### FIXME
    if r < 0 : r = r *-1

    return r

def build_obj_tuple(data, idx, fields):
    result = []
    for f in fields:
        x = data[f][idx]
        result.append(x)
    return tuple(result)

def eta_to_theta(x):
    #  give theta in rad 
    return (2. * ROOT.TMath.ATan(ROOT.TMath.Exp(-1.*x)))

def deg_to_rad(x):
    return (x * ROOT.TMath.Pi()/180.)

def track_to_binary_df(trk, return_quant_vals=False):
    """ build the track word in the necessary format and output the binary string """
    pt  = trk[trk_obj.index('L1TT_trk_pt')]
    eta = trk[trk_obj.index('L1TT_trk_eta')]
    phi = trk[trk_obj.index('L1TT_trk_phi')]
    charge  = trk[trk_obj.index('L1TT_trk_charge')]
    chisq   = trk[trk_obj.index('L1TT_trk_chi2')]
    nstubs  = trk[trk_obj.index('L1TT_trk_nstubs')]

    # print "pt : {}, eta : {}, phi : {}, charge : {}. chisq : {}, nstubs : {}".format(pt, eta, phi, charge, chisq, nstubs)

    ## make all the due conversions
    theta  = eta_to_theta(eta)
    charge = 1 if charge > 0 else 0 ## 1 : positive. 0: negative

    ## quantize everything
    q_pt     = quantize(pt,     scale=0.5)
    q_theta  = quantize(theta,  scale=0.002)
    q_phi    = quantize(phi,    scale=0.002) ## FIXME
    q_charge = charge
    q_chisq  = quantize(chisq,  scale=1)
    q_nstubs = quantize(nstubs, scale=1)

    ## protection against very large overflow
    q_chisq = saturate(q_chisq, 10)

    # for debug only
    if return_quant_vals:
        ret_dict = {
            'pt'     : q_pt,
            'theta'  : q_theta,
            'phi'    : q_phi,
            'charge' : q_charge,
            'chisq'  : q_chisq,
            'nstubs' : q_nstubs,
        }
        return ret_dict

    s_pt     = to_binary(q_pt,     15) ## FIXME : fix all values
    s_theta  = to_binary(q_theta,  15)
    s_phi    = to_binary(q_phi,    15)
    s_charge = to_binary(q_charge, 1)
    s_chisq  = to_binary(q_chisq,  10)
    s_nstubs = to_binary(q_nstubs, 10)

    ## build the variable as a binary string
    trk_word = ''.join([s_nstubs, s_chisq, s_charge, s_theta, s_phi, s_pt])

    ## pad to 100 bit length
    nbits = 100

    if len(trk_word) > nbits:
        print "*** WARNING: track is longer than", nbits, 'bits, trimming'
        trk_word = trk_word[:nbits]

    if len(trk_word) != nbits:
        ntoadd = nbits-len(trk_word)
        trk_word = '0'*ntoadd + trk_word

    if len(trk_word) != nbits:
        print "*** ERROR: track string has a lenght different than", nbits, 'bits ??'

    return trk_word

def muon_to_binary_df(mu, return_quant_vals=False):
    """ build the  muon word in the necessary format and output the binary string """
    pt      = mu[muon_obj.index('EMTF_mu_pt')]
    theta   = mu[muon_obj.index('EMTF_mu_theta')]
    phi     = mu[muon_obj.index('EMTF_mu_phi')]
    charge  = mu[muon_obj.index('EMTF_mu_charge')]

    ## convert theta and phi to radians
    theta = deg_to_rad(theta)
    phi   = deg_to_rad(phi)

    ## make all the due conversions
    charge = 1 if charge > 0 else 0 ## 1 : positive. 0: negative

    ## quantize everything
    q_pt     = quantize(pt,     scale=0.5)
    q_theta  = quantize(theta,  scale=0.002)
    q_phi    = quantize(phi,    scale=0.002) ## FIXME
    q_charge = charge

    # for debug only
    if return_quant_vals:
        ret_dict = {
            'pt'     : q_pt,
            'theta'  : q_theta,
            'phi'    : q_phi,
            'charge' : q_charge,
        }
        return ret_dict

    s_pt     = to_binary(q_pt,     15) ## FIXME : fix all values
    s_theta  = to_binary(q_theta,  11)
    s_phi    = to_binary(q_phi,    11)
    s_charge = to_binary(q_charge, 1)

    mu_word = ''.join([s_charge, s_theta, s_phi, s_pt])

    ## pad to 100 bit length
    nbits = 40

    if len(mu_word) > nbits:
        print "*** WARNING: muon is longer than", nbits, 'bits, trimming'
        mu_word = mu_word[:nbits]

    if len(mu_word) != nbits:
        ntoadd = nbits-len(mu_word)
        mu_word = '0'*ntoadd + mu_word

    if len(mu_word) != nbits:
        print "*** ERROR: muon string has a lenght different than", nbits, 'bits ??'

    return mu_word

def chunkify (in_s, chsize = 32):
    
    chunks = []
    # print in_s

    if len(in_s) % chsize != 0:
        raise RuntimeError("size of chunks does not match total")

    while len(in_s) > 0:
        this_s = in_s[:chsize]
        in_s   = in_s[chsize:]
        chunks.append(this_s)

    # print chunks

    return chunks


####################################################################################################################


print '... starting'

values = root_numpy.root2array('root://cmseos.fnal.gov//store/user/lcadamur/L1MuTrks_ntuples/SingleMu_FlatPt-2to100_L1TPU200_12Ott_DWcorr_CMSSWdefaultNoRelax/output/ntuple_0.root',
        'Ntuplizer/MuonTrackTree')

print '... input opened'

fout = open('mu_track_patterns.txt', 'w')



nEv = 2
if nEv > len(values):
    print "... you requeste", nEv, "events but input tree only has", len(values), "values"
    nEv = len(values)


NtrkToKeep = 15
NmuToKeep  = 12

NmuBits  = 40
NtrkBits = 100

n_dump_object = 1 # printout the properties of the first N objects written [ > 0 to print anything]

print '... starting event loop'

for iEv in range(nEv):
    
    print "... ... doing event", iEv

    n_trk  = values[iEv]['n_L1TT_trk']
    n_muon = values[iEv]['n_EMTF_mu']

    tracks = []
    muons = []

    for itrk in range(n_trk):
        trk = build_obj_tuple(values[iEv], itrk, trk_obj)
        tracks.append(trk)

    for imuon in range(n_muon):
        muon = build_obj_tuple(values[iEv], imuon, muon_obj)
        muons.append(muon)

    # print tracks
    # print muon

    ### filter to only keep tracks in the endcap
    tracks = filter(lambda x: abs(x[trk_obj.index('L1TT_trk_eta')]) > 1.2, tracks)
    # tracks = filter(lambda x: abs(x[1]) > 1.2, tracks)

    # print tracks
    # print muon

    ### order by pT
    tracks.sort(key=lambda tup: tup[trk_obj.index('L1TT_trk_pt')], reverse=True) ## sort by pt (first field)
    muons.sort(key=lambda tup: tup[muon_obj.index('EMTF_mu_pt')], reverse=True) ## sort by pt (first field)
    # tracks.sort(key=lambda tup: tup[0], reverse=True) ## sort by pt (first field)
    # muons.sort(key=lambda tup: tup[0], reverse=True) ## sort by pt (first field)

    # print tracks
    # print muon

    ### trim according to the number to keep -> multiplexing to be implemented here
    tracks = tracks[:NtrkToKeep]
    muons  = muons[:NmuToKeep]

    print " >> dumping as patterns", len(tracks), "tracks and", len(muons), "EMTF muons"

    # print tracks
    # print muon

    if iEv < n_dump_object:
        print "\n================ TRACKS from EVT", iEv, "================"
        print "... dataformat", trk_obj
        for idx, t in enumerate(tracks):
            trk_vals = track_to_binary_df(t, return_quant_vals=True)
            print idx, ">>", t
            print "         >>> quant: pt = {pt:<10}, theta = {theta:<10}, phi = {phi:<10}, charge = {charge:<2}, chisq = {chisq:<10}, nstubs = {nstubs:<10}".format(**trk_vals)
            print "         >>> full w = ", track_to_binary_df(t, return_quant_vals=False)

        print "\n================ MUONS from EVT", iEv, "================"
        print "... dataformat", muon_obj
        for idx, m in enumerate(muons):
            mu_vals = muon_to_binary_df(m, return_quant_vals=True)
            print idx, ">>", m
            print "         >>> quant: pt = {pt:<10}, theta = {theta:<10}, phi = {phi:<10}, charge = {charge:<2}".format(**mu_vals)
            print "         >>> full w = ", muon_to_binary_df(m, return_quant_vals=False)
        print '\n'

    ### I selected the candidates that I want -> dump them to a single bit word and then to file    
    ### DF composition : LSBs are a chain of NmuToKeep with NmuBits, HSBs are a chain of NtrkToKeep with NtrkBits

    s_mu  = ''
    s_trk = ''

    for mu in muons:
        s_mu = muon_to_binary_df(mu) + s_mu

    ## pad with zeroes in case Nmu < NmuToKeep
    if len(muons) < NmuToKeep:
        print ' >> this event only has', len(muons), 'muons, padding with zeros'
        ntopad = NmuBits * (NmuToKeep - len(muons))
        s_mu = '0' * ntopad + s_mu

    for trk in tracks:
        s_trk = track_to_binary_df(trk) + s_trk

    ## pad with zeroes in case Nmu < NmuToKeep
    if len(tracks) < NtrkToKeep:
        print ' >> this event only has', len(tracks), 'tracks, padding with zeros'
        ntopad = NtrkBits * (NtrkToKeep - len(tracks))
        s_trk = '0' * ntopad + s_trk

    s_tot = s_trk + s_mu

    ## since each input word is 2048 bits, pad with zeroes
    nbitsDF = 2048
    if len(s_tot) > nbitsDF:
        print "*** WARNING: pattern is longer than", nbitsDF, 'bits, trimming'
        s_tot = s_tot[:nbitsDF]

    if len(s_tot) != nbitsDF:
        ntoadd = nbitsDF-len(s_tot)
        s_tot = '0'*ntoadd + s_tot

    if len(s_tot) != nbitsDF:
        print "*** ERROR: pattern string has a lenght different than", nbitsDF, 'bits ??'

    ## convert into buckets of 32 bits so that it's easy to read them in the buffers
    chunks = chunkify (s_tot, chsize = 32)

    ## convert into hex numbers to ease c++ I/O
    num_chunks = [int(s, 2) for s in chunks]

    ## output to file in hex format
    for nc in num_chunks:
        fout.write('{:08x} '.format(nc))
    fout.write('\n')

    # track_to_binary_df(tracks[0])

    # fout.write(value + '\n')

# x = values['L1TT_trk_pt'][0][0]
# print x, quantize(x, 0.5), to_binary(quantize(x, 0.5), nbits=6)

# print values['L1TT_trk_pt'][0]


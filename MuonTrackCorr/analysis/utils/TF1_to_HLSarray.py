### convert the input TF1 into a c++ array by writing the initialization at command line
### since I am not sure of how to make the array initialized from a .coe in HLS

def TF1_to_arr(func, stepx, stepy):
    xmin = ROOT.Double(0.0)
    xmax = ROOT.Double(0.0)
    func.GetRange(xmin, xmax)
    print "f : ", func.GetName(), " xmin, xmax = ", xmin, xmax
    vals = []
    istep = 0
    while True:
        x = istep*stepx
        # print " .... ", x
        if x > xmax:
            break
        v = (x, int(func.Eval(x)/stepy))
        # print v
        vals.append(v)
        istep += 1
    print " >> outputting array of", len(vals), "length"
    return vals

def writeln(f, val):
    f.write(val+'\n')

# def arr_to_txt(arr, warr, fout, arrname, HLStype):
#     """ write a single 1D array """
#     writeln(fout, '%s %s [%i] = {' % (HLStype, arrname, warr))
#     # if warr > len(arr):
#     #     print "array size from TF1 and desired arr width do not match"
#     for i in range(0, (1 << warr)):
#         val = arr[i][1] if i < len(arr) else arr[-1][1] ### saturate to last value to pad array
#         writeln(fout, '   %0x,' % val)
#     writeln(fout, '}')

def arr_to_txt(arr, warr, fout):
    """ write a single 1D array """
    # writeln(fout, '      {')
    # if warr > len(arr):
    #     print "array size from TF1 and desired arr width do not match"
    for i in range(0, (1 << warr)):
        val = arr[i][1] if i < len(arr) else arr[-1][1] ### saturate to last value to pad array
        writeln(fout, '         0x%0x,' % val)
    # writeln(fout, '      }')


def arr2D_to_txt(arr, nbitrow, nbitcol, fout, arrname, HLStype):
    """ write 2D array """
    writeln(fout, 'const static %s %s [%i][%i] = {' % (HLStype, arrname, (1 << nbitrow), (1 << nbitcol) ))
    # if warr > len(arr):
    #     print "array size from TF1 and desired arr width do not match"
    for ir in range(0, (1 << nbitrow)):
        if ir < len(arr): ## since I have nbins_theta < 26nbitsrow
            writeln(fout, '   {')
            arr_to_txt(arr[ir], nbitcol, fout)
            writeln(fout, '   },')
    writeln(fout, '};')

import ROOT
import argparse

parser = argparse.ArgumentParser(description='Command line parser')

# parser.add_argument('--file', dest='file', help='input file name', default='../correlator_data/quantized/matching_windows_theta_q99_wrlx_x2to6_y0to0p5__x0.5_y0.001.root')
# args = parser.parse_args()

file_proto = '../correlator_data/quantized/matching_windows_{}_q99_wrlx_x2to6_y0to0p5__x0.5_y0.001.root'

fout = open('matching_LUTs.h', 'w')
writeln(fout, '#ifndef MATCHING_LUTS_H')
writeln(fout, '#define MATCHING_LUTS_H')
writeln(fout, '#include "ap_int.h"')

for angle in ["phi", "theta"]:
    file = file_proto.format(angle)
    print "... opening file ", file
    fIn = ROOT.TFile(file)
    for bound in ("low", "high"):
        this_arr_coll = [] ### the total of the arrays for these 10 bins
        for ifit in range(1, 11): ## there are 10 eta bins
            fname = 'fit_%s_%i' % (bound, ifit)
            print fname
            func = fIn.Get(fname)
            farr = TF1_to_arr(func, 0.5, 0.001)
            this_arr_coll.append(farr)
            # if ifit == 1 and bound == 'low': 
            #     arr_to_txt(arr=farr, warr=9, fout=fout, arrname=fname, HLStype="ap_uint<10>") ### fix: array name and  hlstype
        ### now dump to file
        arr2D_to_txt(this_arr_coll, nbitrow=4, nbitcol=9, fout=fout, arrname = "%s_%s_bounds" % (angle, bound), HLStype="ap_uint<10>")
writeln(fout, '#endif')

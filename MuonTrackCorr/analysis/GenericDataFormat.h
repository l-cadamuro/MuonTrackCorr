#ifndef GENERICDATAFORMAT_H
#define GENERICDATAFORMAT_H

/*
** class  : GenericDataFormat
** author : L.Cadamuro (UF)
** date   : 4/11/2019
** brief  : very generic structs to be used as inputs to the correlator
**        : to make sure that Mantra can handle muons and tracks from all the detectors
*/

struct track_df {
    double pt;     // GeV
    double eta;    // rad, -inf / +inf
    double theta;  // rad, 0 -> +90-90
    double phi;    // rad, -pi / + pi
    int    nstubs; // 
    double chi2;   // 
    int    charge; // -1. +1 
};

struct muon_df {
    double pt;     // GeV
    double eta;    // rad, -inf / +inf
    double theta;  // rad, 0 -> +90-90
    double phi;    // rad, -pi / + pi
    int    charge; // -1. +1 
};

#endif //GENERICDATAFORMAT_H
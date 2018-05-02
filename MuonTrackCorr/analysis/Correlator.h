#ifndef CORRELATOR_H
#define CORRELATOR_H

#include <iostream>
#include <array>
#include <vector>
#include <tuple>
#include <string>
#include <utility>
#include <stdlib.h>
#include "MatchWindow.h"
#include "TFile.h"
#include "MuTkTree.h" // my interface to the ntuples

class Correlator{
    
    public:
        Correlator(std::vector<double>& bounds, TFile* fIn_theta, TFile* fIn_phi);
        ~Correlator(){};
        void test(double eta, double pt);
        std::vector<int> find_match(MuTkTree& mtkt); // gives a vector with the idxs of muons for each L1TTT

    private:
        int getBin(double val);

        // converters
        double deg_to_rad(double x) {
            return (x * TMath::Pi()/180.) ;
        }

        double eta_to_theta(double x){
            //  give theta in rad 
            return (2. * TMath::ATan(TMath::Exp(-1.*x)));
        }

        double to_mpio2_pio2(double x){
            //  put the angle in radians between -pi/2 and pi/2
            while (x >= 0.5*TMath::Pi())
                x -= TMath::Pi();
            while (x < -0.5*TMath::Pi())
                x += TMath::Pi();
            return x;
        }


        int nbins_; // counts the number of MatchWindow = bounds_.size() - 1
        std::vector<double> bounds_; // counts the boundaries of the MatchWindow (in eta/theta)
        std::vector<MatchWindow> wdws_theta_;
        std::vector<MatchWindow> wdws_phi_;
};

Correlator::Correlator(std::vector<double>& bounds, TFile* fIn_theta, TFile* fIn_phi) :
    wdws_theta_(bounds.size()-1, MatchWindow()),
    wdws_phi_(bounds.size()-1, MatchWindow())
{
    nbins_ = bounds.size()-1;
    for (double b : bounds)
        bounds_.push_back(b);

    // now load in memory the TF1 fits

    for (uint ib = 0; ib < nbins_; ++ib)
    {
        std::string wdn;
        std::string nml;
        std::string nmh;
        TF1* fl;
        TF1* fh;

        wdn = std::string("wdw_theta_") + std::to_string(ib+1);
        nml = std::string("fit_low_")   + std::to_string(ib+1);
        nmh = std::string("fit_high_")  + std::to_string(ib+1);
        fl = (TF1*) fIn_theta->Get(nml.c_str());
        fh = (TF1*) fIn_theta->Get(nmh.c_str());
        if (fl == nullptr || fh == nullptr)
            throw std::runtime_error("Could not init theta");        
        wdws_theta_.at(ib).SetName(wdn);
        wdws_theta_.at(ib).SetLower(fl);
        wdws_theta_.at(ib).SetUpper(fh);


        wdn = std::string("wdw_phi_") + std::to_string(ib+1);
        nml = std::string("fit_low_")   + std::to_string(ib+1);
        nmh = std::string("fit_high_")  + std::to_string(ib+1);
        fl = (TF1*) fIn_phi->Get(nml.c_str());
        fh = (TF1*) fIn_phi->Get(nmh.c_str());
        if (fl == nullptr || fh == nullptr)
            throw std::runtime_error("Could not init phi");        
        wdws_phi_.at(ib).SetName(wdn);
        wdws_phi_.at(ib).SetLower(fl);
        wdws_phi_.at(ib).SetUpper(fh);
    }
}


int Correlator::getBin(double val)
{
    // FIXME: not the most efficient, nor the most elegant implementation for now
    if (val < bounds_.at(0))
        return 0;
    if (val >= bounds_.back())
        return (nbins_-1); // i.e. bounds_size() -2

    for (uint ib = 0; ib < bounds_.size()-1; ++ib)
    {
        if (val >= bounds_.at(ib) && val < bounds_.at(ib+1))
            return ib;
    }

    std::cout << "Something strange happened at val " << val << std::endl;
    return 0;
}

void Correlator::test(double eta, double pt)
{
    int ibin = getBin(eta);
    std::cout << "- eta : " << eta << " pt: " << pt << std::endl; 
    std::cout << ">>> bin " << ibin << std::endl;
    std::cout << ">>> low_phi : "   << wdws_phi_.at(ibin).bound_low(pt)   << " , high_phi : " << wdws_phi_.at(ibin).bound_high(pt) << std::endl;
    std::cout << ">>> low_theta : " << wdws_theta_.at(ibin).bound_low(pt) << " , high_theta : " << wdws_theta_.at(ibin).bound_high(pt) << std::endl;
    return;
}

std::vector<int> Correlator::find_match(MuTkTree& mtkt)
{
    std::vector<int> out (*(mtkt.n_L1TT_trk));
    for (uint it = 0; it < *(mtkt.n_L1TT_trk); ++it)
    {
        float trk_pt      = mtkt.L1TT_trk_pt.At(it);
        float trk_aeta    = std::abs(mtkt.L1TT_trk_eta.At(it));
        float trk_theta   = to_mpio2_pio2(eta_to_theta(mtkt.L1TT_trk_eta.At(it)));
        float trk_phi     = mtkt.L1TT_trk_phi.At(it);

        int ibin = getBin(trk_aeta);

        std::vector<std::tuple<float, float, int>> matched; // dtheta, dphi, idx
        // loop on muons to see which match
        for (uint im = 0; im < *(mtkt.n_EMTF_mu); ++im)
        {

            // putting everything in rad as in the matchTree
            float emtf_theta  = to_mpio2_pio2(eta_to_theta(mtkt.EMTF_mu_eta.At(im))) ;
            float emtf_phi    = deg_to_rad(mtkt.EMTF_mu_phi.At(im)) ;

            float dtheta = std::abs(std::abs(emtf_theta) - std::abs(trk_theta));
            float dphi   = std::abs(std::abs(emtf_phi) - std::abs(trk_phi));

            // FIXME: introduce the sign in the comparison in phi!

            // float rndm = 1.*rand()/RAND_MAX;
            float safety_factor_l = 0.5; // make the matching windows larger by this safety factor
            float safety_factor_h = 0.5; // make the matching windows larger by this safety factor

            if (
                // emtf_theta * trk_theta > 0 &&
                dtheta >  (1 - safety_factor_l) * wdws_theta_.at(ibin).bound_low(trk_pt)  &&
                dtheta <= (1 + safety_factor_h) * wdws_theta_.at(ibin).bound_high(trk_pt) &&
                dphi   >  (1 - safety_factor_l) * wdws_phi_.at(ibin).bound_low(trk_pt)    &&
                dphi   <= (1 + safety_factor_h) * wdws_phi_.at(ibin).bound_high(trk_pt)   &&
                // rndm > 0.5
                true
            )
                matched.push_back(std::make_tuple(dtheta, dphi, im));
            // else if (emtf_theta * trk_theta > 0)
            // {
            //     std::cout << "=== DEBUG ===" << std::endl;
            //     if (! (dtheta >  (1 - safety_factor_l) * wdws_theta_.at(ibin).bound_low(trk_pt)  )) std::cout << "FAIL dtheta low -- " << dtheta << " " << wdws_theta_.at(ibin).bound_low(trk_pt) << std::endl;
            //     if (! (dtheta <= (1 + safety_factor_h) * wdws_theta_.at(ibin).bound_high(trk_pt) )) std::cout << "FAIL dtheta high -- " << dtheta << " " << wdws_theta_.at(ibin).bound_high(trk_pt) << std::endl;
            //     if (! (dphi   >  (1 - safety_factor_l) * wdws_phi_.at(ibin).bound_low(trk_pt)    )) std::cout << "FAIL dphi low -- " << dphi << " " << wdws_phi_.at(ibin).bound_low(trk_pt) << std::endl;
            //     if (! (dphi   <= (1 + safety_factor_h) * wdws_phi_.at(ibin).bound_high(trk_pt)   )) std::cout << "FAIL dphi high -- " << dphi << " " << wdws_phi_.at(ibin).bound_high(trk_pt) << std::endl;
            // }
        }

        if (matched.size() == 0)
            out.at(it) = -1;
        else
        {
            std::sort(matched.begin(), matched.end()); // closest in theta, then in phi
            out.at(it) = std::get<2>(matched.at(0));
        }
    }
    return out;
}

#endif
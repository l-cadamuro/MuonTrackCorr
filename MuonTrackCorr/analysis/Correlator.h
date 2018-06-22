#ifndef CORRELATOR_H
#define CORRELATOR_H

#include <iostream>
#include <functional>
#include <array>
#include <vector>
#include <tuple>
#include <string>
#include <utility>
#include <stdlib.h>
#include "MatchWindow.h"
#include "TFile.h"
#include "MuTkTree.h" // my interface to the ntuples
#include "TMath.h"

class Correlator{
    
    public:
        Correlator(std::vector<double>& bounds, TFile* fIn_theta, TFile* fIn_phi);
        ~Correlator(){};
        void test(double eta, double pt);
        std::vector<int> find_match(MuTkTree& mtkt, std::vector<int>* narbitrated = nullptr); // gives a vector with the idxs of muons for each L1TTT
        void set_safety_factor (float sf_l, float sf_h) {
            safety_factor_l_ = sf_l;
            safety_factor_h_ = sf_h;
            std::cout << "Correlator : safety factor LOW is " << safety_factor_l_ << std::endl;
            std::cout << "Correlator : safety factor HIGH is " << safety_factor_h_ << std::endl;
        }
        void set_sf_initialrelax (float sf_l, float sf_h) {
            initial_sf_l_ = sf_l;
            initial_sf_h_ = sf_h;
            std::cout << "Correlator : initial relax safety factor LOW is " << initial_sf_l_ << std::endl;
            std::cout << "Correlator : initial relax safety factor HIGH is " << initial_sf_h_ << std::endl;
        }
        void set_relaxation_pattern(float pt_start, float pt_end) {
            pt_start_ = pt_start;
            pt_end_   = pt_end;
            std::cout << "Correlator : set relaxing from " << pt_start_ << " to " << pt_end_ << std::endl;
        }
        void set_safety_factor (float sf) {set_safety_factor(sf,sf);}
        void set_sf_initialrelax (float sf) {set_sf_initialrelax(sf,sf);}
        void set_do_relax_factor (bool val) {
            do_relax_factor_ = val;
            std::cout << "Correlator : set do_relax to " << std::boolalpha << do_relax_factor_ << std::noboolalpha << std::endl;
        }
    
        bool track_qual_presel_ = true;

    private:
        int getBin(double val);

        // resolves ambiguities to give max 1 tkmu per EMTF
        // if a pointer to narbitrated is passed, this vector is filled with the number of tracks arbitrated that were matched to the same EMTF
        std::vector<int> make_unique_coll(MuTkTree& mtkt, std::vector<int> matches, std::vector<int>* narbitrated = nullptr);

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

        double to_mpi_pi (double x){
            while (x >= TMath::Pi())
                x -= 2.*TMath::Pi();
            while (x < -TMath::Pi())
                x += 2.*TMath::Pi();
            return x;
        }

        double sf_progressive (double x, double xstart, double xstop, double ystart, double ystop)
        {
            if (x < xstart)
                return ystart;
            if (x >= xstart && x < xstop)
                return ystart + (x-xstart)*(ystop-ystart)/(xstop-xstart);
            return ystop;
        }

        int nbins_; // counts the number of MatchWindow = bounds_.size() - 1
        std::vector<double> bounds_; // counts the boundaries of the MatchWindow (in eta/theta)
        std::vector<MatchWindow> wdws_theta_;
        std::vector<MatchWindow> wdws_phi_;
        float safety_factor_l_; // increase the lower theta/phi threshold by this fractions
        float safety_factor_h_; // increase the upper theta/phi threshold by this fractions
        float initial_sf_l_; // the start of the relaxation
        float initial_sf_h_; // the start of the relaxation
        float pt_start_; // the relaxation of the threshold
        float pt_end_; // the relaxation of the threshold
        bool  do_relax_factor_; // true if applying the linear relaxation
};

Correlator::Correlator(std::vector<double>& bounds, TFile* fIn_theta, TFile* fIn_phi) :
    wdws_theta_(bounds.size()-1, MatchWindow()),
    wdws_phi_(bounds.size()-1, MatchWindow())
{
    set_safety_factor(0.5);
    set_sf_initialrelax(0.0);
    set_relaxation_pattern(2.0, 6.0);
    set_do_relax_factor(true);

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

std::vector<int> Correlator::find_match(MuTkTree& mtkt, std::vector<int>* narbitrated)
{
    std::vector<int> out (*(mtkt.n_L1TT_trk));
    for (uint it = 0; it < *(mtkt.n_L1TT_trk); ++it)
    {
        float trk_pt      = mtkt.L1TT_trk_pt.At(it);
        float trk_p       = mtkt.L1TT_trk_p.At(it);
        float trk_aeta    = std::abs(mtkt.L1TT_trk_eta.At(it));
        float trk_theta   = to_mpio2_pio2(eta_to_theta(mtkt.L1TT_trk_eta.At(it)));
        float trk_phi     = mtkt.L1TT_trk_phi.At(it);
        int   trk_charge  = mtkt.L1TT_trk_charge.At(it);

        // porting some selections from the MuonTrackCorr finder
        // https://github.com/cms-l1t-offline/cmssw/blob/l1t-phase2-932-v1.6/L1Trigger/L1TTrackMatch/plugins/L1TkMuonProducer.cc#L264
        bool reject_trk = false;
        if (trk_p  < 3.5 )  reject_trk = true;
        if (trk_aeta > 2.5) reject_trk = true;
        if (track_qual_presel_)
        {
            float l1tk_chi2 = mtkt.L1TT_trk_chi2.At(it);
            int l1tk_nstubs = mtkt.L1TT_trk_nstubs.At(it);
            if (l1tk_chi2 >= 100) reject_trk = true;
            if (l1tk_nstubs < 4) reject_trk = true;
        }

        int ibin = getBin(trk_aeta);

        std::vector<std::tuple<float, float, int>> matched; // dtheta, dphi, idx
        // loop on muons to see which match
        for (uint im = 0; im < *(mtkt.n_EMTF_mu); ++im)
        {

            // putting everything in rad as in the matchTree
            float emtf_theta  = to_mpio2_pio2(eta_to_theta(mtkt.EMTF_mu_eta.At(im))) ;
            float emtf_phi    = deg_to_rad(mtkt.EMTF_mu_phi.At(im)) ;

            // float dtheta = std::abs(std::abs(emtf_theta) - std::abs(trk_theta));
            // float dphi   = std::abs(std::abs(emtf_phi) - std::abs(trk_phi));

            float dtheta = std::abs(emtf_theta - trk_theta);
            float dphi   = to_mpi_pi(emtf_phi - trk_phi);
            float adphi  = std::abs(dphi);

            // float rndm = 1.*rand()/RAND_MAX;
            // 50% --> approx same windows as TkMu corr
            // float safety_factor_l = 0.5; // make the matching windows larger by this safety factor
            // float safety_factor_h = 0.5; // make the matching windows larger by this safety factor

            // float safety_factor_l = 0.0; // make the matching windows larger by this safety factor
            // float safety_factor_h = 0.0; // make the matching windows larger by this safety factor

            // applying a ''flat'' safety factors gives too large cones at low pT where the occupancy is higher
            // instead, the factor can be increased vs pt to retrieve high pT efficiency and keep low occupancy at low pt

            // float pt_start = 2.0;
            // float pt_end   = 2.0;

            double sf_l;
            double sf_h;
            if (do_relax_factor_)
            {
                sf_l = sf_progressive(trk_pt, pt_start_, pt_end_, initial_sf_l_, safety_factor_l_);
                sf_h = sf_progressive(trk_pt, pt_start_, pt_end_, initial_sf_h_, safety_factor_h_);
            }
            else
            {
                sf_l = safety_factor_l_;
                sf_h = safety_factor_h_;
            }

            // double sf_l = sf_progressive(trk_pt, pt_start_, pt_end_, 0.0, safety_factor_l_);
            // double sf_h = sf_progressive(trk_pt, pt_start_, pt_end_, 0.0, safety_factor_h_);


            if (
                // emtf_theta * trk_theta > 0 &&
                dtheta >  (1 - sf_l) * wdws_theta_.at(ibin).bound_low(trk_pt)  &&
                dtheta <= (1 + sf_h) * wdws_theta_.at(ibin).bound_high(trk_pt) &&
                adphi  >  (1 - sf_l) * wdws_phi_.at(ibin).bound_low(trk_pt)    &&
                adphi  <= (1 + sf_h) * wdws_phi_.at(ibin).bound_high(trk_pt)   &&
                dphi*trk_charge < 0                                            && // sign requirement
                // rndm > 0.5
                true
            )
                matched.push_back(std::make_tuple(dtheta, adphi, im));
            // else if (emtf_theta * trk_theta > 0)
            // {
            //     std::cout << "=== DEBUG ===" << std::endl;
            //     if (! (dtheta >  (1 - safety_factor_l) * wdws_theta_.at(ibin).bound_low(trk_pt)  )) std::cout << "FAIL dtheta low -- " << dtheta << " " << wdws_theta_.at(ibin).bound_low(trk_pt) << std::endl;
            //     if (! (dtheta <= (1 + safety_factor_h) * wdws_theta_.at(ibin).bound_high(trk_pt) )) std::cout << "FAIL dtheta high -- " << dtheta << " " << wdws_theta_.at(ibin).bound_high(trk_pt) << std::endl;
            //     if (! (dphi   >  (1 - safety_factor_l) * wdws_phi_.at(ibin).bound_low(trk_pt)    )) std::cout << "FAIL dphi low -- " << dphi << " " << wdws_phi_.at(ibin).bound_low(trk_pt) << std::endl;
            //     if (! (dphi   <= (1 + safety_factor_h) * wdws_phi_.at(ibin).bound_high(trk_pt)   )) std::cout << "FAIL dphi high -- " << dphi << " " << wdws_phi_.at(ibin).bound_high(trk_pt) << std::endl;
            // }
        }

        if (reject_trk)
            matched.clear(); // quick fix - to be optimised to avoid the operations above

        if (matched.size() == 0)
            out.at(it) = -1;
        else
        {
            std::sort(matched.begin(), matched.end()); // closest in theta, then in phi
            out.at(it) = std::get<2>(matched.at(0));
        }
    }

    // return out;

    // now convert out to a unique set
    auto unique_out = make_unique_coll(mtkt, out, narbitrated);

    // auto unique_out = out;
    // if (narbitrated) narbitrated->resize(unique_out.size(), 99);
    
    return unique_out;
}

std::vector<int> Correlator::make_unique_coll(MuTkTree& mtkt, std::vector<int> matches, std::vector<int>* narbitrated)
{
    std::vector<int> out (matches.size(), -1);

    if (narbitrated)
        narbitrated->resize(matches.size(), 0);

    std::vector<std::vector<int>> macthed_to_emtf(*(mtkt.n_EMTF_mu), std::vector<int>(0)); // one vector of matched trk idx per EMTF

    for (int itrack = 0; itrack < matches.size(); ++itrack)
    {
        int iemtf = matches.at(itrack);
        if (iemtf < 0) continue;
        macthed_to_emtf.at(iemtf).push_back(itrack);
    }

    // this sorts by by the trk (a < b if pta < ptb)
    std::function<bool(int, int, MuTkTree&)> track_less_than_proto = [](int idx1, int idx2, MuTkTree& mtrktr)
    {
        float pt1 = mtrktr.L1TT_trk_pt.At(idx1);
        float pt2 = mtrktr.L1TT_trk_pt.At(idx2);
        return (pt1 < pt2);
    };
    // // and binds to accept only 2 params
    std::function<bool(int,int)> track_less_than = std::bind(track_less_than_proto, std::placeholders::_1, std::placeholders::_2, std::ref(mtkt));


    for (int iemtf = 0; iemtf < macthed_to_emtf.size(); ++iemtf)
    {
        std::vector<int>& thisv = macthed_to_emtf.at(iemtf);
        if (thisv.size() == 0) continue;
        
        // std::cout << " === BEFORE === " << std::endl;
        // for (int idx : macthed_to_emtf.at(iemtf))
        //     std::cout << mtkt.L1TT_trk_pt.At(idx) << std::endl;

        std::sort(thisv.begin(), thisv.end(), track_less_than);

        // std::cout << " === AFTER === " << std::endl;
        // for (int idx : macthed_to_emtf.at(iemtf))
        //     std::cout << mtkt.L1TT_trk_pt.At(idx) << std::endl;

        // copy to the output
        int best_trk = thisv.back();
        out.at(best_trk) = iemtf;

        if (narbitrated)
            narbitrated->at(best_trk) = thisv.size();
    }

    return out;
}

#endif

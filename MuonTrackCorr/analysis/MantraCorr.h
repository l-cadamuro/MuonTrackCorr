#ifndef MANTRACORR_H
#define MANTRACORR_H

/*
** class  : MantraCorr
** author : L.Cadamuro (UF)
** date   : 4/11/2019
** brief  : correlates muons and tracks using pre-encoded windows
*/

#include <iostream>
#include <vector>
#include <string>
#include <utility>
#include "MatchWindow.h"
#include "GenericDataFormat.h"
#include "TFile.h"


class MantraCorr
{
    public:
        MantraCorr(std::vector<double>& bounds, TFile* fIn_theta, TFile* fIn_phi, std::string name);
        ~MantraCorr(){};

        // returns a vector with the same size of muons, each with an index to the matched L1 track, or -1 if no match is found
        std::vector<int> find_match(std::vector<track_df>& tracks, std::vector<muon_df>& muons);

        void test(double eta, double pt);

        void relax_windows   (double& low, double cent, double& high); // will modify low and high

        void set_safety_factor (float sf_l, float sf_h) {
            safety_factor_l_ = sf_l;
            safety_factor_h_ = sf_h;
            std::cout << "MantraCorr : " << name_ << " safety factor LOW is "  << safety_factor_l_ << std::endl;
            std::cout << "MantraCorr : " << name_ << " safety factor HIGH is " << safety_factor_h_ << std::endl;
        }

        int sign(double x){
            if (x == 0)
                return 1;
            return int (x/std::abs(x));
        }

        void setArbitrationType (std::string type); // MaxPt, MinDeltaPt

    private:

        int getBin(double val);

        std::string name_;

        int nbins_; // counts the number of MatchWindow = bounds_.size() - 1
        std::vector<double> bounds_; // counts the boundaries of the MatchWindow (in eta/theta)
        std::vector<MatchWindow> wdws_theta_;
        std::vector<MatchWindow> wdws_phi_;

        int    min_nstubs = 4;   // >= min_nstubs
        double max_chi2   = 100; // < max_chi2

        float safety_factor_l_; // increase the lower theta/phi threshold by this fractions w.r.t. the center
        float safety_factor_h_; // increase the upper theta/phi threshold by this fractions w.r.t. the center


        // float initial_sf_l_; // the start of the relaxation
        // float initial_sf_h_; // the start of the relaxation
        // float pt_start_; // the relaxation of the threshold
        // float pt_end_; // the relaxation of the threshold
        // bool  do_relax_factor_; // true if applying the linear relaxation

        double to_mpi_pi (double x){
            while (x >= TMath::Pi())
                x -= 2.*TMath::Pi();
            while (x < -TMath::Pi())
                x += 2.*TMath::Pi();
            return x;
        }

        enum sortParType {
            kMaxPt,     // pick the highest pt track matched 
            kMinDeltaPt // pick the track with the smallest pt difference w.r.t the muon
        };

        sortParType sort_type_;
};

MantraCorr::MantraCorr(std::vector<double>& bounds, TFile* fIn_theta, TFile* fIn_phi, std::string name = "mantra") :
    wdws_theta_ (bounds.size()-1, MatchWindow()),
    wdws_phi_   (bounds.size()-1, MatchWindow())
{

    name_ = name;

    safety_factor_l_ = 0.0;
    safety_factor_h_ = 0.0;

    sort_type_ = kMaxPt;

    // copy boundaries
    nbins_ = bounds.size()-1;
    for (double b : bounds)
        bounds_.push_back(b);

    // now load in memory the TF1 fits

    for (uint ib = 0; ib < nbins_; ++ib)
    {
        std::string wdn;
        std::string nml;
        std::string nmc;
        std::string nmh;
        TF1* fl;
        TF1* fc;
        TF1* fh;

        wdn = name_ + std::string("_wdw_theta_") + std::to_string(ib+1);
        nml = std::string("fit_low_")   + std::to_string(ib+1);
        nmc = std::string("fit_cent_")  + std::to_string(ib+1);
        nmh = std::string("fit_high_")  + std::to_string(ib+1);
        
        fl = (TF1*) fIn_theta->Get(nml.c_str());
        fc = (TF1*) fIn_theta->Get(nmc.c_str());
        fh = (TF1*) fIn_theta->Get(nmh.c_str());
        if (fl == nullptr || fc == nullptr || fh == nullptr){
            std::cout << "... fit theta low  : " << fl << std::endl;
            std::cout << "... fit theta cent : " << fc << std::endl;
            std::cout << "... fit theta high : " << fh << std::endl;
            throw std::runtime_error("MantraCorr : Could not init theta");        
        }
        wdws_theta_.at(ib).SetName(wdn);
        wdws_theta_.at(ib).SetLower(fl);
        wdws_theta_.at(ib).SetCentral(fc);
        wdws_theta_.at(ib).SetUpper(fh);

        wdn = name_ + std::string("_wdw_phi_") + std::to_string(ib+1);
        nml = std::string("fit_low_")   + std::to_string(ib+1);
        nmc = std::string("fit_cent_")  + std::to_string(ib+1);
        nmh = std::string("fit_high_")  + std::to_string(ib+1);
        fl = (TF1*) fIn_phi->Get(nml.c_str());
        fc = (TF1*) fIn_phi->Get(nmc.c_str());
        fh = (TF1*) fIn_phi->Get(nmh.c_str());
        if (fl == nullptr || fc == nullptr || fh == nullptr){
            std::cout << "... fit phi low  : " << fl << std::endl;
            std::cout << "... fit phi cent : " << fc << std::endl;
            std::cout << "... fit phi high : " << fh << std::endl;
            throw std::runtime_error("MantraCorr : Could not init phi");        
        }
        wdws_phi_.at(ib).SetName(wdn);
        wdws_phi_.at(ib).SetLower(fl);
        wdws_phi_.at(ib).SetCentral(fc);
        wdws_phi_.at(ib).SetUpper(fh);
    }    
}

int MantraCorr::getBin(double val)
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

void MantraCorr::test(double eta, double pt)
{
    int ibin = getBin(eta);
   
    std::cout << " ---- eta : " << eta << " pt: " << pt << std::endl; 
    std::cout << " ---- bin " << ibin << std::endl;
    std::cout << " ---- "
        << "- low_phi  : "   << wdws_phi_.at(ibin).bound_low(pt)
        << "- cent_phi : "   << wdws_phi_.at(ibin).bound_cent(pt)
        << "- high_phi : "   << wdws_phi_.at(ibin).bound_high(pt)
        << std::endl;

    std::cout << " ---- "
        << "- low_theta  : "   << wdws_theta_.at(ibin).bound_low(pt)
        << "- cent_theta : "   << wdws_theta_.at(ibin).bound_cent(pt)
        << "- high_theta : "   << wdws_theta_.at(ibin).bound_high(pt)
        << std::endl;

    return;
}

std::vector<int> MantraCorr::find_match(std::vector<track_df>& tracks, std::vector<muon_df>& muons)
{
    std::vector<int> result (muons.size(), -1); // init all TkMu to index -1
    for (uint imu = 0; imu < muons.size(); ++imu)
    {
        muon_df mu = muons.at(imu);
        std::vector<std::pair<double, int>> matched_trks; // sort_par, idx
        for (uint itrk = 0; itrk < tracks.size(); ++itrk)
        {
            // preselection of tracks
            track_df trk = tracks.at(itrk);
            if (trk.chi2   >= max_chi2)   continue; // require trk.chi2 < max_chi2
            if (trk.nstubs < min_nstubs) continue; // require trk.nstubs >= min_nstubs

            // compute delta
            // col_dphicharge = dataframe.loc[ : , 'trk_phi'].subtract(dataframe.loc[ : , phi_name]).multiply(dataframe.loc[ : , 'trk_charge']).apply(to_mpi_pi)
            // col_dthetaendc = dataframe.loc[ : , theta_name].subtract(dataframe.loc[ : , 'trk_theta']).multiply(dataframe.loc[ : , etasign_name])
            
            double dphi_charge = to_mpi_pi((trk.phi - mu.phi) * trk.charge);
            double dtheta_endc = (mu.theta - trk.theta) * (std::abs(mu.theta)/mu.theta); // sign from theta, to avoid division by 0
            if (sign(mu.theta) != sign(trk.theta)){ // crossing the barrel -> remove 180 deg to the theta of the neg candidate to avoid jumps at eta = 0
                dtheta_endc -= TMath::Pi();
            }

            // lookup the values
            int ibin = getBin(std::abs(trk.eta));

            double phi_low   = wdws_phi_.at(ibin).bound_low(trk.pt);
            double phi_cent  = wdws_phi_.at(ibin).bound_cent(trk.pt);
            double phi_high  = wdws_phi_.at(ibin).bound_high(trk.pt);
            relax_windows (phi_low, phi_cent, phi_high); // apply the safety factor
            bool   in_phi = (dphi_charge > phi_low && dphi_charge < phi_high);

            double theta_low   = wdws_theta_.at(ibin).bound_low(trk.pt);
            double theta_cent  = wdws_theta_.at(ibin).bound_cent(trk.pt);
            double theta_high  = wdws_theta_.at(ibin).bound_high(trk.pt);
            relax_windows (theta_low, theta_cent, theta_high);  // apply the safety factor
            bool   in_theta = (dtheta_endc > theta_low && dtheta_endc < theta_high);

            // if (!in_theta && in_phi)
            //     std::cout << "DID NOT MATCH : " << std::endl
            //               << trk.pt << " " << trk.eta << " " << trk.theta << " " << trk.phi << std::endl
            //               << mu.pt << " " << mu.eta << " " << mu.theta << " " << mu.phi << std::endl
            //               << dtheta_endc << std::endl;

            if (in_phi && in_theta){
                double sort_par = 99999;
                if (sort_type_ == kMaxPt)
                    sort_par = trk.pt;
                else if (sort_type_ == kMinDeltaPt){
                    sort_par = (trk.pt > 0 ? std::abs(1. - (mu.pt / trk.pt)) : 0); // trk.pt should always be > 0, but put this protection just in case
                }
                matched_trks.push_back(std::make_pair(sort_par, itrk));
            }
        }

        // choose out of the matched tracks the best one
        if (matched_trks.size() > 0)
        {
            sort (matched_trks.begin(), matched_trks.end());
            int ibest = 99999;
            if (sort_type_ == kMaxPt)
                ibest = matched_trks.rbegin() -> second; // sorted low to high -> take last for highest pT (rbegin)
            else if (sort_type_ == kMinDeltaPt)
                ibest = matched_trks.begin() -> second; // sorted low to high -> take first for min pT distance (begin)
            result.at(imu) = ibest;
        }
    }

    return result;
}

void MantraCorr::relax_windows  (double& low, double cent, double& high)
{
    double delta_high = high - cent;
    double delta_low  = cent - low;

    high = high + safety_factor_h_*delta_high;
    low  = low  - safety_factor_l_*delta_low;

    return;
}

void MantraCorr::setArbitrationType (std::string type)
{
    std::cout << "MantraCorr : setting arbitration type to " << type << std::endl;
    if (type == "MaxPt")
        sort_type_ = kMaxPt;
    else if (type == "MinDeltaPt")
        sort_type_ = kMinDeltaPt;
    else
        throw std::runtime_error("MantraCorr : setArbitrationType : cannot understand the arbitration type passed");
}


#endif // MANTRACORR_H
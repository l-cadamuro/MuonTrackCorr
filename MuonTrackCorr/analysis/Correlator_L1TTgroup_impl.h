#ifndef CORRELATOR_L1TTGROUP_IMPL_H
#define CORRELATOR_L1TTGROUP_IMPL_H

#include <iostream>
#include <array>
#include <vector>
#include <cmath>
#include <tuple>
#include <string>
#include <utility>
#include <stdlib.h>
#include "MatchWindow.h"
#include "TFile.h"
#include "TVector2.h"
#include "MuTkTree.h" // my interface to the ntuples

/* class: Correlator_L1TTgroup_impl
** brief: class that implements on my private ntuples the CMSSW implementation of the correlator
** https://github.com/cms-l1t-offline/cmssw/blob/l1t-phase2-v2.13/L1Trigger/L1TTrackMatch/plugins/L1TkMuonProducer.cc
** I use the same interface as Correlator.h to be able to switch between them
*/

class  Correlator_L1TTgroup_impl
{
    public:
        Correlator_L1TTgroup_impl(){};
        ~Correlator_L1TTgroup_impl(){};
        // gives a vector with the idxs of muons for each L1TTT
        // if a pointer to narbitrated is passed, this vector is filled with the number of tracks arbitrated that were matched to the same EMTF
        std::vector<int> find_match(MuTkTree& mtkt, std::vector<int>* narbitrated = nullptr);

    private:
        struct PropState { //something simple, imagine it's hardware emulation
           PropState() :
              pt(-99),  eta(-99), phi(-99),
              sigmaPt(-99),  sigmaEta(-99), sigmaPhi(-99),
              valid(false) {}
            float pt;
            float eta;
            float phi;
            float sigmaPt;
            float sigmaEta;
            float sigmaPhi;
            bool valid;
        };

        double deg_to_rad(double x) {
            return (x * TMath::Pi()/180.) ;
        }

        double eta_to_theta(double x){
            //  give theta in rad 
            return (2. * TMath::ATan(TMath::Exp(-1.*x)));
        }

        float deltaR2(float eta1, float phi1, float eta2, float phi2) const {
            double deta = eta2-eta1;
            double dphi = TVector2::Phi_mpi_pi(phi2-phi1);
            return ( deta*deta+dphi*dphi );
        }


        // bool filter_track   (MuTkTree& mtkt, int itrk);
        // bool filter_emtf    (MuTkTree& mtkt, int iemtf);
        PropState propagateToGMT (MuTkTree& mtkt, int itrk);
        // return vector of tkmus, as <itrk, iemtf>
        std::vector<std::pair<int,int>> make_tkmu(MuTkTree& mtkt, std::vector<int>* narbitrated = nullptr); // implements the cmssw mutk producer

        float ETAMIN_               = 0.;
        float ETAMAX_               = 5.;
        float ZMAX_                 = 25.;   // |z_track| < ZMAX in cm
        float CHI2MAX_              = 100.;
        float PTMINTRA_             = 2.;
        float DRmax_                = 0.5;
        int nStubsmin_              = 3;     // minimum number of stubs
        bool correctGMTPropForTkZ_  = true;
};

std::vector<int> Correlator_L1TTgroup_impl::find_match(MuTkTree& mtkt, std::vector<int>* narbitrated)
{
    std::vector<int> num_arbitrated_per_cand;
    std::vector<int>* num_arbitrated_per_cand_ptr = (narbitrated ? &num_arbitrated_per_cand : nullptr);

    auto tkmus = make_tkmu(mtkt, num_arbitrated_per_cand_ptr); // is a vector of pairs (itrk, iemtf)
    // put in the interface format

    std::vector<int> out (*(mtkt.n_L1TT_trk), -1);
    if (narbitrated)
      narbitrated->resize(*(mtkt.n_L1TT_trk), 0);
    
    for (uint imutk = 0; imutk < tkmus.size(); ++imutk)
    {
        int itrack = tkmus.at(imutk).first;
        int iemtf  = tkmus.at(imutk).second;
        out.at(itrack) = iemtf; 
        if (narbitrated){
          narbitrated->at(itrack) = num_arbitrated_per_cand_ptr->at(imutk);
        }

    }
    return out;
}

// -----------------------------------------------------------------------------------------------
std::vector<std::pair<int,int>> Correlator_L1TTgroup_impl::make_tkmu(MuTkTree& mtkt, std::vector<int>* narbitrated)
{
  std::vector<std::pair<int,int>> result;
  
  if (narbitrated)
    narbitrated->clear();

  for (int iemtf = 0; iemtf < *(mtkt.n_EMTF_mu); ++iemtf){

    float l1mu_eta = mtkt.EMTF_mu_eta.At(iemtf);
    float l1mu_phi = deg_to_rad(mtkt.EMTF_mu_phi.At(iemtf)) ;;

    float l1mu_feta = std::fabs( l1mu_eta );
    if (l1mu_feta < ETAMIN_) continue;
    if (l1mu_feta > ETAMAX_) continue;

    float drmin = 999;
    float ptmax = -1;
    if (ptmax < 0) ptmax = -1;  // dummy

    PropState matchProp;
    int match_idx = -1;

    int n_matched_trks = 0;    

    for (int itrk = 0; itrk < *(mtkt.n_L1TT_trk); ++itrk){

      // unsigned int nPars = 4;
      // if (use5ParameterFit_) nPars = 5;
      float l1tk_pt = mtkt.L1TT_trk_pt.At(itrk);
      if (l1tk_pt < PTMINTRA_) continue;

      float l1tk_z  = mtkt.L1TT_trk_z.At(itrk);
      if (fabs(l1tk_z) > ZMAX_) continue;

      float l1tk_chi2 = mtkt.L1TT_trk_chi2.At(itrk);
      if (l1tk_chi2 > CHI2MAX_) continue;

      int l1tk_nstubs = mtkt.L1TT_trk_nstubs.At(itrk);
      if ( l1tk_nstubs < nStubsmin_) continue;

      float l1tk_eta = mtkt.L1TT_trk_eta.At(itrk);
      float l1tk_phi = mtkt.L1TT_trk_phi.At(itrk);

      float dr2 = deltaR2(l1mu_eta, l1mu_phi, l1tk_eta, l1tk_phi);
      if (dr2 > 0.3) continue;

      const PropState& pstate = propagateToGMT(mtkt, itrk);
      if (!pstate.valid) continue;

      float dr2prop = deltaR2(l1mu_eta, l1mu_phi, pstate.eta, pstate.phi);
      // FIXME: check if this matching procedure can be improved with
      // a pT dependent dR window
      
      if (dr2prop < DRmax_)
      {
        // everything here is a potntial candidate.
        // the code below will only pick up the closest one
        ++n_matched_trks;

        if (dr2prop < drmin){
          drmin = dr2prop;
          match_idx = itrk;
          matchProp = pstate;
        }
      }
      
    }// over l1tks

    if (match_idx >= 0){
      // const L1TTTrackType& matchTk = l1tks[match_idx];

      // float etaCut = 3.*sqrt(l1mu->hwDEtaExtra()*l1mu->hwDEtaExtra() + matchProp.sigmaEta*matchProp.sigmaEta);
      // float phiCut = 4.*sqrt(l1mu->hwDPhiExtra()*l1mu->hwDPhiExtra() + matchProp.sigmaPhi*matchProp.sigmaPhi);

      // float dEta = std::abs(matchProp.eta - l1mu->eta());
      // float dPhi = std::abs(deltaPhi(matchProp.phi, l1mu->phi()));

      // LogDebug("MYDEBUG")<<"match details: prop "<<matchProp.pt<<" "<<matchProp.eta<<" "<<matchProp.phi
            //  <<" mutk "<<l1mu->pt()<<" "<<l1mu->eta()<<" "<<l1mu->phi()<<" delta "<<dEta<<" "<<dPhi<<" cut "<<etaCut<<" "<<phiCut;
      // if (drmin < DRmax_){
      if (true){ // drmin moved above

        // unsigned int nPars = 4;
        // if (use5ParameterFit_) nPars = 5;
        // const auto& p3 = matchTk.getMomentum(nPars);
        // float p4e = sqrt(0.105658369*0.105658369 + p3.mag2() );

        // math::XYZTLorentzVector l1tkp4(p3.x(), p3.y(), p3.z(), p4e);

        // const auto& tkv3=matchTk.getPOCA(nPars);
        // math::XYZPoint v3(tkv3.x(), tkv3.y(), tkv3.z());
        // float trkisol = -999;

        // L1TkMuonParticle l1tkmu(l1tkp4, l1muRef, l1tkPtr, trkisol);
        // l1tkmu.setTrkzVtx( (float)tkv3.z() );

        // tkMuons.push_back(l1tkmu);
        result.push_back(std::make_pair(match_idx, iemtf));
        if (narbitrated)
          narbitrated->push_back(n_matched_trks);
      } // if there is a fine match
    } // if there is a coarse match
  }//over l1mus

  // never happens, good
  // if (result.size() > *(mtkt.n_EMTF_mu))
  //   std::cout << "HOW IS THIS POSSIBLE?? " << result.size() << " " << *(mtkt.n_EMTF_mu) << std::endl;

  // std::cout << "RESULT: " << result.size() << " ARB " << narbitrated->size() << std::endl;
  // for (uint i = 0; i < result.size(); ++i)
  // {
  //   std::cout << i << ") " << result.at(i).first << " " << result.at(i).second << " -- " << narbitrated->at(i) << std::endl;
  // }

  return result;
}



Correlator_L1TTgroup_impl::PropState Correlator_L1TTgroup_impl::propagateToGMT (MuTkTree& mtkt, int itrk)
{

    float tk_pt   = mtkt.L1TT_trk_pt.At(itrk);     //  p3.perp();
    float tk_p    = mtkt.L1TT_trk_p.At(itrk);      //  p3.mag();
    float tk_eta  = mtkt.L1TT_trk_eta.At(itrk);    //  p3.eta();
    float tk_aeta = std::abs(tk_eta);;             //  std::abs(tk_eta);
    float tk_phi  = mtkt.L1TT_trk_phi.At(itrk);    //  p3.phi();
    float tk_q    = mtkt.L1TT_trk_charge.At(itrk); //  tk.getRInv()>0? 1.: -1.;
    float tk_z    = mtkt.L1TT_trk_z.At(itrk);      //  tk.getPOCA().z();
    if (!correctGMTPropForTkZ_) tk_z = 0;

    Correlator_L1TTgroup_impl::PropState dest;
    if (tk_p<3.5 ) return dest;
    if (tk_aeta <1.1 && tk_pt < 3.5) return dest;
    if (tk_aeta > 2.5) return dest;

    //0th order:
    dest.valid = true;

    float dzCorrPhi = 1.;
    float deta = 0;
    float etaProp = tk_aeta;

    if (tk_aeta < 1.1){
    etaProp = 1.1;
    deta = tk_z/550./cosh(tk_aeta);
    } else {
    float delta = tk_z/850.; //roughly scales as distance to 2nd station
    if (tk_eta > 0) delta *=-1;
    dzCorrPhi = 1. + delta;

    float zOzs = tk_z/850.;
    if (tk_eta > 0) deta = zOzs/(1. - zOzs);
    else deta = zOzs/(1.+zOzs);
    deta = deta*tanh(tk_eta);
    }
    float resPhi = tk_phi - 1.464*tk_q*cosh(1.7)/cosh(etaProp)/tk_pt*dzCorrPhi - M_PI/144.;
    if (resPhi > M_PI) resPhi -= 2.*M_PI;
    if (resPhi < -M_PI) resPhi += 2.*M_PI;

    dest.eta = tk_eta + deta;
    dest.phi = resPhi;
    dest.pt = tk_pt; //not corrected for eloss

    dest.sigmaEta = 0.100/tk_pt; //multiple scattering term
    dest.sigmaPhi = 0.106/tk_pt; //need a better estimate for these
    return dest;
}

// bool Correlator_L1TTgroup_impl::filter_track   (MuTkTree& mtkt, int itrk)
// {

// }


// Correlator_L1TTgroup_impl::filter_emtf (MuTkTree& mtkt, int iemtf)
// {
//     float l1mu_eta = mtkt.EMTF_mu_eta.At(iemtf);
//     float l1mu_phi = deg_to_rad(mtkt.EMTF_mu_phi.At(iemtf)) ;;

//     float ETAMIN_ = 0.0;
//     float ETAMAX_ = 5.0;

//     float l1mu_feta = std::fabs( l1mu_eta );
//     if (l1mu_feta < ETAMIN_) return false;
//     if (l1mu_feta > ETAMAX_) return false;

//     return true;
// }

#endif
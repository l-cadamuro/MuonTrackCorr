#ifndef MUTKTREE_H
#define MUTKTREE_H

#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include "TTree.h"
#include "TChain.h"
#include "TFile.h"

class MuTkTree {

    public:
        MuTkTree(TChain* ch) :  mtktread(ch) {}
        ~MuTkTree(){};
        bool Next() {return mtktread.Next();}

        TTreeReader mtktread;
        /////////////////////////////////////////////////////////////////////
        // Readers to access the data (delete the ones you do not need).

        TTreeReaderValue<UInt_t> n_EMTF_mu     = {mtktread, "n_EMTF_mu"};
        TTreeReaderArray<float> EMTF_mu_pt     = {mtktread, "EMTF_mu_pt"};
        TTreeReaderArray<float> EMTF_mu_pt_xml = {mtktread, "EMTF_mu_pt_xml"};
        TTreeReaderArray<float> EMTF_mu_eta    = {mtktread, "EMTF_mu_eta"};
        TTreeReaderArray<float> EMTF_mu_theta  = {mtktread, "EMTF_mu_theta"};
        TTreeReaderArray<float> EMTF_mu_phi    = {mtktread, "EMTF_mu_phi"};
        TTreeReaderArray<int> EMTF_mu_charge   = {mtktread, "EMTF_mu_charge"};
        TTreeReaderArray<int> EMTF_mu_mode     = {mtktread, "EMTF_mu_mode"};
        TTreeReaderArray<int> EMTF_mu_endcap   = {mtktread, "EMTF_mu_endcap"};
        TTreeReaderArray<int> EMTF_mu_sector   = {mtktread, "EMTF_mu_sector"};
        TTreeReaderArray<int> EMTF_mu_bx       = {mtktread, "EMTF_mu_bx"};
        TTreeReaderArray<int> EMTF_mu_hitref1  = {mtktread, "EMTF_mu_hitref1"};
        TTreeReaderArray<int> EMTF_mu_hitref2  = {mtktread, "EMTF_mu_hitref2"};
        TTreeReaderArray<int> EMTF_mu_hitref3  = {mtktread, "EMTF_mu_hitref3"};
        TTreeReaderArray<int> EMTF_mu_hitref4  = {mtktread, "EMTF_mu_hitref4"};

        TTreeReaderValue<UInt_t> n_L1TT_trk     = {mtktread, "n_L1TT_trk"};
        TTreeReaderArray<float> L1TT_trk_pt     = {mtktread, "L1TT_trk_pt"};
        TTreeReaderArray<float> L1TT_trk_eta    = {mtktread, "L1TT_trk_eta"};
        TTreeReaderArray<float> L1TT_trk_phi    = {mtktread, "L1TT_trk_phi"};
        // TTreeReaderArray<int>   L1TT_trk_charge = {mtktread, "L1TT_trk_charge"};

        TTreeReaderValue<UInt_t> n_gen_mu      = {mtktread, "n_gen_mu"};
        TTreeReaderArray<float> gen_mu_pt      = {mtktread, "gen_mu_pt"};
        TTreeReaderArray<float> gen_mu_eta     = {mtktread, "gen_mu_eta"};
        TTreeReaderArray<float> gen_mu_phi     = {mtktread, "gen_mu_phi"};
        TTreeReaderArray<float> gen_mu_e       = {mtktread, "gen_mu_e"};
        TTreeReaderArray<int> gen_mu_charge    = {mtktread, "gen_mu_charge"};

        TTreeReaderValue<UInt_t> n_mu_hit        = {mtktread, "n_mu_hit"};
        TTreeReaderArray<short> mu_hit_endcap    = {mtktread, "mu_hit_endcap"};
        TTreeReaderArray<short> mu_hit_station   = {mtktread, "mu_hit_station"};
        TTreeReaderArray<short> mu_hit_ring      = {mtktread, "mu_hit_ring"};
        TTreeReaderArray<short> mu_hit_sector    = {mtktread, "mu_hit_sector"};
        TTreeReaderArray<short> mu_hit_subsector = {mtktread, "mu_hit_subsector"};
        TTreeReaderArray<short> mu_hit_chamber   = {mtktread, "mu_hit_chamber"};
        TTreeReaderArray<short> mu_hit_cscid     = {mtktread, "mu_hit_cscid"};
        TTreeReaderArray<short> mu_hit_bx        = {mtktread, "mu_hit_bx"};
        TTreeReaderArray<short> mu_hit_type      = {mtktread, "mu_hit_type"};
        TTreeReaderArray<short> mu_hit_neighbor  = {mtktread, "mu_hit_neighbor"};
        TTreeReaderArray<float> mu_hit_sim_phi   = {mtktread, "mu_hit_sim_phi"};
        TTreeReaderArray<float> mu_hit_sim_theta = {mtktread, "mu_hit_sim_theta"};
        TTreeReaderArray<float> mu_hit_sim_eta   = {mtktread, "mu_hit_sim_eta"};        
};

#endif
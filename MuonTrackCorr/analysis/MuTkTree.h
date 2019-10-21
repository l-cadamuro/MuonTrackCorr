#ifndef MUTKTREE_H
#define MUTKTREE_H

// to override the version at compile time add -D CUSTOM_TREE_VERSION -D TREEVERSION=<VNUMBER>
#ifndef CUSTOM_TREE_VERSION
// #define TREEVERSION 0 // the original version used for corr developments
// #define TREEVERSION 1 // added barrel and muon endcap
#define TREEVERSION 2 // added matched gen track info and extra EMTF hit properties
#endif

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

        #if TREEVERSION >= 1
            TTreeReaderValue<UInt_t> n_barrel_mu     = {mtktread, "n_barrel_mu"};
            TTreeReaderArray<float> barrel_mu_pt     = {mtktread, "barrel_mu_pt"};
            TTreeReaderArray<float> barrel_mu_eta    = {mtktread, "barrel_mu_eta"};
            TTreeReaderArray<float> barrel_mu_phi    = {mtktread, "barrel_mu_phi"};
            TTreeReaderArray<int>   barrel_mu_charge = {mtktread, "barrel_mu_charge"};

            TTreeReaderValue<UInt_t> n_ovrlap_mu     = {mtktread, "n_ovrlap_mu"};
            TTreeReaderArray<float> ovrlap_mu_pt     = {mtktread, "ovrlap_mu_pt"};
            TTreeReaderArray<float> ovrlap_mu_eta    = {mtktread, "ovrlap_mu_eta"};
            TTreeReaderArray<float> ovrlap_mu_phi    = {mtktread, "ovrlap_mu_phi"};
            TTreeReaderArray<int>   ovrlap_mu_charge = {mtktread, "ovrlap_mu_charge"};
        #endif

        TTreeReaderValue<UInt_t> n_L1TT_trk     = {mtktread, "n_L1TT_trk"};
        TTreeReaderArray<float> L1TT_trk_pt     = {mtktread, "L1TT_trk_pt"};
        TTreeReaderArray<float> L1TT_trk_eta    = {mtktread, "L1TT_trk_eta"};
        TTreeReaderArray<float> L1TT_trk_phi    = {mtktread, "L1TT_trk_phi"};
        TTreeReaderArray<int>   L1TT_trk_charge = {mtktread, "L1TT_trk_charge"};
        TTreeReaderArray<float> L1TT_trk_p      = {mtktread, "L1TT_trk_p"};
        TTreeReaderArray<float> L1TT_trk_z      = {mtktread, "L1TT_trk_z"};
        TTreeReaderArray<float> L1TT_trk_chi2   = {mtktread, "L1TT_trk_chi2"};
        TTreeReaderArray<int>   L1TT_trk_nstubs = {mtktread, "L1TT_trk_nstubs"};
        #if TREEVERSION >= 2
           TTreeReaderArray<int>   L1TT_trk_gen_qual   = {mtktread, "L1TT_trk_gen_qual"};
           TTreeReaderArray<int>   L1TT_trk_gen_TP_ID  = {mtktread, "L1TT_trk_gen_TP_ID"};
           TTreeReaderArray<float> L1TT_trk_gen_TP_pt  = {mtktread, "L1TT_trk_gen_TP_pt"};
           TTreeReaderArray<float> L1TT_trk_gen_TP_eta = {mtktread, "L1TT_trk_gen_TP_eta"};
           TTreeReaderArray<float> L1TT_trk_gen_TP_phi = {mtktread, "L1TT_trk_gen_TP_phi"};
           TTreeReaderArray<float> L1TT_trk_gen_TP_m   = {mtktread, "L1TT_trk_gen_TP_m"};
        #endif

        TTreeReaderValue<UInt_t> n_L1_TkMu     = {mtktread, "n_L1_TkMu"};
        TTreeReaderArray<float> L1_TkMu_pt     = {mtktread, "L1_TkMu_pt"};
        TTreeReaderArray<float> L1_TkMu_eta    = {mtktread, "L1_TkMu_eta"};
        TTreeReaderArray<float> L1_TkMu_phi    = {mtktread, "L1_TkMu_phi"};
        #if TREEVERSION >= 2
           TTreeReaderArray<int>   L1_TkMu_charge     = {mtktread, "L1_TkMu_charge"};
           TTreeReaderArray<float> L1_TkMu_p          = {mtktread, "L1_TkMu_p"};
           TTreeReaderArray<float> L1_TkMu_z          = {mtktread, "L1_TkMu_z"};
           TTreeReaderArray<float> L1_TkMu_chi2       = {mtktread, "L1_TkMu_chi2"};
           TTreeReaderArray<int>   L1_TkMu_nstubs     = {mtktread, "L1_TkMu_nstubs"};
           TTreeReaderArray<int>   L1_TkMu_mudetID    = {mtktread, "L1_TkMu_mudetID"};
           TTreeReaderArray<int>   L1_TkMu_gen_qual   = {mtktread, "L1_TkMu_gen_qual"};
           TTreeReaderArray<int>   L1_TkMu_gen_TP_ID  = {mtktread, "L1_TkMu_gen_TP_ID"};
           TTreeReaderArray<float> L1_TkMu_gen_TP_pt  = {mtktread, "L1_TkMu_gen_TP_pt"};
           TTreeReaderArray<float> L1_TkMu_gen_TP_eta = {mtktread, "L1_TkMu_gen_TP_eta"};
           TTreeReaderArray<float> L1_TkMu_gen_TP_phi = {mtktread, "L1_TkMu_gen_TP_phi"};
           TTreeReaderArray<float> L1_TkMu_gen_TP_m   = {mtktread, "L1_TkMu_gen_TP_m"};
        #endif

        // NB: TkMuStub was actually available since earlier tree version but unused so far
        // I'm adding all (30/09/2019) as if version 2 and commenting out as it's currently unused
        #if TREEVERSION >= 2 
           TTreeReaderValue<UInt_t> n_L1_TkMuStub          = {mtktread, "n_L1_TkMuStub"};
           TTreeReaderArray<float>  L1_TkMuStub_pt         = {mtktread, "L1_TkMuStub_pt"};
           TTreeReaderArray<float>  L1_TkMuStub_eta        = {mtktread, "L1_TkMuStub_eta"};
           TTreeReaderArray<float>  L1_TkMuStub_phi        = {mtktread, "L1_TkMuStub_phi"};
           TTreeReaderArray<int>    L1_TkMuStub_charge     = {mtktread, "L1_TkMuStub_charge"};
           TTreeReaderArray<float>  L1_TkMuStub_p          = {mtktread, "L1_TkMuStub_p"};
           TTreeReaderArray<float>  L1_TkMuStub_z          = {mtktread, "L1_TkMuStub_z"};
           TTreeReaderArray<float>  L1_TkMuStub_chi2       = {mtktread, "L1_TkMuStub_chi2"};
           TTreeReaderArray<int>    L1_TkMuStub_nstubs     = {mtktread, "L1_TkMuStub_nstubs"};
           TTreeReaderArray<int>    L1_TkMuStub_gen_qual   = {mtktread, "L1_TkMuStub_gen_qual"};
           TTreeReaderArray<int>    L1_TkMuStub_gen_TP_ID  = {mtktread, "L1_TkMuStub_gen_TP_ID"};
           TTreeReaderArray<float>  L1_TkMuStub_gen_TP_pt  = {mtktread, "L1_TkMuStub_gen_TP_pt"};
           TTreeReaderArray<float>  L1_TkMuStub_gen_TP_eta = {mtktread, "L1_TkMuStub_gen_TP_eta"};
           TTreeReaderArray<float>  L1_TkMuStub_gen_TP_phi = {mtktread, "L1_TkMuStub_gen_TP_phi"};
           TTreeReaderArray<float>  L1_TkMuStub_gen_TP_m   = {mtktread, "L1_TkMuStub_gen_TP_m"};            
        #endif

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
        #if TREEVERSION >= 2 
           TTreeReaderArray<short> mu_hit_strip    = {mtktread, "mu_hit_strip"};
           TTreeReaderArray<short> mu_hit_wire     = {mtktread, "mu_hit_wire"};
           TTreeReaderArray<short> mu_hit_roll     = {mtktread, "mu_hit_roll"};
           TTreeReaderArray<short> mu_hit_quality  = {mtktread, "mu_hit_quality"};
           TTreeReaderArray<short> mu_hit_pattern  = {mtktread, "mu_hit_pattern"};
           TTreeReaderArray<short> mu_hit_bend     = {mtktread, "mu_hit_bend"};
           TTreeReaderArray<short> mu_hit_time     = {mtktread, "mu_hit_time"};
           TTreeReaderArray<short> mu_hit_fr       = {mtktread, "mu_hit_fr"};
           TTreeReaderArray<int> mu_hit_emtf_phi   = {mtktread, "mu_hit_emtf_phi"};
           TTreeReaderArray<int> mu_hit_emtf_theta = {mtktread, "mu_hit_emtf_theta"};
        #endif
        TTreeReaderArray<float> mu_hit_sim_phi   = {mtktread, "mu_hit_sim_phi"};
        TTreeReaderArray<float> mu_hit_sim_theta = {mtktread, "mu_hit_sim_theta"};
        TTreeReaderArray<float> mu_hit_sim_eta   = {mtktread, "mu_hit_sim_eta"};        
        #if TREEVERSION >= 2 
           TTreeReaderArray<float> mu_hit_sim_r = {mtktread, "mu_hit_sim_r"};
           TTreeReaderArray<float> mu_hit_sim_z = {mtktread, "mu_hit_sim_z"};
        #endif
};

#endif
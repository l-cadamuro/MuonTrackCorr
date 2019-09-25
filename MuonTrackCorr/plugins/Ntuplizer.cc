#ifndef NTUPLIZER_H
#define NTUPLIZER_H

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/Common/interface/RefVector.h"
#include "DataFormats/Common/interface/DetSetVectorNew.h"
#include "DataFormats/L1Trigger/interface/Muon.h"
#include "DataFormats/L1TrackTrigger/interface/TTTrack.h"
#include "DataFormats/L1TrackTrigger/interface/TTTypes.h"
#include "DataFormats/L1TMuon/interface/EMTFTrack.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenStatusFlags.h"

#include "DataFormats/L1TrackTrigger/interface/L1TkMuonParticle.h"
#include "DataFormats/L1TrackTrigger/interface/L1TkMuonParticleFwd.h"

#include "L1Trigger/L1TMuon/interface/MicroGMTConfiguration.h"

#include "TTree.h"

using namespace edm;
using namespace l1t;
using namespace reco;

// From L1Trigger/L1TMuonEndCap/interface/MuonTriggerPrimitive.h
class TriggerPrimitive {
public:
  enum subsystem_type{kDT,kCSC,kRPC,kGEM,kME0,kNSubsystems};
};

class Ntuplizer : public edm::EDAnalyzer {
    public:

        typedef TTTrack< Ref_Phase2TrackerDigi_ >  L1TTTrackType;
        typedef std::vector< L1TTTrackType >       L1TTTrackCollectionType;
        typedef std::vector< GenParticle >         GenParticleCollection;

        explicit Ntuplizer(const edm::ParameterSet&);
        virtual ~Ntuplizer();

    private:
        //----edm control---
        virtual void beginJob() ;
        virtual void beginRun(edm::Run const&, edm::EventSetup const&);
        virtual void analyze(const edm::Event&, const edm::EventSetup&);
        virtual void endJob();
        virtual void endRun(edm::Run const&, edm::EventSetup const&);
        void initialize();

        // const edm::EDGetTokenT< MuonBxCollection > muTokenPos;
        // const edm::EDGetTokenT< MuonBxCollection > muTokenNeg;
        const edm::EDGetTokenT< EMTFTrackCollection > muToken;
        const edm::EDGetTokenT< EMTFHitCollection >   mu_hitToken;
        const edm::EDGetTokenT< std::vector< TTTrack< Ref_Phase2TrackerDigi_ > > > trackToken;
        const edm::EDGetTokenT< std::vector< reco::GenParticle > > genPartToken;
        const edm::EDGetTokenT< L1TkMuonParticleCollection > tkMuToken;
        const edm::EDGetTokenT< L1TkMuonParticleCollection > tkMuStubToken;
        const edm::EDGetTokenT< RegionalMuonCandBxCollection > muBarrelToken;
        const edm::EDGetTokenT< RegionalMuonCandBxCollection > muOvrlapToken;

        const static int nTrkPars = 4; // number of parameters in the trk fit -- eventually to be made configurable

        //
        bool save_all_trks_;
        bool prompt_mu_only_;
        bool mu_from_tau_only_;
        bool save_tau_3mu_;
        //

        //-----output---
        TTree *tree_;

        unsigned int n_EMTF_mu_;
        std::vector<float> EMTF_mu_pt_;
        std::vector<float> EMTF_mu_pt_xml_;
        std::vector<float> EMTF_mu_eta_;
        std::vector<float> EMTF_mu_theta_;
        std::vector<float> EMTF_mu_phi_;
        std::vector<int>   EMTF_mu_charge_;
        std::vector<int>   EMTF_mu_mode_;
        std::vector<int>   EMTF_mu_endcap_;
        std::vector<int>   EMTF_mu_sector_;
        std::vector<int>   EMTF_mu_bx_;
        std::vector<int>   EMTF_mu_hitref1_;
        std::vector<int>   EMTF_mu_hitref2_;
        std::vector<int>   EMTF_mu_hitref3_;
        std::vector<int>   EMTF_mu_hitref4_;
        // std::vector<float> EMTF_mu_e_;

        unsigned int n_barrel_mu_;
        std::vector<float> barrel_mu_pt_;
        std::vector<float> barrel_mu_eta_;
        std::vector<float> barrel_mu_phi_;
        std::vector<int>   barrel_mu_charge_;

        unsigned int n_ovrlap_mu_;
        std::vector<float> ovrlap_mu_pt_;
        std::vector<float> ovrlap_mu_eta_;
        std::vector<float> ovrlap_mu_phi_;
        std::vector<int>   ovrlap_mu_charge_;

        // hits of a EMTF track
        // std::vector<int>   EMTF_mu_h1_type_;
        // std::vector<int>   EMTF_mu_h2_type_;
        // std::vector<int>   EMTF_mu_h3_type_;
        // std::vector<int>   EMTF_mu_h4_type_;

        unsigned int n_L1TT_trk_;
        std::vector<float> L1TT_trk_pt_;
        std::vector<float> L1TT_trk_eta_;
        std::vector<float> L1TT_trk_phi_;
        std::vector<int> L1TT_trk_charge_;
        std::vector<float> L1TT_trk_p_;
        std::vector<float> L1TT_trk_z_;
        std::vector<float> L1TT_trk_chi2_;
        std::vector<int> L1TT_trk_nstubs_;

        unsigned int n_L1_TkMu_;
        std::vector<float> L1_TkMu_pt_;
        std::vector<float> L1_TkMu_eta_;
        std::vector<float> L1_TkMu_phi_;
        std::vector<int>   L1_TkMu_charge_;
        std::vector<float> L1_TkMu_p_;
        std::vector<float> L1_TkMu_z_;
        std::vector<float> L1_TkMu_chi2_;
        std::vector<int>   L1_TkMu_nstubs_;
        std::vector<int>   L1_TkMu_mudetID_;
        // std::vector<float> L1_TkMu_e_;
        // std::vector<int> L1_TkMu_charge_;

        unsigned int n_L1_TkMuStub_;
        std::vector<float> L1_TkMuStub_pt_;
        std::vector<float> L1_TkMuStub_eta_;
        std::vector<float> L1_TkMuStub_phi_;
        std::vector<int>   L1_TkMuStub_charge_;
        std::vector<float> L1_TkMuStub_p_;
        std::vector<float> L1_TkMuStub_z_;
        std::vector<float> L1_TkMuStub_chi2_;
        std::vector<int>   L1_TkMuStub_nstubs_;

        unsigned int n_gen_mu_;
        std::vector<float> gen_mu_pt_;
        std::vector<float> gen_mu_eta_;
        std::vector<float> gen_mu_phi_;
        std::vector<float> gen_mu_e_;
        std::vector<int>   gen_mu_charge_;
        std::vector<int>   gen_mu_gentauidx_;

        unsigned int n_gen_tau_;
        std::vector<float> gen_tau_pt_;
        std::vector<float> gen_tau_eta_;
        std::vector<float> gen_tau_phi_;
        std::vector<float> gen_tau_e_;
        std::vector<int>   gen_tau_charge_;

        // hits
        // format taken from : https://github.com/jiafulow/L1TMuonSimulationsMar2017/blob/master/Analyzers/plugins/NtupleMaker.cc
        unsigned int n_mu_hit_;
        std::vector<int16_t>  mu_hit_endcap_;
        std::vector<int16_t>  mu_hit_station_;
        std::vector<int16_t>  mu_hit_ring_;
        std::vector<int16_t>  mu_hit_sector_;
        std::vector<int16_t>  mu_hit_subsector_;
        std::vector<int16_t>  mu_hit_chamber_;
        std::vector<int16_t>  mu_hit_cscid_;
        std::vector<int16_t>  mu_hit_bx_;
        std::vector<int16_t>  mu_hit_type_;  // subsystem: DT=0,CSC=1,RPC=2,GEM=3
        std::vector<int16_t>  mu_hit_neighbor_;
        //
        std::vector<int16_t>  mu_hit_strip_;
        std::vector<int16_t>  mu_hit_wire_;
        std::vector<int16_t>  mu_hit_roll_;
        std::vector<int16_t>  mu_hit_quality_;
        std::vector<int16_t>  mu_hit_pattern_;
        std::vector<int16_t>  mu_hit_bend_;
        std::vector<int16_t>  mu_hit_time_;
        std::vector<int16_t>  mu_hit_fr_;
        std::vector<int32_t>  mu_hit_emtf_phi_;
        std::vector<int32_t>  mu_hit_emtf_theta_;
        //
        std::vector<float  >  mu_hit_sim_phi_;
        std::vector<float  >  mu_hit_sim_theta_;
        std::vector<float  >  mu_hit_sim_eta_;
        std::vector<float  >  mu_hit_sim_r_; // seems not there in the CMSSW emulator data format
        std::vector<float  >  mu_hit_sim_z_; // seems not there in the CMSSW emulator data format
};

void Ntuplizer::initialize()
{
    n_EMTF_mu_  = 0;
    EMTF_mu_pt_.clear();
    EMTF_mu_pt_xml_.clear();
    EMTF_mu_eta_.clear();
    EMTF_mu_theta_.clear();
    EMTF_mu_phi_.clear();
    EMTF_mu_charge_.clear();
    EMTF_mu_mode_.clear();
    EMTF_mu_endcap_.clear();
    EMTF_mu_sector_.clear();
    EMTF_mu_bx_.clear();
    EMTF_mu_hitref1_.clear();
    EMTF_mu_hitref2_.clear();
    EMTF_mu_hitref3_.clear();
    EMTF_mu_hitref4_.clear();

    n_barrel_mu_ = 0;
    barrel_mu_pt_.clear();
    barrel_mu_eta_.clear();
    barrel_mu_phi_.clear();
    barrel_mu_charge_.clear();

    n_ovrlap_mu_ = 0;
    ovrlap_mu_pt_.clear();
    ovrlap_mu_eta_.clear();
    ovrlap_mu_phi_.clear();
    ovrlap_mu_charge_.clear();


    n_L1TT_trk_ = 0;
    L1TT_trk_pt_.clear();
    L1TT_trk_eta_.clear();
    L1TT_trk_phi_.clear();
    L1TT_trk_charge_.clear();
    L1TT_trk_p_.clear();
    L1TT_trk_z_.clear();
    L1TT_trk_chi2_.clear();
    L1TT_trk_nstubs_.clear();

    n_L1_TkMu_ = 0;
    L1_TkMu_pt_.clear();
    L1_TkMu_eta_.clear();
    L1_TkMu_phi_.clear();
    L1_TkMu_charge_.clear();
    L1_TkMu_p_.clear();
    L1_TkMu_z_.clear();
    L1_TkMu_chi2_.clear();
    L1_TkMu_nstubs_.clear();
    L1_TkMu_mudetID_.clear();
    // L1_TkMu_charge_.clear();

    n_L1_TkMuStub_ = 0;
    L1_TkMuStub_pt_.clear();
    L1_TkMuStub_eta_.clear();
    L1_TkMuStub_phi_.clear();
    L1_TkMuStub_charge_.clear();
    L1_TkMuStub_p_.clear();
    L1_TkMuStub_z_.clear();
    L1_TkMuStub_chi2_.clear();
    L1_TkMuStub_nstubs_.clear();

    n_gen_mu_   = 0;
    gen_mu_pt_.clear();
    gen_mu_eta_.clear();
    gen_mu_phi_.clear();
    gen_mu_e_.clear();
    gen_mu_charge_.clear();
    gen_mu_gentauidx_.clear();

    n_gen_tau_   = 0;
    gen_tau_pt_.clear();
    gen_tau_eta_.clear();
    gen_tau_phi_.clear();
    gen_tau_e_.clear();
    gen_tau_charge_.clear();

    n_mu_hit_ = 0;
    mu_hit_endcap_.clear();
    mu_hit_station_.clear();
    mu_hit_ring_.clear();
    mu_hit_sector_.clear();
    mu_hit_subsector_.clear();
    mu_hit_chamber_.clear();
    mu_hit_cscid_.clear();
    mu_hit_bx_.clear();
    mu_hit_type_.clear();
    mu_hit_neighbor_.clear();
    //
    mu_hit_strip_.clear();
    mu_hit_wire_.clear();
    mu_hit_roll_.clear();
    mu_hit_quality_.clear();
    mu_hit_pattern_.clear();
    mu_hit_bend_.clear();
    mu_hit_time_.clear();
    mu_hit_fr_.clear();
    mu_hit_emtf_phi_.clear();
    mu_hit_emtf_theta_.clear();
    //
    mu_hit_sim_phi_.clear();
    mu_hit_sim_theta_.clear();
    mu_hit_sim_eta_.clear();
    mu_hit_sim_r_.clear();
    mu_hit_sim_z_.clear();

}

Ntuplizer::Ntuplizer(const edm::ParameterSet& iConfig):
    // muTokenPos(consumes< MuonBxCollection >           (iConfig.getParameter<edm::InputTag>("L1MuonPosInputTag"))),
    // muTokenNeg(consumes< MuonBxCollection >           (iConfig.getParameter<edm::InputTag>("L1MuonNegInputTag"))),
    muToken       (consumes< EMTFTrackCollection >          (iConfig.getParameter<edm::InputTag>("L1MuonEMTFInputTag"))),
    mu_hitToken   (consumes< EMTFHitCollection >            (iConfig.getParameter<edm::InputTag>("L1EMTFHitInputTag"))),
    trackToken    (consumes< L1TTTrackCollectionType >      (iConfig.getParameter<edm::InputTag>("L1TrackInputTag"))),
    genPartToken  (consumes< GenParticleCollection >        (iConfig.getParameter<edm::InputTag>("GenParticleInputTag"))),
    tkMuToken     (consumes< L1TkMuonParticleCollection >   (iConfig.getParameter<edm::InputTag>("TkMuInputTag"))),
    tkMuStubToken (consumes< L1TkMuonParticleCollection >   (iConfig.getParameter<edm::InputTag>("TkMuStubInputTag"))),
    muBarrelToken (consumes< RegionalMuonCandBxCollection > (iConfig.getParameter<edm::InputTag>("L1BarrelMuonInputTag"))),
    muOvrlapToken (consumes< RegionalMuonCandBxCollection > (iConfig.getParameter<edm::InputTag>("L1OverlapMuonInputTag")))

{
    save_all_trks_    =  iConfig.getParameter<bool>("save_all_L1TTT");
    prompt_mu_only_   =  iConfig.getParameter<bool>("prompt_mu_only");
    mu_from_tau_only_ =  iConfig.getParameter<bool>("mu_from_tau_only");
    save_tau_3mu_     =  iConfig.getParameter<bool>("save_tau_3mu");
    initialize();
}

Ntuplizer::~Ntuplizer()
{}

void Ntuplizer::beginJob()
{
    edm::Service<TFileService> fs;
    tree_ = fs -> make<TTree>("MuonTrackTree", "MuonTrackTree");

    tree_->Branch("n_EMTF_mu", &n_EMTF_mu_);
    tree_->Branch("EMTF_mu_pt", &EMTF_mu_pt_);
    tree_->Branch("EMTF_mu_pt_xml", &EMTF_mu_pt_xml_);
    tree_->Branch("EMTF_mu_eta", &EMTF_mu_eta_);
    tree_->Branch("EMTF_mu_theta", &EMTF_mu_theta_);
    tree_->Branch("EMTF_mu_phi", &EMTF_mu_phi_);
    tree_->Branch("EMTF_mu_charge", &EMTF_mu_charge_);
    tree_->Branch("EMTF_mu_mode", &EMTF_mu_mode_);
    tree_->Branch("EMTF_mu_endcap", &EMTF_mu_endcap_);
    tree_->Branch("EMTF_mu_sector", &EMTF_mu_sector_);
    tree_->Branch("EMTF_mu_bx", &EMTF_mu_bx_);
    tree_->Branch("EMTF_mu_hitref1", &EMTF_mu_hitref1_);
    tree_->Branch("EMTF_mu_hitref2", &EMTF_mu_hitref2_);
    tree_->Branch("EMTF_mu_hitref3", &EMTF_mu_hitref3_);
    tree_->Branch("EMTF_mu_hitref4", &EMTF_mu_hitref4_);


    tree_->Branch("n_barrel_mu",      &n_barrel_mu_);
    tree_->Branch("barrel_mu_pt",     &barrel_mu_pt_);
    tree_->Branch("barrel_mu_eta",    &barrel_mu_eta_);
    tree_->Branch("barrel_mu_phi",    &barrel_mu_phi_);
    tree_->Branch("barrel_mu_charge", &barrel_mu_charge_);

    tree_->Branch("n_ovrlap_mu",      &n_ovrlap_mu_);
    tree_->Branch("ovrlap_mu_pt",     &ovrlap_mu_pt_);
    tree_->Branch("ovrlap_mu_eta",    &ovrlap_mu_eta_);
    tree_->Branch("ovrlap_mu_phi",    &ovrlap_mu_phi_);
    tree_->Branch("ovrlap_mu_charge", &ovrlap_mu_charge_);

    // tree_->Branch("EMTF_mu_e", &EMTF_mu_e_);

    tree_->Branch("n_L1TT_trk", &n_L1TT_trk_);
    tree_->Branch("L1TT_trk_pt", &L1TT_trk_pt_);
    tree_->Branch("L1TT_trk_eta", &L1TT_trk_eta_);
    tree_->Branch("L1TT_trk_phi", &L1TT_trk_phi_);
    tree_->Branch("L1TT_trk_charge", &L1TT_trk_charge_);
    tree_->Branch("L1TT_trk_p", &L1TT_trk_p_);
    tree_->Branch("L1TT_trk_z", &L1TT_trk_z_);
    tree_->Branch("L1TT_trk_chi2", &L1TT_trk_chi2_);
    tree_->Branch("L1TT_trk_nstubs", &L1TT_trk_nstubs_);

    //
    tree_->Branch("n_L1_TkMu", &n_L1_TkMu_);
    tree_->Branch("L1_TkMu_pt", &L1_TkMu_pt_);
    tree_->Branch("L1_TkMu_eta", &L1_TkMu_eta_);
    tree_->Branch("L1_TkMu_phi", &L1_TkMu_phi_);
    tree_->Branch("L1_TkMu_charge", &L1_TkMu_charge_);
    tree_->Branch("L1_TkMu_p", &L1_TkMu_p_);
    tree_->Branch("L1_TkMu_z", &L1_TkMu_z_);
    tree_->Branch("L1_TkMu_chi2", &L1_TkMu_chi2_);
    tree_->Branch("L1_TkMu_nstubs", &L1_TkMu_nstubs_);
    tree_->Branch("L1_TkMu_mudetID", &L1_TkMu_mudetID_);

    tree_->Branch("n_L1_TkMuStub", &n_L1_TkMuStub_);
    tree_->Branch("L1_TkMuStub_pt", &L1_TkMuStub_pt_);
    tree_->Branch("L1_TkMuStub_eta", &L1_TkMuStub_eta_);
    tree_->Branch("L1_TkMuStub_phi", &L1_TkMuStub_phi_);
    tree_->Branch("L1_TkMuStub_charge", &L1_TkMuStub_charge_);
    tree_->Branch("L1_TkMuStub_p", &L1_TkMuStub_p_);
    tree_->Branch("L1_TkMuStub_z", &L1_TkMuStub_z_);
    tree_->Branch("L1_TkMuStub_chi2", &L1_TkMuStub_chi2_);
    tree_->Branch("L1_TkMuStub_nstubs", &L1_TkMuStub_nstubs_);

    tree_->Branch("n_gen_mu", &n_gen_mu_);
    tree_->Branch("gen_mu_pt", &gen_mu_pt_);
    tree_->Branch("gen_mu_eta", &gen_mu_eta_);
    tree_->Branch("gen_mu_phi", &gen_mu_phi_);
    tree_->Branch("gen_mu_e", &gen_mu_e_);
    tree_->Branch("gen_mu_charge", &gen_mu_charge_);
    if (save_tau_3mu_)
        tree_->Branch("gen_mu_gentauidx", &gen_mu_gentauidx_);

    // hit info
    tree_->Branch("n_mu_hit", &n_mu_hit_);
    tree_->Branch("mu_hit_endcap", &mu_hit_endcap_);
    tree_->Branch("mu_hit_station", &mu_hit_station_);
    tree_->Branch("mu_hit_ring", &mu_hit_ring_);
    tree_->Branch("mu_hit_sector", &mu_hit_sector_);
    tree_->Branch("mu_hit_subsector", &mu_hit_subsector_);
    tree_->Branch("mu_hit_chamber", &mu_hit_chamber_);
    tree_->Branch("mu_hit_cscid", &mu_hit_cscid_);
    tree_->Branch("mu_hit_bx", &mu_hit_bx_);
    tree_->Branch("mu_hit_type", &mu_hit_type_);
    tree_->Branch("mu_hit_neighbor", &mu_hit_neighbor_);
    //
    tree_->Branch("mu_hit_strip", &mu_hit_strip_);
    tree_->Branch("mu_hit_wire", &mu_hit_wire_);
    tree_->Branch("mu_hit_roll", &mu_hit_roll_);
    tree_->Branch("mu_hit_quality", &mu_hit_quality_);
    tree_->Branch("mu_hit_pattern", &mu_hit_pattern_);
    tree_->Branch("mu_hit_bend", &mu_hit_bend_);
    tree_->Branch("mu_hit_time", &mu_hit_time_);
    tree_->Branch("mu_hit_fr", &mu_hit_fr_);
    tree_->Branch("mu_hit_emtf_phi", &mu_hit_emtf_phi_);
    tree_->Branch("mu_hit_emtf_theta", &mu_hit_emtf_theta_);
    //
    tree_->Branch("mu_hit_sim_phi", &mu_hit_sim_phi_);
    tree_->Branch("mu_hit_sim_theta", &mu_hit_sim_theta_);
    tree_->Branch("mu_hit_sim_eta", &mu_hit_sim_eta_);
    tree_->Branch("mu_hit_sim_r", &mu_hit_sim_r_);
    tree_->Branch("mu_hit_sim_z", &mu_hit_sim_z_);

    //
    if (save_tau_3mu_)
    {
        tree_->Branch("n_gen_tau", &n_gen_tau_);
        tree_->Branch("gen_tau_pt", &gen_tau_pt_);
        tree_->Branch("gen_tau_eta", &gen_tau_eta_);
        tree_->Branch("gen_tau_phi", &gen_tau_phi_);
        tree_->Branch("gen_tau_e", &gen_tau_e_);
        tree_->Branch("gen_tau_charge", &gen_tau_charge_);   
    }
}

void Ntuplizer::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{}

void Ntuplizer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // --------- in-place function
    // from https://github.com/jiafulow/L1TMuonSimulationsMar2017/blob/master/Analyzers/plugins/NtupleMaker.cc#L374
    auto get_hit_refs = [](const auto& trk, const auto& hits) {
        using namespace l1t;

        std::vector<int32_t> hit_refs = {-1, -1, -1, -1};
        EMTFHitCollection::const_iterator conv_hits_it1  = trk.Hits().begin();
        EMTFHitCollection::const_iterator conv_hits_end1 = trk.Hits().end();

        for (; conv_hits_it1 != conv_hits_end1; ++conv_hits_it1) {
          EMTFHitCollection::const_iterator conv_hits_it2  = hits.begin();
          EMTFHitCollection::const_iterator conv_hits_end2 = hits.end();

          for (; conv_hits_it2 != conv_hits_end2; ++conv_hits_it2) {
            const EMTFHit& conv_hit_i = *conv_hits_it1;
            const EMTFHit& conv_hit_j = *conv_hits_it2;

            // See L1Trigger/L1TMuonEndCap/src/PrimitiveMatching.cc
            // All these must match: [bx_history][station][chamber][segment]
            if (
              (conv_hit_i.Subsystem()  == conv_hit_j.Subsystem()) &&
              (conv_hit_i.PC_station() == conv_hit_j.PC_station()) &&
              (conv_hit_i.PC_chamber() == conv_hit_j.PC_chamber()) &&
              (conv_hit_i.Ring()       == conv_hit_j.Ring()) &&  // because of ME1/1
              (conv_hit_i.Strip()      == conv_hit_j.Strip()) &&
              (conv_hit_i.Wire()       == conv_hit_j.Wire()) &&
              (conv_hit_i.Pattern()    == conv_hit_j.Pattern()) &&
              (conv_hit_i.BX()         == conv_hit_j.BX()) &&
              (conv_hit_i.Strip_low()  == conv_hit_j.Strip_low()) && // For RPC clusters
              (conv_hit_i.Strip_hi()   == conv_hit_j.Strip_hi()) &&  // For RPC clusters
              (conv_hit_i.Roll()       == conv_hit_j.Roll()) &&
              (conv_hit_i.Endcap()     == conv_hit_j.Endcap()) &&
              (conv_hit_i.Sector()     == conv_hit_j.Sector()) &&
              true
            ) {
              int istation = (conv_hit_i.Station() - 1);
              auto hit_ref = std::distance(hits.begin(), conv_hits_it2);
              hit_refs.at(istation) = hit_ref;
            }  // end if
          }  // end loop over hits
        }  // end loop over trk.Hits()

        // Sanity check
        for (int istation = 0; istation < 4; ++istation) {
          bool has_hit = trk.Mode() & (1 << (3 - istation));
          assert(has_hit == (hit_refs.at(istation) != -1));
        }

        return hit_refs;
    };

    // helper functions by Jia Fu
    // taken from https://github.com/jiafulow/L1TMuonSimulationsMar2017/blob/master/Analyzers/plugins/NtupleMaker.cc#L602
    auto get_pattern = [](const auto& hit) {
      int pattern = 0;
      if (hit.Subsystem() == TriggerPrimitive::kCSC) {
        pattern = hit.Pattern();
      } else if (hit.Subsystem() == TriggerPrimitive::kDT) {
        pattern = hit.Sync_err();  // syncErr was hacked to store rpc bit
      }
      return pattern;
    };
     
    auto get_time = [](const auto& hit) {
      float time = hit.Time();
      return static_cast<int>(std::round(time*16/25));  // integer unit is 25ns/16 (4-bit)
    };

    auto isFront_detail = [](int subsystem, int station, int ring, int chamber, int subsector) {
      bool result = false;
  
      if (subsystem == TriggerPrimitive::kCSC) {
        bool isOverlapping = !(station == 1 && ring == 3);
        // not overlapping means back
        if(isOverlapping)
        {
          bool isEven = (chamber % 2 == 0);
          // odd chambers are bolted to the iron, which faces
          // forward in 1&2, backward in 3&4, so...
          result = (station < 3) ? isEven : !isEven;
        }
      } else if (subsystem == TriggerPrimitive::kRPC) {
        //// 10 degree rings have even subsectors in front
        //// 20 degree rings have odd subsectors in front
        //bool is_10degree = !((station == 3 || station == 4) && (ring == 1));
        //bool isEven = (subsector % 2 == 0);
        //result = (is_10degree) ? isEven : !isEven;
  
        // Use the equivalent CSC chamber F/R
        bool isEven = (chamber % 2 == 0);
        result = (station < 3) ? isEven : !isEven;
      } else if (subsystem == TriggerPrimitive::kGEM) {
        //
        result = (chamber % 2 == 0);
      } else if (subsystem == TriggerPrimitive::kME0) {
        //
        result = (chamber % 2 == 0);
      } else if (subsystem == TriggerPrimitive::kDT) {
        //
        result = (chamber % 2 == 0);
      }
      return result;
    };

    auto isFront = [&](const auto& hit) {
      return isFront_detail(hit.Subsystem(), hit.Station(), hit.Ring(), hit.Chamber(), (hit.Subsystem() == TriggerPrimitive::kRPC ? hit.Subsector_RPC() : hit.Subsector()));
    };

    // --------------------------------------------------------------

    initialize();

    // // the L1Muons objects - plus side
    // edm::Handle<MuonBxCollection> l1musPosH;
    // iEvent.getByToken(muTokenPos, l1musPosH);  
    // const MuonBxCollection& l1musPos = (*l1musPosH.product());

    // // the L1Muons objects - minus side
    // edm::Handle<MuonBxCollection> l1musNegH;
    // iEvent.getByToken(muTokenNeg, l1musNegH);  
    // const MuonBxCollection& l1musNeg = (*l1musNegH.product());

    // the L1Muons objects - directly frtom EMTF
    edm::Handle<EMTFTrackCollection> l1musH;
    iEvent.getByToken(muToken, l1musH);  
    const EMTFTrackCollection& l1mus = (*l1musH.product());

    edm::Handle<EMTFHitCollection> l1muhitsH;
    iEvent.getByToken(mu_hitToken, l1muhitsH);  
    const EMTFHitCollection& l1muhits = (*l1muhitsH.product());


    edm::Handle<RegionalMuonCandBxCollection> l1musBarrelH;
    iEvent.getByToken(muBarrelToken, l1musBarrelH);  
    const RegionalMuonCandBxCollection& l1musBarrel = (*l1musBarrelH.product());

    edm::Handle<RegionalMuonCandBxCollection> l1musOvrlapH;
    iEvent.getByToken(muOvrlapToken, l1musOvrlapH);  
    const RegionalMuonCandBxCollection& l1musOvrlap = (*l1musOvrlapH.product());

    // the L1Tracks
    edm::Handle<L1TTTrackCollectionType> l1tksH;
    iEvent.getByToken(trackToken, l1tksH);
    const L1TTTrackCollectionType& l1tks = (*l1tksH.product());

    // the gen particles
    edm::Handle<GenParticleCollection> genpartH;
    iEvent.getByToken(genPartToken, genpartH);
    const GenParticleCollection& genparts = (*genpartH.product());

    // the mu+trk objects
    edm::Handle<L1TkMuonParticleCollection> tkmuH;
    iEvent.getByToken(tkMuToken, tkmuH);
    const L1TkMuonParticleCollection& tkmus = (*tkmuH.product());

    edm::Handle<L1TkMuonParticleCollection> tkmustubH;
    iEvent.getByToken(tkMuStubToken, tkmustubH);
    const L1TkMuonParticleCollection& tkmustubs = (*tkmustubH.product());

    // ------------------------------------------------------

    // for the  tau->3mu cross-linking
    std::vector<int> selected_muons;
    std::vector<int> selected_taus;

    for (auto genpartit = genparts.begin(); genpartit != genparts.end(); ++genpartit)
    {
        int apdgid = abs(genpartit->pdgId());
        // if (apdgid != 13 && (apdgid != 15 && save_tau_3mu_) )
        //     continue;
        if (apdgid != 13 && apdgid != 15)
            continue;

        // save the muons
        if (apdgid == 13)
        {

            if (prompt_mu_only_) // to be activated in the cfg. On only if interested in mu gun on Zmumu, off for muons in bjets
            {
                // keep only hard scatter stuff (processing Z->mumu)
                if (!genpartit->statusFlags().isPrompt())      continue;
                // if (!genpartit->statusFlags().isHardProcess()) continue; // do not apply this (missing muons in Z->mumu)
                if (!genpartit->statusFlags().isLastCopy())    continue;
            }

            if (mu_from_tau_only_) // to be activated in the cfg. On only if interested in mu from tau->3mu samples
            {
                if (abs(genpartit->mother(0)->pdgId()) != 15)      continue;
            }

            ++n_gen_mu_;
            gen_mu_pt_.push_back(genpartit->pt());
            gen_mu_eta_.push_back(genpartit->eta());
            gen_mu_phi_.push_back(genpartit->phi());
            gen_mu_e_.push_back(genpartit->energy());
            gen_mu_charge_.push_back(genpartit->charge());
            // cout << genpartit->status() << endl;
            // the single mu sample has 2 muons, back-to-back

            selected_muons.push_back(std::distance(genparts.begin(), genpartit));
        }

        // save the taus
        if (apdgid == 15 && save_tau_3mu_)
        {
            // only tau -> 3mu
            if (genpartit->numberOfDaughters() != 3)
                continue;

            int apdgiddau1 = abs(genpartit->daughter(0)->pdgId());
            int apdgiddau2 = abs(genpartit->daughter(1)->pdgId());
            int apdgiddau3 = abs(genpartit->daughter(2)->pdgId());

            bool istau3mu = (apdgiddau1 == 13 && apdgiddau2 == 13 && apdgiddau3 == 13);
            if (istau3mu)
            {
                ++n_gen_tau_;
                gen_tau_pt_.push_back(genpartit->pt());
                gen_tau_eta_.push_back(genpartit->eta());
                gen_tau_phi_.push_back(genpartit->phi());
                gen_tau_e_.push_back(genpartit->energy());
                gen_tau_charge_.push_back(genpartit->charge());

                selected_taus.push_back(std::distance(genparts.begin(), genpartit));
            }
        }
    }

    // now cross-link mu candidates and taus
    if (save_tau_3mu_)
    {
        for (uint igenmu = 0; igenmu < selected_muons.size(); ++igenmu)
        {
            int idxgenmu = selected_muons.at(igenmu);
            auto muonit = genparts.begin() + idxgenmu;
            auto muonmotherit = muonit->mother(0);

            int itau_match = -1;
            for (uint igentau = 0; igentau < selected_taus.size(); ++igentau)
            {
                int idxgentau = selected_taus.at(igentau);
                auto tauit = genparts.begin() + idxgentau;

                // if the mu mother is the tau, save it index
                if (&(*muonmotherit) == &(*tauit))
                {
                    itau_match = igentau;
                    break;
                }
            }
            // store the idx - will point to the position in the tau vector
            gen_mu_gentauidx_.push_back(itau_match);            
        }
    }

    // // some debug!
    // cout << "------ TAUS ------ " << endl;
    // for (uint igentau = 0; igentau < gen_tau_pt_.size(); ++igentau)
    // {
    //     cout << igentau
    //          << ") pt = " << gen_tau_pt_.at(igentau)
    //          << " eta = " << gen_tau_eta_.at(igentau)
    //          << " phi = " << gen_tau_phi_.at(igentau)
    //          << endl;
    // }
    // cout << "------ MUONS ------ " << endl;
    // for (uint igenmu = 0; igenmu < gen_mu_pt_.size(); ++igenmu)
    // {
    //     cout << igenmu
    //          << ") pt = " << gen_mu_pt_.at(igenmu)
    //          << " eta = " << gen_mu_eta_.at(igenmu)
    //          << " phi = " << gen_mu_phi_.at(igenmu)
    //          << " tau_idx = " << gen_mu_gentauidx_.at(igenmu)
    //          << endl;
    // }


    // n_L1TT_trk_ = l1tks.size();
    for (auto l1trkit = l1tks.begin(); l1trkit != l1tks.end(); ++l1trkit)
    {
        ++n_L1TT_trk_;
        if (save_all_trks_) // keep the branch structure but do not fill vectors
        {
            L1TT_trk_pt_ .push_back(l1trkit->getMomentum(nTrkPars).perp());
            L1TT_trk_eta_.push_back(l1trkit->getMomentum(nTrkPars).eta());
            L1TT_trk_phi_.push_back(l1trkit->getMomentum(nTrkPars).phi());
            int l1tttq = (l1trkit->getRInv(nTrkPars) > 0 ? 1 : -1);
            L1TT_trk_charge_.push_back(l1tttq);
            L1TT_trk_p_     .push_back(l1trkit->getMomentum(nTrkPars).mag());
            L1TT_trk_z_     .push_back(l1trkit->getPOCA().z());
            L1TT_trk_chi2_  .push_back(l1trkit->getChi2(nTrkPars));
            L1TT_trk_nstubs_.push_back(l1trkit->getStubRefs().size());
        }
        /*
        // check to access components info
        auto stubRefs = l1trkit->getStubRefs();
        cout << "N stub refs " << stubRefs.size() << endl;
        for (unsigned int isr = 0; isr < stubRefs.size(); ++isr)
        {
            auto& stub = *(stubRefs.at(isr));
            cout << " - " << isr << " " << stub.getTriggerDisplacement() << endl;
        }
        */

    }

    // for (auto l1muit = l1musPos.begin(0); l1muit != l1musPos.end(0); ++l1muit)
    // {
    //     ++n_EMTF_mu_;
    // }

    // for (auto l1muit = l1musNeg.begin(0); l1muit != l1musNeg.end(0); ++l1muit)
    // {
    //     ++n_EMTF_mu_;
    // }

    for (auto l1muit = l1mus.begin(); l1muit != l1mus.end(); ++l1muit)
    {
        const auto& hit_refs = get_hit_refs(*l1muit, l1muhits);
        assert(hit_refs.size() == 4); // sanity check

        if (l1muit->BX() != 0)
            continue;
        ++n_EMTF_mu_;
        EMTF_mu_pt_.push_back(l1muit->Pt());
        EMTF_mu_pt_xml_.push_back(l1muit->Pt_XML());
        EMTF_mu_eta_.push_back(l1muit->Eta());
        EMTF_mu_theta_.push_back(l1muit->Theta());
        EMTF_mu_phi_.push_back(l1muit->Phi_glob());
        EMTF_mu_charge_.push_back(l1muit->Charge());
        EMTF_mu_mode_.push_back(l1muit->Mode());
        EMTF_mu_endcap_.push_back(l1muit->Endcap());
        EMTF_mu_sector_.push_back(l1muit->Sector());
        EMTF_mu_bx_.push_back(l1muit->BX());
        // EMTF_mu_e_.push_back(l1muit->energy());
        EMTF_mu_hitref1_.push_back(hit_refs.at(0));
        EMTF_mu_hitref2_.push_back(hit_refs.at(1));
        EMTF_mu_hitref3_.push_back(hit_refs.at(2));
        EMTF_mu_hitref4_.push_back(hit_refs.at(3));

        // if (l1mus.size() > 4)
        // cout << "Number of hits in this track " << l1muit->Hits().size() << "  -- trk qual " << l1muit->Mode() << endl;
    }

    // barrel muons
    // NB: convertions taken from https://github.com/cms-l1t-offline/cmssw/blob/l1t-phase2-v2.22.1-CMSSW_10_6_1_patch2/L1Trigger/L1TTrackMatch/plugins/L1TkMuonProducer.cc
    for (auto l1mubarrit = l1musBarrel.begin(0); l1mubarrit != l1musBarrel.end(0); ++l1mubarrit)
    {
        ++n_barrel_mu_;
        
        barrel_mu_pt_.push_back(l1mubarrit->hwPt() * 0.5);
        barrel_mu_eta_.push_back(l1mubarrit->hwEta() * 0.010875);
        float this_l1mu_phi = MicroGMTConfiguration::calcGlobalPhi( l1mubarrit->hwPhi(), l1mubarrit->trackFinderType(), l1mubarrit->processor() )*2*M_PI/576.;
        barrel_mu_phi_.push_back(this_l1mu_phi);
        int hwsign = l1mubarrit->hwSign();
        int charge = (hwsign == 0 ? 1 : -1); // charge sign bit (charge = (-1)^(sign))
        barrel_mu_charge_.push_back(charge);
    }

    // overlap muons
    for (auto l1muovrlit = l1musOvrlap.begin(0); l1muovrlit != l1musOvrlap.end(0); ++l1muovrlit)
    {
        ++n_ovrlap_mu_;
        
        ovrlap_mu_pt_.push_back(l1muovrlit->hwPt() * 0.5);
        ovrlap_mu_eta_.push_back(l1muovrlit->hwEta() * 0.010875);
        float this_l1mu_phi = MicroGMTConfiguration::calcGlobalPhi( l1muovrlit->hwPhi(), l1muovrlit->trackFinderType(), l1muovrlit->processor() )*2*M_PI/576.;
        ovrlap_mu_phi_.push_back(this_l1mu_phi);
        int hwsign = l1muovrlit->hwSign();
        int charge =  (hwsign == 0 ? 1 : -1); // charge sign bit (charge = (-1)^(sign))
        ovrlap_mu_charge_.push_back(charge);
    }

    /// mu + trks
    // cout << "--- this event has " << tkmus.size() << " muons" << endl;
    for (const auto& tkmu : tkmus)
    {
        ++n_L1_TkMu_;
        L1_TkMu_pt_  . push_back(tkmu.pt());
        L1_TkMu_eta_ . push_back(tkmu.eta());
        L1_TkMu_phi_ . push_back(tkmu.phi());

        // get the associated track and get properties
        // const edm::Ptr< L1TTTrackType >& getTrkPtr() const
        auto matchedTrk =  tkmu.getTrkPtr();
        int l1tttq = (matchedTrk->getRInv(nTrkPars) > 0 ? 1 : -1);
        L1_TkMu_charge_  . push_back(l1tttq);
        L1_TkMu_p_       . push_back(matchedTrk->getMomentum(nTrkPars).mag());
        L1_TkMu_z_       . push_back(matchedTrk->getPOCA().z());
        L1_TkMu_chi2_    . push_back(matchedTrk->getChi2(nTrkPars));
        L1_TkMu_nstubs_  . push_back(matchedTrk->getStubRefs().size());

        L1_TkMu_mudetID_ . push_back(tkmu.muonDetector());

        // this is true, verified
        // cout << tkmu.pt() << " " << matchedTrk->getMomentum(nTrkPars).perp() << endl;
    }

    /// trk + stubs
    for (const auto& tkmustub : tkmustubs)
    {
        ++n_L1_TkMuStub_;
        L1_TkMuStub_pt_  . push_back(tkmustub.pt());
        L1_TkMuStub_eta_ . push_back(tkmustub.eta());
        L1_TkMuStub_phi_ . push_back(tkmustub.phi());

        // get the associated track and get properties
        // const edm::Ptr< L1TTTrackType >& getTrkPtr() const
        auto matchedTrk =  tkmustub.getTrkPtr();
        int l1tttq = (matchedTrk->getRInv(nTrkPars) > 0 ? 1 : -1);
        L1_TkMuStub_charge_  . push_back(l1tttq);
        L1_TkMuStub_p_       . push_back(matchedTrk->getMomentum(nTrkPars).mag());
        L1_TkMuStub_z_       . push_back(matchedTrk->getPOCA().z());
        L1_TkMuStub_chi2_    . push_back(matchedTrk->getChi2(nTrkPars));
        L1_TkMuStub_nstubs_  . push_back(matchedTrk->getStubRefs().size());

        // this is true, verified
        // cout << tkmustub.pt() << " " << matchedTrk->getMomentum(nTrkPars).perp() << endl;
    }

    /// hits
    for (const auto& hit : l1muhits)
    {
        ++n_mu_hit_;
        mu_hit_endcap_     . push_back(hit.Endcap());
        mu_hit_station_    . push_back(hit.Station());
        mu_hit_ring_       . push_back(hit.Ring());
        mu_hit_sector_     . push_back(hit.PC_sector());
        mu_hit_subsector_  . push_back(hit.Subsector());
        mu_hit_chamber_    . push_back(hit.Chamber());
        mu_hit_cscid_      . push_back(hit.CSC_ID());
        mu_hit_bx_         . push_back(hit.BX());
        mu_hit_type_       . push_back(hit.Subsystem());
        mu_hit_neighbor_   . push_back(hit.Neighbor());
        //
        mu_hit_strip_      . push_back(hit.Strip());
        mu_hit_wire_       . push_back(hit.Wire());
        mu_hit_roll_       . push_back(hit.Roll());
        mu_hit_quality_    . push_back(hit.Quality());
        mu_hit_pattern_    . push_back(get_pattern(hit));  // modified
        mu_hit_bend_       . push_back(hit.Bend());
        mu_hit_time_       . push_back(get_time(hit));     // modified
        mu_hit_fr_         . push_back(isFront(hit));
        mu_hit_emtf_phi_   . push_back(hit.Phi_fp());
        mu_hit_emtf_theta_ . push_back(hit.Theta_fp());
        //
        mu_hit_sim_phi_    . push_back(hit.Phi_sim());
        mu_hit_sim_theta_  . push_back(hit.Theta_sim());
        mu_hit_sim_eta_    . push_back(hit.Eta_sim());
        mu_hit_sim_r_      . push_back(hit.Rho_sim());
        mu_hit_sim_z_      . push_back(hit.Z_sim());
    }

    tree_->Fill();
}

void Ntuplizer::endJob()
{}

void Ntuplizer::endRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{}


#include <FWCore/Framework/interface/MakerMacros.h>
DEFINE_FWK_MODULE(Ntuplizer);

#endif // NTUPLIZER_H
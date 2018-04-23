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

// #include "DataFormats/L1TrackTrigger/interface/L1TkMuonParticle.h"
// #include "DataFormats/L1TrackTrigger/interface/L1TkMuonParticleFwd.h"


#include "TTree.h"

using namespace edm;
using namespace l1t;
using namespace reco;

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

        const static int nTrkPars = 4; // number of parameters in the trk fit -- eventually to be made configurable

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

        // hits of a EMTF track
        // std::vector<int>   EMTF_mu_h1_type_;
        // std::vector<int>   EMTF_mu_h2_type_;
        // std::vector<int>   EMTF_mu_h3_type_;
        // std::vector<int>   EMTF_mu_h4_type_;

        unsigned int n_L1TT_trk_;
        std::vector<float> L1TT_trk_pt_;
        std::vector<float> L1TT_trk_eta_;
        std::vector<float> L1TT_trk_phi_;
        // std::vector<float> L1TT_trk_e_;
        // std::vector<int> L1TT_trk_charge_;

        unsigned int n_gen_mu_;
        std::vector<float> gen_mu_pt_;
        std::vector<float> gen_mu_eta_;
        std::vector<float> gen_mu_phi_;
        std::vector<float> gen_mu_e_;
        std::vector<int>   gen_mu_charge_;

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
        std::vector<float  >  mu_hit_sim_phi_;
        std::vector<float  >  mu_hit_sim_theta_;
        std::vector<float  >  mu_hit_sim_eta_;
        // std::vector<float  >  mu_hit_sim_r_; // seems not there in the CMSSW emulator data format
        // std::vector<float  >  mu_hit_sim_z_; // seems not there in the CMSSW emulator data format


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

    n_L1TT_trk_ = 0;
    L1TT_trk_pt_.clear();
    L1TT_trk_eta_.clear();
    L1TT_trk_phi_.clear();
    // L1TT_trk_charge_.clear();

    n_gen_mu_   = 0;
    gen_mu_pt_.clear();
    gen_mu_eta_.clear();
    gen_mu_phi_.clear();
    gen_mu_e_.clear();
    gen_mu_charge_.clear();

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
    mu_hit_sim_phi_.clear();
    mu_hit_sim_theta_.clear();
    mu_hit_sim_eta_.clear();
    // mu_hit_sim_r_.clear();
    // mu_hit_sim_z_.clear();

}

Ntuplizer::Ntuplizer(const edm::ParameterSet& iConfig):
    // muTokenPos(consumes< MuonBxCollection >           (iConfig.getParameter<edm::InputTag>("L1MuonPosInputTag"))),
    // muTokenNeg(consumes< MuonBxCollection >           (iConfig.getParameter<edm::InputTag>("L1MuonNegInputTag"))),
    muToken(consumes< EMTFTrackCollection >           (iConfig.getParameter<edm::InputTag>("L1MuonEMTFInputTag"))),
    mu_hitToken(consumes< EMTFHitCollection >         (iConfig.getParameter<edm::InputTag>("L1EMTFHitInputTag"))),
    trackToken(consumes< L1TTTrackCollectionType >    (iConfig.getParameter<edm::InputTag>("L1TrackInputTag"))),
    genPartToken(consumes< GenParticleCollection >    (iConfig.getParameter<edm::InputTag>("GenParticleInputTag")))
{
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

    // tree_->Branch("EMTF_mu_e", &EMTF_mu_e_);

    tree_->Branch("n_L1TT_trk", &n_L1TT_trk_);
    tree_->Branch("L1TT_trk_pt", &L1TT_trk_pt_);
    tree_->Branch("L1TT_trk_eta", &L1TT_trk_eta_);
    tree_->Branch("L1TT_trk_phi", &L1TT_trk_phi_);
    // tree_->Branch("L1TT_trk_e", &L1TT_trk_e_);
    // tree_->Branch("L1TT_trk_charge", &L1TT_trk_charge_);

    tree_->Branch("n_gen_mu", &n_gen_mu_);
    tree_->Branch("gen_mu_pt", &gen_mu_pt_);
    tree_->Branch("gen_mu_eta", &gen_mu_eta_);
    tree_->Branch("gen_mu_phi", &gen_mu_phi_);
    tree_->Branch("gen_mu_e", &gen_mu_e_);
    tree_->Branch("gen_mu_charge", &gen_mu_charge_);

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
    tree_->Branch("mu_hit_sim_phi", &mu_hit_sim_phi_);
    tree_->Branch("mu_hit_sim_theta", &mu_hit_sim_theta_);
    tree_->Branch("mu_hit_sim_eta", &mu_hit_sim_eta_);

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

    // the L1Tracks
    edm::Handle<L1TTTrackCollectionType> l1tksH;
    iEvent.getByToken(trackToken, l1tksH);
    const L1TTTrackCollectionType& l1tks = (*l1tksH.product());

    // the gen particles
    edm::Handle<GenParticleCollection> genpartH;
    iEvent.getByToken(genPartToken, genpartH);
    const GenParticleCollection& genparts = (*genpartH.product());

    // ------------------------------------------------------

    for (auto genpartit = genparts.begin(); genpartit != genparts.end(); ++genpartit)
    {
        if (abs(genpartit->pdgId()) != 13)
            continue;
        ++n_gen_mu_;
        gen_mu_pt_.push_back(genpartit->pt());
        gen_mu_eta_.push_back(genpartit->eta());
        gen_mu_phi_.push_back(genpartit->phi());
        gen_mu_e_.push_back(genpartit->energy());
        gen_mu_charge_.push_back(genpartit->charge());
        // cout << genpartit->status() << endl;
        // the single mu sample has 2 muons, back-to-back

    }

    // n_L1TT_trk_ = l1tks.size();
    for (auto l1trkit = l1tks.begin(); l1trkit != l1tks.end(); ++l1trkit)
    {
        ++n_L1TT_trk_;
        L1TT_trk_pt_.push_back(l1trkit->getMomentum(nTrkPars).perp());
        L1TT_trk_eta_.push_back(l1trkit->getMomentum(nTrkPars).eta());
        L1TT_trk_phi_.push_back(l1trkit->getMomentum(nTrkPars).phi());
        // L1TT_trk_charge_.push_back(l1trkit->getMomentum(nTrkPars).charge());
        // L1TT_trk_e_.push_back(l1trkit->energy());
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
        mu_hit_sim_phi_    . push_back(hit.Phi_sim());
        mu_hit_sim_theta_  . push_back(hit.Theta_sim());
        mu_hit_sim_eta_    . push_back(hit.Eta_sim());
        // mu_hit_sim_r_      . push_back(hit.Rho_sim());
        // mu_hit_sim_z_      . push_back(hit.Z_sim());
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
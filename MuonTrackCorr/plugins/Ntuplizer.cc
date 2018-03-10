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
        // std::vector<float> EMTF_mu_e_;

        unsigned int n_L1TT_trk_;
        std::vector<float> L1TT_trk_pt_;
        std::vector<float> L1TT_trk_eta_;
        std::vector<float> L1TT_trk_phi_;
        // std::vector<float> L1TT_trk_e_;

        unsigned int n_gen_mu_;
        std::vector<float> gen_mu_pt_;
        std::vector<float> gen_mu_eta_;
        std::vector<float> gen_mu_phi_;
        std::vector<float> gen_mu_e_;

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

    n_L1TT_trk_ = 0;
    L1TT_trk_pt_.clear();
    L1TT_trk_eta_.clear();
    L1TT_trk_phi_.clear();

    n_gen_mu_   = 0;
    gen_mu_pt_.clear();
    gen_mu_eta_.clear();
    gen_mu_phi_.clear();
    gen_mu_e_.clear();


}

Ntuplizer::Ntuplizer(const edm::ParameterSet& iConfig):
    // muTokenPos(consumes< MuonBxCollection >           (iConfig.getParameter<edm::InputTag>("L1MuonPosInputTag"))),
    // muTokenNeg(consumes< MuonBxCollection >           (iConfig.getParameter<edm::InputTag>("L1MuonNegInputTag"))),
    muToken(consumes< EMTFTrackCollection >           (iConfig.getParameter<edm::InputTag>("L1MuonEMTFInputTag"))),
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

    // tree_->Branch("EMTF_mu_e", &EMTF_mu_e_);

    tree_->Branch("n_L1TT_trk", &n_L1TT_trk_);
    tree_->Branch("L1TT_trk_pt", &L1TT_trk_pt_);
    tree_->Branch("L1TT_trk_eta", &L1TT_trk_eta_);
    tree_->Branch("L1TT_trk_phi", &L1TT_trk_phi_);
    // tree_->Branch("L1TT_trk_e", &L1TT_trk_e_);

    tree_->Branch("n_gen_mu", &n_gen_mu_);
    tree_->Branch("gen_mu_pt", &gen_mu_pt_);
    tree_->Branch("gen_mu_eta", &gen_mu_eta_);
    tree_->Branch("gen_mu_phi", &gen_mu_phi_);
    tree_->Branch("gen_mu_e", &gen_mu_e_);
}

void Ntuplizer::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{}

void Ntuplizer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
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
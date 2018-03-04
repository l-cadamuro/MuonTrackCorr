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
// #include "DataFormats/L1TrackTrigger/interface/L1TkMuonParticle.h"
// #include "DataFormats/L1TrackTrigger/interface/L1TkMuonParticleFwd.h"

#include "TTree.h"

using namespace edm;
using namespace l1t;

class Ntuplizer : public edm::EDAnalyzer {
    public:

        typedef TTTrack< Ref_Phase2TrackerDigi_ >  L1TTTrackType;
        typedef std::vector< L1TTTrackType >       L1TTTrackCollectionType;

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

        const edm::EDGetTokenT< MuonBxCollection > muTokenPos;
        const edm::EDGetTokenT< MuonBxCollection > muTokenNeg;
        const edm::EDGetTokenT< std::vector< TTTrack< Ref_Phase2TrackerDigi_ > > > trackToken;

        //-----output---
        TTree *tree_;

        unsigned int n_EMTF_mu_;
        unsigned int n_L1TT_trk_;
};

void Ntuplizer::initialize()
{
    n_EMTF_mu_  = 0;
    n_L1TT_trk_ = 0;
}

Ntuplizer::Ntuplizer(const edm::ParameterSet& iConfig):
    muTokenPos(consumes< MuonBxCollection >           (iConfig.getParameter<edm::InputTag>("L1MuonPosInputTag"))),
    muTokenNeg(consumes< MuonBxCollection >           (iConfig.getParameter<edm::InputTag>("L1MuonNegInputTag"))),
    trackToken(consumes< L1TTTrackCollectionType >    (iConfig.getParameter<edm::InputTag>("L1TrackInputTag")))
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
    tree_->Branch("n_L1TT_trk", &n_L1TT_trk_);

}

void Ntuplizer::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{}

void Ntuplizer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    initialize();

    // the L1Muons objects - plus side
    edm::Handle<MuonBxCollection> l1musPosH;
    iEvent.getByToken(muTokenPos, l1musPosH);  
    const MuonBxCollection& l1musPos = (*l1musPosH.product());

    // the L1Muons objects - minus side
    edm::Handle<MuonBxCollection> l1musNegH;
    iEvent.getByToken(muTokenNeg, l1musNegH);  
    const MuonBxCollection& l1musNeg = (*l1musNegH.product());

    // the L1Tracks
    edm::Handle<L1TTTrackCollectionType> l1tksH;
    iEvent.getByToken(trackToken, l1tksH);
    const L1TTTrackCollectionType& l1tks = (*l1tksH.product());

    n_L1TT_trk_ = l1tks.size();

    for (auto l1muit = l1musPos.begin(0); l1muit != l1musPos.end(0); ++l1muit)
    {
        ++n_EMTF_mu_;
    }

    for (auto l1muit = l1musNeg.begin(0); l1muit != l1musNeg.end(0); ++l1muit)
    {
        ++n_EMTF_mu_;
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
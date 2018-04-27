#ifndef PRINTMUONS_H
#define PRINTMUONS_H

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/L1Trigger/interface/Muon.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/L1TMuon/interface/EMTFTrack.h"

#include "DataFormats/L1TMuon/interface/RegionalMuonCand.h"
#include "DataFormats/L1TMuon/interface/RegionalMuonCandFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/L1TrackTrigger/interface/L1TkMuonParticle.h"
#include "DataFormats/L1TrackTrigger/interface/L1TkMuonParticleFwd.h"

// system include files
#include <memory>
#include <string>

using namespace edm;
using namespace l1t;
using namespace reco;


class PrintMuons : public edm::EDAnalyzer {
    public:
        explicit PrintMuons(const edm::ParameterSet&);
        virtual ~PrintMuons(){};

    private:
        //----edm control---
        virtual void beginJob(){};
        virtual void beginRun(edm::Run const&, edm::EventSetup const&){};
        virtual void analyze(const edm::Event&, const edm::EventSetup&);
        virtual void endJob(){};
        virtual void endRun(edm::Run const&, edm::EventSetup const&){};

        const edm::EDGetTokenT< EMTFTrackCollection >           emtfTrkToken;
        const edm::EDGetTokenT< RegionalMuonCandBxCollection >  emtfRegToken;

        int calcGlobalPhi(int locPhi, int proc);
};

PrintMuons::PrintMuons(const edm::ParameterSet& iConfig):
    emtfTrkToken (consumes< EMTFTrackCollection >           (iConfig.getParameter<edm::InputTag>("emtfTrkToken"))),
    emtfRegToken (consumes< RegionalMuonCandBxCollection >  (iConfig.getParameter<edm::InputTag>("emtfRegToken")))
{}

// from https://github.com/cms-sw/cmssw/blob/f35b32c499059d9ce31e0060d4543bf8a12e9efc/L1Trigger/L1TMuon/src/MicroGMTConfiguration.cc
// simplified for EMTF only
int PrintMuons::calcGlobalPhi(int locPhi, int proc) {
  int globPhi = 0;
  // if (t == bmtf) {
  //     // each BMTF processor corresponds to a 30 degree wedge = 48 in int-scale
  //     globPhi = (proc) * 48 + locPhi;
  //     // first processor starts at CMS phi = -15 degrees...
  //     globPhi += 576-24;
  //     // handle wrap-around (since we add the 576-24, the value will never be negative!)
  //     globPhi = globPhi%576;
  // } else {
      // all others correspond to 60 degree sectors = 96 in int-scale
      globPhi = (proc) * 96 + locPhi;
      // first processor starts at CMS phi = 15 degrees (24 in int)... Handle wrap-around with %. Add 576 to make sure the number is positive
      globPhi = (globPhi + 600) % 576;
  // }
  return globPhi;
}

void PrintMuons::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    edm::Handle<EMTFTrackCollection> emtfTrkH;
    iEvent.getByToken(emtfTrkToken, emtfTrkH);  
    const EMTFTrackCollection& emtfTrks = (*emtfTrkH.product());

    edm::Handle<RegionalMuonCandBxCollection> emtfRegH;
    iEvent.getByToken(emtfRegToken, emtfRegH);  
    const RegionalMuonCandBxCollection& emtfRegs = (*emtfRegH.product());

    cout << " ==== EMTF TRACKS === " << emtfTrks.size() << endl;
    for (auto& emtfTrk : emtfTrks)
    {
        cout << " - pt: " << emtfTrk.Pt() << " - eta: " << emtfTrk.Eta() << " - phi : " << emtfTrk.Phi_glob() << endl;
    }

    cout << " ==== EMTF REGIONAL === " << emtfRegs.size() << endl;
    for (auto& emtfReg : emtfRegs)
    {
        // taken from L1TkMuProducer... assuming the conversion below is correct
        // float l1mu_pt  = emtfReg.hwPt()*0.5;
        // float l1mu_eta = emtfReg.hwEta()*0.010875;
        // float l1mu_phi = emtfReg.hwPhi()*2*M_PI/576.;

        // from https://github.com/cms-sw/cmssw/blob/f35b32c499059d9ce31e0060d4543bf8a12e9efc/L1Trigger/L1TMuon/plugins/L1TMuonProducer.cc
        // (mu->hwPt()-1)*0.5, mu->hwEta()*0.010875, mu->hwGlobalPhi()*0.010908

        float l1mu_pt  = (emtfReg.hwPt()-1)*0.5;
        float l1mu_eta = emtfReg.hwEta()*0.010875;
        int gphi = calcGlobalPhi(emtfReg.hwPhi(), emtfReg.processor());
        float l1mu_phi = gphi*0.010908;

        cout << " - pt: " << l1mu_pt << " - eta: " << l1mu_eta << " - phi : " << l1mu_phi << endl;
    }

}

#include <FWCore/Framework/interface/MakerMacros.h>
DEFINE_FWK_MODULE(PrintMuons);

#endif // PRINTMUONS_H
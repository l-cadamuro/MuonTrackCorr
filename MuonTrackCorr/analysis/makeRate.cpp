#include "RateCalculator.h"
#include "MuTkTree.h"
#include "Correlator.h"
#include "Correlator_L1TTgroup_impl.h"
#include "MantraCorr.h"
#include "GenericDataFormat.h"
#include "TH1.h"
#include "TH2.h"
#include <string>
#include <iostream>
#include <vector>

using namespace std;

#define DEBUG false
// #define fiducial_eta_min 1.2
#define fiducial_eta_min 1.24 // Jia Fu synch'd
#define fiducial_eta_max 2.4

// c++ -lm -o makeRate makeRate.cpp `root-config --glibs --cflags`

std::vector<double> prepare_corr_bounds(string fname, string hname)
{
    // find the boundaries of the match windoww
    TFile* fIn = TFile::Open(fname.c_str());
    TH2* h_test = (TH2*) fIn->Get(hname.c_str());
    if (h_test == nullptr)
    {
        // cout << "Can't find histo to derive bounds" << endl;
        throw std::runtime_error("Can't find histo to derive bounds");
    }

    int nbds = h_test->GetNbinsY()+1;
    cout << "... using " << nbds-1 << " eta bins" << endl;
    vector<double> bounds (nbds);
    for (int ib = 0; ib < nbds; ++ib)
    {
        bounds.at(ib) = h_test->GetYaxis()->GetBinLowEdge(ib+1);
        cout << "Low edge " << ib << " is " << bounds.at(ib) << endl;
    }
    fIn->Close();
    return bounds;
}

int appendFromFileList (TChain* chain, string filename)
{
    //cout << "=== inizio parser ===" << endl;
    std::ifstream infile(filename.c_str());
    std::string line;
    int nfiles = 0;
    while (std::getline(infile, line))
    {
        line = line.substr(0, line.find("#", 0)); // remove comments introduced by #
        while (line.find(" ") != std::string::npos) line = line.erase(line.find(" "), 1); // remove white spaces
        while (line.find("\n") != std::string::npos) line = line.erase(line.find("\n"), 1); // remove new line characters
        while (line.find("\r") != std::string::npos) line = line.erase(line.find("\r"), 1); // remove carriage return characters
        if (!line.empty()) // skip empty lines
        {
            chain->Add(line.c_str());
            ++nfiles;
        }
     }
    return nfiles;
}

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

// dump and convert tracks to the format needed for the correlator
std::vector<track_df> MuTkTree_to_trkvec(MuTkTree& mtkt)
{
    std::vector<track_df> result (*mtkt.n_L1TT_trk);
    for (uint itrk = 0; itrk < *mtkt.n_L1TT_trk; ++itrk)
    {

        result.at(itrk).pt      = mtkt.L1TT_trk_pt.At(itrk);
        result.at(itrk).eta     = mtkt.L1TT_trk_eta.At(itrk);
        result.at(itrk).theta   = to_mpio2_pio2(eta_to_theta(mtkt.L1TT_trk_eta.At(itrk)));
        result.at(itrk).phi     = mtkt.L1TT_trk_phi.At(itrk);
        result.at(itrk).nstubs  = mtkt.L1TT_trk_nstubs.At(itrk);
        result.at(itrk).chi2    = mtkt.L1TT_trk_chi2.At(itrk);
        result.at(itrk).charge  = mtkt.L1TT_trk_charge.At(itrk);
    }

    return result;
}

// dump and convert muons to the format needed for the correlator
std::vector<muon_df> MuTkTree_to_muvec(MuTkTree& mtkt, std::string system)
{

    if (system == "barrel")
    {
        std::vector<muon_df> result (*mtkt.n_barrel_mu);
        for (uint imu = 0; imu < *mtkt.n_barrel_mu; ++imu)
        {
            result.at(imu).pt     = mtkt.barrel_mu_pt.At(imu);
            result.at(imu).eta    = mtkt.barrel_mu_eta.At(imu);
            result.at(imu).theta  = to_mpio2_pio2(eta_to_theta(mtkt.barrel_mu_eta.At(imu)));
            result.at(imu).phi    = mtkt.barrel_mu_phi.At(imu);
            result.at(imu).charge = mtkt.barrel_mu_charge.At(imu);
        }
        return result;
    }

    else if (system == "overlap")
    {
        std::vector<muon_df> result (*mtkt.n_ovrlap_mu);
        for (uint imu = 0; imu < *mtkt.n_ovrlap_mu; ++imu)
        {
            result.at(imu).pt     = mtkt.ovrlap_mu_pt.At(imu);
            result.at(imu).eta    = mtkt.ovrlap_mu_eta.At(imu);
            result.at(imu).theta  = to_mpio2_pio2(eta_to_theta(mtkt.ovrlap_mu_eta.At(imu)));
            result.at(imu).phi    = mtkt.ovrlap_mu_phi.At(imu);
            result.at(imu).charge = mtkt.ovrlap_mu_charge.At(imu);
        }
        return result;
    }

    else if (system == "endcap")
    {
        std::vector<muon_df> result (*mtkt.n_EMTF_mu);
        for (uint imu = 0; imu < *mtkt.n_EMTF_mu; ++imu)
        {
            result.at(imu).pt     = mtkt.EMTF_mu_pt.At(imu);
            result.at(imu).eta    = mtkt.EMTF_mu_eta.At(imu);
            result.at(imu).theta  = to_mpio2_pio2(eta_to_theta(mtkt.EMTF_mu_eta.At(imu)));
            result.at(imu).phi    = deg_to_rad(mtkt.EMTF_mu_phi.At(imu));
            result.at(imu).charge = mtkt.EMTF_mu_charge.At(imu);
        }
        return result;
    }

    else
        throw std::runtime_error("MuTkTree_to_muvec : cannot understand system");
}



int main(int argc, char** argv)
{
    string filelist = "filelist/NuGun_200PU_8Giu_TkMu_moreinfotrk_allEvts.txt";
    // string outputname = "muon_trigger_rates.root";
    string outputname = "muon_trigger_rates_preselTracks.root";

    if (argc > 2)
    {
        filelist   = argv[1];    
        outputname = argv[2];
    }

    string mantraTrkArb = "MinDeltaPt";
    if (argc > 3)
    {
        mantraTrkArb = argv[3];
    }

    int quantile = 99;
    bool doRelax = true;
    float sftor  = 0.5;
    float sftor_initial = 0.0;

    // int maxEvts = 10000;
    int maxEvts = -1;

    /// -----------------------------------------------------------

    cout << "... running on filelist " << filelist << endl;
    cout << "... saving output to " << outputname << endl;
    cout << "... MAnTra track arbitration type " << mantraTrkArb << endl;

    TChain* ch = new TChain("Ntuplizer/MuonTrackTree");
    MuTkTree mtkt (ch);

    int appd = appendFromFileList (ch, filelist);
    cout << "... read out " << appd << " files" << endl;

    RateCalculator rc_EMTF("EMTF");
    RateCalculator rc_TPTkMu("TPTkMu");
    RateCalculator rc_TPTkMu_truemu("TPTkMu_truemu");
    RateCalculator rc_TPTkMu_fakemu("TPTkMu_fakemu");
    RateCalculator rc_MyTPTkMu("MyTPTkMu"); // my implementation
    RateCalculator rc_UpgTkMu("UpgTkMu");
    RateCalculator rc_TPTkMuStub("TPTkMuStub");
    RateCalculator rc_TPTkMuStub_truemu("TPTkMuStub_truemu");
    RateCalculator rc_TPTkMuStub_fakemu("TPTkMuStub_fakemu");
    //
    RateCalculator rc_Mantra_TkMu_barr("Mantra_TkMu_barr");
    RateCalculator rc_Mantra_TkMu_ovrl("Mantra_TkMu_ovrl");
    RateCalculator rc_Mantra_TkMu_endc("Mantra_TkMu_endc");


    rc_EMTF.setStyle(kBlue);
    rc_TPTkMu.setStyle(kRed);
    rc_TPTkMu_truemu.setStyle(kRed+2);
    rc_TPTkMu_fakemu.setStyle(kRed-9);
    rc_MyTPTkMu.setStyle(kOrange);
    rc_UpgTkMu.setStyle(kGreen+1);
    rc_TPTkMuStub.setStyle(kGreen);
    rc_TPTkMuStub_truemu.setStyle(kGreen+2);
    rc_TPTkMuStub_fakemu.setStyle(kGreen-9);

    TFile* fOut = new TFile (outputname.c_str(), "recreate");

    // -------------------------------------- upg correlator
    auto bounds = prepare_corr_bounds("correlator_data/matching_windows.root", "h_dphi_l");
    string fIn_theta_name = "EMPTY";
    string fIn_phi_name   = "EMPTY";
    if (quantile == 90)
    {
        fIn_theta_name = "correlator_data/matching_windows_theta_q90.root";
        fIn_phi_name = "correlator_data/matching_windows_phi_q90.root";
    }
    else if (quantile == 95)
    {
        fIn_theta_name = "correlator_data/matching_windows_theta.root";
        fIn_phi_name = "correlator_data/matching_windows_phi.root";
    }
    else if (quantile == 99)
    {
        fIn_theta_name = "correlator_data/matching_windows_theta_q99.root";
        fIn_phi_name = "correlator_data/matching_windows_phi_q99.root";
    }
    else
    {
        cout << "I don't have the files for the quantile " << quantile << endl;
        return 1;
    }


    TFile* fIn_theta = TFile::Open (fIn_theta_name.c_str());
    TFile* fIn_phi   = TFile::Open (fIn_phi_name.c_str());
    Correlator corr (bounds, fIn_theta, fIn_phi);
    corr.set_safety_factor(sftor);
    corr.set_sf_initialrelax(sftor_initial);
    corr.set_do_relax_factor(doRelax);
    fIn_theta->Close();
    fIn_phi->Close();

    // ---------------------------------------------
    
    Correlator_L1TTgroup_impl corrL1TT_impl;

    // ---------------------------------------------

    // create the correlators
    auto bounds_barrel = prepare_corr_bounds  ("matching_windows_barrel/matching_windows_boundaries.root", "h_dphi_l");
    TFile* fIn_barr_theta = TFile::Open       ("matching_windows_barrel/matching_windows_theta_q99.root");
    TFile* fIn_barr_phi   = TFile::Open       ("matching_windows_barrel/matching_windows_phi_q99.root");
    MantraCorr mantracorr_barrel (bounds_barrel, fIn_barr_theta, fIn_barr_phi, "mantrabarrel");
    mantracorr_barrel.set_safety_factor(0.5, 0.5);
    mantracorr_barrel.setArbitrationType(mantraTrkArb);
    // mantracorr_barrel.setArbitrationType("MinDeltaPt");
    // mantracorr_barrel.setArbitrationType("MaxPt");
    fIn_barr_theta->Close();
    fIn_barr_phi->Close();

    auto bounds_ovrlap = prepare_corr_bounds  ("matching_windows_overlap/matching_windows_boundaries.root", "h_dphi_l");
    TFile* fIn_ovrl_theta = TFile::Open       ("matching_windows_overlap/matching_windows_theta_q99.root");
    TFile* fIn_ovrl_phi   = TFile::Open       ("matching_windows_overlap/matching_windows_phi_q99.root");    
    MantraCorr mantracorr_ovrlap (bounds_ovrlap, fIn_ovrl_theta, fIn_ovrl_phi, "mantraovrlap");
    mantracorr_ovrlap.set_safety_factor(0.5, 0.5);
    mantracorr_ovrlap.setArbitrationType(mantraTrkArb);
    // mantracorr_ovrlap.setArbitrationType("MinDeltaPt");
    // mantracorr_ovrlap.setArbitrationType("MaxPt");
    fIn_ovrl_theta->Close();
    fIn_ovrl_phi->Close();

    auto bounds_endcap = prepare_corr_bounds  ("matching_windows_endcap/matching_windows_boundaries.root", "h_dphi_l");
    TFile* fIn_endc_theta = TFile::Open       ("matching_windows_endcap/matching_windows_theta_q99.root");
    TFile* fIn_endc_phi   = TFile::Open       ("matching_windows_endcap/matching_windows_phi_q99.root");
    MantraCorr mantracorr_endcap (bounds_endcap, fIn_endc_theta, fIn_endc_phi, "mantraendcap");
    mantracorr_endcap.set_safety_factor(0.5, 0.5);
    mantracorr_endcap.setArbitrationType(mantraTrkArb);
    // mantracorr_endcap.setArbitrationType("MinDeltaPt");
    // mantracorr_endcap.setArbitrationType("MaxPt");
    fIn_endc_theta->Close();
    fIn_endc_phi->Close();

    // ---------------------------------------------


    for (uint iEv = 0; true; ++iEv)
    {
        if (!mtkt.Next()) break;

        if (maxEvts > -1 && iEv > maxEvts)
            break;

        if (iEv % 10000 == 0 || DEBUG)
            cout << "... processing " << iEv << endl;

        // fill rates
        for (uint iemtf = 0; iemtf < *(mtkt.n_EMTF_mu); ++iemtf){
            float aeta = std::fabs(mtkt.EMTF_mu_eta.At(iemtf));
            if (aeta < fiducial_eta_min || aeta > fiducial_eta_max) // Jia Fu synch'd
                continue;
            rc_EMTF.feedPt(mtkt.EMTF_mu_pt.At(iemtf)); // Jia Fu synch'd
            // rc_EMTF.feedPt(mtkt.EMTF_mu_pt_xml.At(iemtf));
        }

        for (uint itkmu = 0; itkmu < *(mtkt.n_L1_TkMu); ++itkmu){
            float aeta = std::fabs(mtkt.L1_TkMu_eta.At(itkmu));
            if (aeta < fiducial_eta_min || aeta > fiducial_eta_max)
                continue;
            if (mtkt.L1_TkMu_mudetID.At(itkmu) != 3)
                continue; // just the ManTra endcap rate

            // cout << mtkt.L1_TkMu_eta.At(itkmu) << endl;
            rc_TPTkMu.feedPt(mtkt.L1_TkMu_pt.At(itkmu));
            int genmatchedTP = mtkt.L1_TkMu_gen_TP_ID.At(itkmu);
            if (abs(genmatchedTP) == 13)
                rc_TPTkMu_truemu.feedPt(mtkt.L1_TkMu_pt.At(itkmu));
            else
                rc_TPTkMu_fakemu.feedPt(mtkt.L1_TkMu_pt.At(itkmu));

        }

        for (uint itkmustub = 0; itkmustub < *(mtkt.n_L1_TkMuStub); ++itkmustub){
            float aeta = std::fabs(mtkt.L1_TkMuStub_eta.At(itkmustub));
            if (aeta < fiducial_eta_min || aeta > fiducial_eta_max)
                continue;
            // if (mtkt.L1_TkMu_mudetID.At(itkmustub) != 3)
            //     continue; // TkMuSTub only for EMTF hits

            // cout << mtkt.L1_TkMu_eta.At(itkmustub) << endl;
            rc_TPTkMuStub.feedPt(mtkt.L1_TkMuStub_pt.At(itkmustub));
            int genmatchedTP = mtkt.L1_TkMuStub_gen_TP_ID.At(itkmustub);
            if (abs(genmatchedTP) == 13)
                rc_TPTkMuStub_truemu.feedPt(mtkt.L1_TkMuStub_pt.At(itkmustub));
            else
                rc_TPTkMuStub_fakemu.feedPt(mtkt.L1_TkMuStub_pt.At(itkmustub));
        }


        // upg correlator
        auto corr_mu_idxs = corr.find_match(mtkt); // for each trk, the emtfmu that matches
        if (corr_mu_idxs.size() != *(mtkt.n_L1TT_trk))
            cout << " ? upg correlator has != nentries than trk ?" << endl;
        for (unsigned int itrk = 0; itrk < corr_mu_idxs.size(); ++itrk){
            if (corr_mu_idxs.at(itrk) >= 0)
                rc_UpgTkMu.feedPt(mtkt.L1TT_trk_pt.At(itrk));
        }


        // correlator idsx
        auto mycorr_mu_idxs = corrL1TT_impl.find_match(mtkt); // for each trk, the emtfmu that matches
        if (mycorr_mu_idxs.size() != *(mtkt.n_L1TT_trk))
            cout << " ? my impl upg correlator has != nentries than trk ?" << endl;
        for (unsigned int itrk = 0; itrk < mycorr_mu_idxs.size(); ++itrk){
            if (mycorr_mu_idxs.at(itrk) >= 0)
                rc_MyTPTkMu.feedPt(mtkt.L1TT_trk_pt.At(itrk));
        }

        // ManTra correlators - for the 3 regions of the detector
        auto barrel_muons = MuTkTree_to_muvec(mtkt, "barrel");
        auto ovrlap_muons = MuTkTree_to_muvec(mtkt, "overlap");
        auto endcap_muons = MuTkTree_to_muvec(mtkt, "endcap");
        auto tracks       = MuTkTree_to_trkvec(mtkt);

        auto barrel_tkmus_idx = mantracorr_barrel.find_match(tracks, barrel_muons);
        auto ovrlap_tkmus_idx = mantracorr_ovrlap.find_match(tracks, ovrlap_muons);
        auto endcap_tkmus_idx = mantracorr_endcap.find_match(tracks, endcap_muons);

        // barrel
        for (uint imu = 0; imu < barrel_tkmus_idx.size(); ++imu)
        {
            int idx = barrel_tkmus_idx.at(imu);
            if (idx < 0) continue;
            track_df trk = tracks.at(idx);
            if (std::abs(trk.eta) > 0.8) continue;            
            rc_Mantra_TkMu_barr.feedPt(trk.pt);
        }

        // overlap
        for (uint imu = 0; imu < ovrlap_tkmus_idx.size(); ++imu)
        {
            int idx = ovrlap_tkmus_idx.at(imu);
            if (idx < 0) continue;
            track_df trk = tracks.at(idx);
            if (std::abs(trk.eta) < 0.8 || std::abs(trk.eta) > 1.2) continue;
            rc_Mantra_TkMu_ovrl.feedPt(trk.pt);
        }

        for (uint imu = 0; imu < endcap_tkmus_idx.size(); ++imu)
        {
            int idx = endcap_tkmus_idx.at(imu);
            if (idx < 0) continue;
            track_df trk = tracks.at(idx);
            if (std::abs(trk.eta) < 1.2) continue;
            rc_Mantra_TkMu_endc.feedPt(trk.pt);
        }


        // make the rate plots here, once all pt filled
        rc_EMTF.process();
        rc_TPTkMu.process();
        rc_TPTkMu_truemu.process();
        rc_TPTkMu_fakemu.process();
        rc_MyTPTkMu.process();
        rc_UpgTkMu.process();
        rc_TPTkMuStub.process();
        rc_TPTkMuStub_truemu.process();
        rc_TPTkMuStub_fakemu.process();
        rc_Mantra_TkMu_barr.process();
        rc_Mantra_TkMu_ovrl.process();
        rc_Mantra_TkMu_endc.process();
    }

    // make rate plots
    rc_EMTF.makeRatePlot();
    rc_TPTkMu.makeRatePlot();
    rc_TPTkMu_truemu.makeRatePlot();
    rc_TPTkMu_fakemu.makeRatePlot();
    rc_MyTPTkMu.makeRatePlot();
    rc_UpgTkMu.makeRatePlot();
    rc_TPTkMuStub.makeRatePlot();
    rc_TPTkMuStub_truemu.makeRatePlot();
    rc_TPTkMuStub_fakemu.makeRatePlot();
    rc_Mantra_TkMu_barr.makeRatePlot();
    rc_Mantra_TkMu_ovrl.makeRatePlot();
    rc_Mantra_TkMu_endc.makeRatePlot();

    // save to file
    rc_EMTF.saveToFile(fOut);
    rc_TPTkMu.saveToFile(fOut);
    rc_TPTkMu_truemu.saveToFile(fOut);
    rc_TPTkMu_fakemu.saveToFile(fOut);
    rc_MyTPTkMu.saveToFile(fOut);
    rc_UpgTkMu.saveToFile(fOut);
    rc_TPTkMuStub.saveToFile(fOut);
    rc_TPTkMuStub_truemu.saveToFile(fOut);
    rc_TPTkMuStub_fakemu.saveToFile(fOut);
    rc_Mantra_TkMu_barr.saveToFile(fOut);
    rc_Mantra_TkMu_ovrl.saveToFile(fOut);
    rc_Mantra_TkMu_endc.saveToFile(fOut);
}
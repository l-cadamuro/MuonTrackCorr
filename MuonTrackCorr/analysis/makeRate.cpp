#include "RateCalculator.h"
#include "MuTkTree.h"
#include "Correlator.h"
#include "Correlator_L1TTgroup_impl.h"
#include "TH1.h"
#include "TH2.h"
#include <string>
#include <iostream>
#include <vector>

using namespace std;

#define DEBUG false
#define fiducial_eta_min 1.2
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


    int quantile = 99;
    bool doRelax = true;
    float sftor  = 0.5;
    float sftor_initial = 0.0;

    // int maxEvts = 100000;
    int maxEvts = -1;

    /// -----------------------------------------------------------

    cout << "... running on filelist " << filelist << endl;
    cout << "... saving output to " << outputname << endl;

    TChain* ch = new TChain("Ntuplizer/MuonTrackTree");
    MuTkTree mtkt (ch);

    int appd = appendFromFileList (ch, filelist);
    cout << "... read out " << appd << " files" << endl;

    RateCalculator rc_EMTF("EMTF");
    RateCalculator rc_TPTkMu("TPTkMu");
    RateCalculator rc_MyTPTkMu("MyTPTkMu"); // my implementation
    RateCalculator rc_UpgTkMu("UpgTkMu");

    rc_EMTF.setStyle(kBlue);
    rc_TPTkMu.setStyle(kRed);
    rc_MyTPTkMu.setStyle(kOrange);
    rc_UpgTkMu.setStyle(kGreen+1);

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

    for (uint iEv = 0; true; ++iEv)
    {
        if (!mtkt.Next()) break;

        if (maxEvts > -1 && iEv > maxEvts)
            break;

        if (iEv % 10000 == 0 || DEBUG)
            cout << "... processing " << iEv << endl;

        // fill rates
        for (uint iemtf = 0; iemtf < *(mtkt.n_EMTF_mu); ++iemtf)
            // rc_EMTF.feedPt(mtkt.EMTF_mu_pt.At(iemtf));
            rc_EMTF.feedPt(mtkt.EMTF_mu_pt_xml.At(iemtf));

        for (uint itkmu = 0; itkmu < *(mtkt.n_L1_TkMu); ++itkmu){
            float aeta = std::fabs(mtkt.L1_TkMu_eta.At(itkmu));
            if (aeta < fiducial_eta_min || aeta > fiducial_eta_max)
                continue;
            // cout << mtkt.L1_TkMu_eta.At(itkmu) << endl;
            rc_TPTkMu.feedPt(mtkt.L1_TkMu_pt.At(itkmu));
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

        // make the rate plots here, once all pt filled
        rc_EMTF.process();
        rc_TPTkMu.process();
        rc_MyTPTkMu.process();
        rc_UpgTkMu.process();
    }

    // make rate plots
    rc_EMTF.makeRatePlot();
    rc_TPTkMu.makeRatePlot();
    rc_MyTPTkMu.makeRatePlot();
    rc_UpgTkMu.makeRatePlot();

    // save to file
    rc_EMTF.saveToFile(fOut);
    rc_TPTkMu.saveToFile(fOut);
    rc_MyTPTkMu.saveToFile(fOut);
    rc_UpgTkMu.saveToFile(fOut);
}
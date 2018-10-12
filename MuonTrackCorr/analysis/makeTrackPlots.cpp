#include <iostream>
#include <string>
#include <utility>
#include <algorithm>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include "TRandom3.h"
#include "TTree.h"
#include "TMath.h"
#include "TChain.h"
#include "TFile.h"
#include "TH2.h"
#include "TVector2.h"

#include "MuTkTree.h"
#include "Correlator.h"
#include "Correlator_L1TTgroup_impl.h"

#include <boost/accumulators/accumulators.hpp>
#include <boost/accumulators/statistics/stats.hpp>
#include <boost/algorithm/string/replace.hpp>

using namespace std;
using namespace boost::accumulators; // for mean and std

#define DEBUG false

#define fiducial_eta_min 1.2
#define fiducial_eta_max 2.4

// c++ -lm -o makeTrackPlots makeTrackPlots.cpp `root-config --glibs --cflags` -lTreePlayer

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

// NB: phi must be in radians
float deltaR (float eta1, float phi1, float eta2, float phi2)
{
        float deta = eta1 - eta2;
        float dphi = TVector2::Phi_mpi_pi(phi1-phi2);
        return TMath::Sqrt( deta*deta + dphi*dphi );
}

// return pair of idx best (first) amnd num possible cands (second)
std::pair<int, int> findBest(
    float eta_tm, float phi_tm,
    TTreeReaderArray<float>& pts, TTreeReaderArray<float>& etas, TTreeReaderArray<float>& phis,
    bool phiIsInDeg = false, float dRmax = 99999, bool apply_fiducial_theta = true)
{
    std::vector<pair<float, int>> vGood;
    for (uint ic = 0; ic < pts.GetSize(); ++ic)
    {
        if ( eta_tm * etas.At(ic) < 0.0) // opposite endcap
            continue; // reject those that are in opposite hemispheres
        
        // restrict to objects in the endcaps
        if (apply_fiducial_theta  && (std::abs(etas.At(ic)) < fiducial_eta_min || std::abs(etas.At(ic)) > fiducial_eta_max)){
            // if (DEBUG && phiIsInDeg) cout << ic << " - I fail the eta boundaries " << " --> " << std::abs(etas.At(ic)) << " " << std::abs(etas.At(ic)) << endl;
            continue;
        }

        float this_phi = (phiIsInDeg ? deg_to_rad(phis.At(ic)) : phis.At(ic) );
        float this_eta = etas.At(ic);
        if (deltaR(eta_tm, phi_tm, this_eta, this_phi) > dRmax)
            continue;
        vGood.push_back(make_pair(pts.At(ic), ic));
    }

    pair<int, int> results = make_pair(-1, 0);
    if (vGood.size() > 0)
    {
        sort(vGood.begin(), vGood.end());
        results.first = vGood.at(vGood.size()-1).second; // pick highest pT --> last element
        results.second = vGood.size();
    }
    return results;
}

int n_mu_in_endcap (MuTkTree& mtkt, bool endcap_pos)
{
    // float aetamin = 1.2;
    // float aetamax = 2.4;

    float aetamin = fiducial_eta_min;
    float aetamax = fiducial_eta_max;

    int np = 0;
    int nm = 0;

    // loop on gen muons
    for (uint igm = 0; igm < *(mtkt.n_gen_mu); ++igm)
    {
        float eta = mtkt.gen_mu_eta.At(igm);
        float phi = mtkt.gen_mu_phi.At(igm);
        float aeta = std::abs(eta);
        
        // endcap only
        if (aeta < aetamin || aeta > aetamax)
            continue;

        if (eta > 0) ++np;
        else ++nm; 
    }

    if (endcap_pos) return np;
    else return nm;
    // if (np > 1) return false; // 2 or more mus in eta+
    // if (nm > 1) return false; // 2 or more mus in eta-
    // if (np == 0 && nm == 0) return false; // no mu in boht eta+ and eta-
    // return true;
}


int main(int argc, char** argv)
{
    string filelist = "EMPTY";
    string outputname = "EMPTY";
    
    string suffix = "mults"; // or leave empty
    
    int iconfig = 0; 

    // override from cms line
    if (argc > 1)
        iconfig = std::stoi(argv[1]);

    if (iconfig == 0) { // DEFAULT
        cout << "... customised to MuMu gun, PU0, flat pT" << endl;
        filelist = "filelist/MuMu_flatPt_0PU_3Mag_TkMu_moreinfotrk.txt";
        outputname = "trk_plots_MuMu_flatPt_0PU.root";            
    }
    if (iconfig == 1) {
        cout << "... customised to MuMu gun, PU0, 1/pT" << endl;
        filelist = "filelist/MuMu_OneOverPt_0PU_3Mag_TkMu_moreinfotrk.txt";
        outputname = "trk_plots_MuMu_OneOverPt_0PU.root";
    }
    if (iconfig == 2) {
        cout << "... customised to ZMuMu, PU0" << endl;
        filelist = "filelist/ZToMuMu_RelVal_PU0_3Mag_TkMu_moreinfotrk.txt";
        outputname = "trk_plots_ZToMuMu_0PU.root";
    }
    if (iconfig == 3) {
        cout << "... customised to ZMuMu, PU200" << endl;
        filelist = "filelist/ZToMuMu_RelVal_PU200_3Mag_TkMu_moreinfotrk.txt";
        outputname = "trk_plots_ZToMuMu_200PU.root";
    }
    if (iconfig == 4) {
        cout << "... customised to Neutrino Gun, PU200" << endl;
        filelist = "filelist/NuGun_200PU_8Giu_TkMu_moreinfotrk_allEvts.txt";
        outputname = "trk_plots_NeutrinoGun_200PU.root";
    }

    // --- suffix to modify output name
    if (argc > 2)
        suffix = argv[2];

    if (!suffix.empty())
    {
        cout << "... appending suffix " << suffix << endl;  
        boost::replace_all(outputname, ".root", string("_") + suffix + string(".root"));
        cout << outputname << endl;
    }


    int maxEvts = -1;

    cout << "... running on filelist " << filelist << endl;

    TChain* ch = new TChain("Ntuplizer/MuonTrackTree");
    MuTkTree mtkt (ch);

    TFile* fOut = new TFile (outputname.c_str(), "recreate");
    // TTree* tOut = new TTree("tree", "tree");
    
    TH1D* nTracks_2 = new TH1D("nTracks_2",   "Tracks in the endcap;N_{tracks} with p_{T} > 2 GeV; a.u.",  150, 0, 150);
    TH1D* nTracks_3 = new TH1D("nTracks_3",   "Tracks in the endcap;N_{tracks} with p_{T} > 3 GeV; a.u.",  150, 0, 150);
    TH1D* nTracks_5 = new TH1D("nTracks_5",   "Tracks in the endcap;N_{tracks} with p_{T} > 5 GeV; a.u.",  150, 0, 150);
    TH1D* nTracks_10 = new TH1D("nTracks_10", "Tracks in the endcap;N_{tracks} with p_{T} > 10 GeV; a.u.", 150, 0, 150);

    TH1D* nTracks_em_2 = new TH1D("nTracks_em_2",   "Tracks in the endcap;N_{tracks} with p_{T} > 2 GeV; a.u.",  150, 0, 150);
    TH1D* nTracks_em_3 = new TH1D("nTracks_em_3",   "Tracks in the endcap;N_{tracks} with p_{T} > 3 GeV; a.u.",  150, 0, 150);
    TH1D* nTracks_em_5 = new TH1D("nTracks_em_5",   "Tracks in the endcap;N_{tracks} with p_{T} > 5 GeV; a.u.",  150, 0, 150);
    TH1D* nTracks_em_10 = new TH1D("nTracks_em_10", "Tracks in the endcap;N_{tracks} with p_{T} > 10 GeV; a.u.", 150, 0, 150);

    TH1D* nTracks_2_60deg = new TH1D("nTracks_2_60deg",   "Tracks in the endcap;N_{tracks} with p_{T} > 2 GeV in phi [0, 60] deg; a.u.",  150, 0, 150);
    TH1D* nTracks_3_60deg = new TH1D("nTracks_3_60deg",   "Tracks in the endcap;N_{tracks} with p_{T} > 3 GeV in phi [0, 60] deg; a.u.",  150, 0, 150);
    TH1D* nTracks_5_60deg = new TH1D("nTracks_5_60deg",   "Tracks in the endcap;N_{tracks} with p_{T} > 5 GeV in phi [0, 60] deg; a.u.",  150, 0, 150);
    TH1D* nTracks_10_60deg = new TH1D("nTracks_10_60deg", "Tracks in the endcap;N_{tracks} with p_{T} > 10 GeV in phi [0, 60] deg; a.u.", 150, 0, 150);

    TH1D* nEMTF_2 = new TH1D("nEMTF_2",   "EMTF in the endcap;N_{EMTF} with p_{T} > 2 GeV; a.u.",  150, 0, 150);
    TH1D* nEMTF_3 = new TH1D("nEMTF_3",   "EMTF in the endcap;N_{EMTF} with p_{T} > 3 GeV; a.u.",  150, 0, 150);
    TH1D* nEMTF_5 = new TH1D("nEMTF_5",   "EMTF in the endcap;N_{EMTF} with p_{T} > 5 GeV; a.u.",  150, 0, 150);
    TH1D* nEMTF_10 = new TH1D("nEMTF_10", "EMTF in the endcap;N_{EMTF} with p_{T} > 10 GeV; a.u.", 150, 0, 150);

    TH1D* nEMTF_2_60deg = new TH1D("nEMTF_2_60deg",   "EMTF in the endcap;N_{EMTF} with p_{T} > 2 GeV in phi [0, 60] deg; a.u.",  150, 0, 150);
    TH1D* nEMTF_3_60deg = new TH1D("nEMTF_3_60deg",   "EMTF in the endcap;N_{EMTF} with p_{T} > 3 GeV in phi [0, 60] deg; a.u.",  150, 0, 150);
    TH1D* nEMTF_5_60deg = new TH1D("nEMTF_5_60deg",   "EMTF in the endcap;N_{EMTF} with p_{T} > 5 GeV in phi [0, 60] deg; a.u.",  150, 0, 150);
    TH1D* nEMTF_10_60deg = new TH1D("nEMTF_10_60deg", "EMTF in the endcap;N_{EMTF} with p_{T} > 10 GeV in phi [0, 60] deg; a.u.", 150, 0, 150);

    TH1D* track_pt = new TH1D("track_pt", "Tracks in the endcap;p_{T} [GeV]; a.u.", 1000, 0, 1000);

    TH1D* EMTF_pt = new TH1D("EMTF_pt", "EMTFs in the endcap;p_{T} [GeV]; a.u.", 1000, 0, 1000);
    
    TH1D* track_eta_2 = new TH1D("track_eta_2",   "N_{tracks} with p_{T} > 2 GeV; track #eta; a.u.",  100, -3, 3);
    TH1D* track_eta_3 = new TH1D("track_eta_3",   "N_{tracks} with p_{T} > 3 GeV; track #eta; a.u.",  100, -3, 3);
    TH1D* track_eta_5 = new TH1D("track_eta_5",   "N_{tracks} with p_{T} > 5 GeV; track #eta; a.u.",  100, -3, 3);
    TH1D* track_eta_10 = new TH1D("track_eta_10", "N_{tracks} with p_{T} > 10 GeV; track #eta; a.u.", 100, -3, 3);


    TH1D* namu_2_dR0p7 = new TH1D("namu_2_dR0p7",   "Tracks with #Delta R < 0.7 from the gen. #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* namu_2_dR0p5 = new TH1D("namu_2_dR0p5",   "Tracks with #Delta R < 0.5 from the gen. #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* namu_2_dR0p3 = new TH1D("namu_2_dR0p3",   "Tracks with #Delta R < 0.3 from the gen. #mu;N_{tracks}; a.u.",  150, 0, 150);

    TH1D* namu_3_dR0p7 = new TH1D("namu_3_dR0p7",   "Tracks with #Delta R < 0.7 from the gen. #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* namu_3_dR0p5 = new TH1D("namu_3_dR0p5",   "Tracks with #Delta R < 0.5 from the gen. #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* namu_3_dR0p3 = new TH1D("namu_3_dR0p3",   "Tracks with #Delta R < 0.3 from the gen. #mu;N_{tracks}; a.u.",  150, 0, 150);

    TH1D* namu_5_dR0p7 = new TH1D("namu_5_dR0p7",   "Tracks with #Delta R < 0.7 from the gen. #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* namu_5_dR0p5 = new TH1D("namu_5_dR0p5",   "Tracks with #Delta R < 0.5 from the gen. #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* namu_5_dR0p3 = new TH1D("namu_5_dR0p3",   "Tracks with #Delta R < 0.3 from the gen. #mu;N_{tracks}; a.u.",  150, 0, 150);


    TH1D* naemtf_2_dR0p7 = new TH1D("naemtf_2_dR0p7",   "Tracks with #Delta R < 0.7 from the EMTF #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* naemtf_2_dR0p5 = new TH1D("naemtf_2_dR0p5",   "Tracks with #Delta R < 0.5 from the EMTF #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* naemtf_2_dR0p3 = new TH1D("naemtf_2_dR0p3",   "Tracks with #Delta R < 0.3 from the EMTF #mu;N_{tracks}; a.u.",  150, 0, 150);

    TH1D* naemtf_3_dR0p7 = new TH1D("naemtf_3_dR0p7",   "Tracks with #Delta R < 0.7 from the EMTF #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* naemtf_3_dR0p5 = new TH1D("naemtf_3_dR0p5",   "Tracks with #Delta R < 0.5 from the EMTF #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* naemtf_3_dR0p3 = new TH1D("naemtf_3_dR0p3",   "Tracks with #Delta R < 0.3 from the EMTF #mu;N_{tracks}; a.u.",  150, 0, 150);

    TH1D* naemtf_5_dR0p7 = new TH1D("naemtf_5_dR0p7",   "Tracks with #Delta R < 0.7 from the EMTF #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* naemtf_5_dR0p5 = new TH1D("naemtf_5_dR0p5",   "Tracks with #Delta R < 0.5 from the EMTF #mu;N_{tracks}; a.u.",  150, 0, 150);
    TH1D* naemtf_5_dR0p3 = new TH1D("naemtf_5_dR0p3",   "Tracks with #Delta R < 0.3 from the EMTF #mu;N_{tracks}; a.u.",  150, 0, 150);

    TH1D* naemtf_L1TTalgo = new TH1D("naemtf_L1TTalgo",   "Tracks around EMTF as in L1TT algo;N_{tracks}; a.u.",  150, 0, 150);


    // TH1D* nTracks_3 = new TH1D("nTracks_3",   "Tracks in the endcap;N tracks p_{T} > 3 GeV; a.u.",  150, 0, 150);
    // TH1D* nTracks_5 = new TH1D("nTracks_5",   "Tracks in the endcap;N tracks p_{T} > 5 GeV; a.u.",  150, 0, 150);
    // TH1D* nTracks_10 = new TH1D("nTracks_10", "Tracks in the endcap;N tracks p_{T} > 10 GeV; a.u.", 150, 0, 150);


    int appd = appendFromFileList (ch, filelist);
    cout << "... read out " << appd << " files" << endl;

    TRandom3* rndmService = new TRandom3(0);

    for (uint iEv = 0; true; ++iEv)
    {
        if (!mtkt.Next()) break;

        if (maxEvts > -1 && iEv > maxEvts)
            break;

        if (iEv % 10000 == 0 || DEBUG)
            cout << "... processing " << iEv << endl;

        int nt_2 = 0;
        int nt_3 = 0;
        int nt_5 = 0;
        int nt_10 = 0;

        int nt_em_2 = 0;
        int nt_em_3 = 0;
        int nt_em_5 = 0;
        int nt_em_10 = 0;

        int nt_2_60deg = 0;
        int nt_3_60deg = 0;
        int nt_5_60deg = 0;
        int nt_10_60deg = 0;

        int nt_em_2_60deg = 0;
        int nt_em_3_60deg = 0;
        int nt_em_5_60deg = 0;
        int nt_em_10_60deg = 0;

        const int ngm_ep = n_mu_in_endcap(mtkt, true);
        const int ngm_em = n_mu_in_endcap(mtkt, false);

        /// track multiplicities etc
        for (uint it = 0; it < *(mtkt.n_L1TT_trk); ++it)
        {
            float tk_eta = mtkt.L1TT_trk_eta.At(it);
            float tk_pt  = mtkt.L1TT_trk_pt.At(it);
            float tk_phi = mtkt.L1TT_trk_phi.At(it);

            // use only tracks in events where no gen mu is in the corresponding endcap
            // to avoid biases from the gen mu track itself

            bool endcap_empty = false;
            if (tk_eta > 0)
                endcap_empty = (ngm_ep == 0 ? true : false);
            if (tk_eta < 0)
                endcap_empty = (ngm_em == 0 ? true : false);
            if (iconfig == 4)
                endcap_empty = true; // bypass this for nu gun events

            if (fabs(tk_eta) > fiducial_eta_min && fabs(tk_eta) < fiducial_eta_max && endcap_empty)
            // if (true)
            {
                if (tk_eta > 0) // do not apply abs, so I count on a single endcap
                {
                    if (tk_pt > 2) ++nt_2;
                    if (tk_pt > 3) ++nt_3;
                    if (tk_pt > 5) ++nt_5;
                    if (tk_pt > 10) ++nt_10;

                    // phi in radians
                    if (tk_pt > 2 && tk_phi > 0 && tk_phi < 1.0472) ++nt_2_60deg;
                    if (tk_pt > 3 && tk_phi > 0 && tk_phi < 1.0472) ++nt_3_60deg;
                    if (tk_pt > 5 && tk_phi > 0 && tk_phi < 1.0472) ++nt_5_60deg;
                    if (tk_pt > 10 && tk_phi > 0 && tk_phi < 1.0472) ++nt_10_60deg;

                }
                else
                {
                    if (tk_pt > 2) ++nt_em_2;
                    if (tk_pt > 3) ++nt_em_3;
                    if (tk_pt > 5) ++nt_em_5;
                    if (tk_pt > 10) ++nt_em_10;                    
                }

                            
                track_pt -> Fill(tk_pt);
                if (tk_pt > 2) track_eta_2->Fill(tk_eta);
                if (tk_pt > 3) track_eta_3->Fill(tk_eta);
                if (tk_pt > 5) track_eta_5->Fill(tk_eta);
                if (tk_pt > 10) track_eta_10->Fill(tk_eta);

            }
        }
        nTracks_2 ->Fill(nt_2);
        nTracks_3 ->Fill(nt_3);
        nTracks_5 ->Fill(nt_5);
        nTracks_10 ->Fill(nt_10);

        nTracks_em_2 ->Fill(nt_em_2);
        nTracks_em_3 ->Fill(nt_em_3);
        nTracks_em_5 ->Fill(nt_em_5);
        nTracks_em_10 ->Fill(nt_em_10);

        nTracks_2_60deg ->Fill(nt_2_60deg);
        nTracks_3_60deg ->Fill(nt_3_60deg);
        nTracks_5_60deg ->Fill(nt_5_60deg);
        nTracks_10_60deg ->Fill(nt_10_60deg);


        // gen mu plots
        for (uint igm = 0; igm < *(mtkt.n_gen_mu); ++igm)
        {
            float eta_gm = mtkt.gen_mu_eta.At(igm);
            float phi_gm = mtkt.gen_mu_phi.At(igm);

            // to make plots arund a random point instead of a gen mu
            // float eta_gm = rndmService->Uniform(1.2, 2.4);
            // float phi_gm = rndmService->Uniform(-1.*TMath::Pi(), TMath::Pi());

            if (fabs(eta_gm) < fiducial_eta_min || fabs(eta_gm) > fiducial_eta_max)
                continue;

            // not the most efficient way, but good enough
            int ntrk_2_0p7 = 0;
            int ntrk_2_0p5 = 0;
            int ntrk_2_0p3 = 0;

            int ntrk_3_0p7 = 0;
            int ntrk_3_0p5 = 0;
            int ntrk_3_0p3 = 0;

            int ntrk_5_0p7 = 0;
            int ntrk_5_0p5 = 0;
            int ntrk_5_0p3 = 0;

            for (uint it = 0; it < *(mtkt.n_L1TT_trk); ++it)
            {
                float tk_eta = mtkt.L1TT_trk_eta.At(it);
                float tk_phi = mtkt.L1TT_trk_phi.At(it);
                float tk_pt  = mtkt.L1TT_trk_pt.At(it);
                float tk_p   = mtkt.L1TT_trk_p.At(it);
                float tk_z       = mtkt.L1TT_trk_z.At(it);
                float tk_chi2    = mtkt.L1TT_trk_chi2.At(it);
                float tk_nstubs  = mtkt.L1TT_trk_nstubs.At(it);

                float dR = deltaR(eta_gm, phi_gm, tk_eta, tk_phi);
                
                if (dR < 0.7 && tk_pt > 2.0) ++ ntrk_2_0p7;
                if (dR < 0.5 && tk_pt > 2.0) ++ ntrk_2_0p5;
                if (dR < 0.3 && tk_pt > 2.0) ++ ntrk_2_0p3;

                if (dR < 0.7 && tk_pt > 3.0) ++ ntrk_3_0p7;
                if (dR < 0.5 && tk_pt > 3.0) ++ ntrk_3_0p5;
                if (dR < 0.3 && tk_pt > 3.0) ++ ntrk_3_0p3;

                if (dR < 0.7 && tk_pt > 5.0) ++ ntrk_5_0p7;
                if (dR < 0.5 && tk_pt > 5.0) ++ ntrk_5_0p5;
                if (dR < 0.3 && tk_pt > 5.0) ++ ntrk_5_0p3;

            }

            namu_2_dR0p7->Fill(ntrk_2_0p7);
            namu_2_dR0p5->Fill(ntrk_2_0p5);
            namu_2_dR0p3->Fill(ntrk_2_0p3);            

            namu_3_dR0p7->Fill(ntrk_3_0p7);
            namu_3_dR0p5->Fill(ntrk_3_0p5);
            namu_3_dR0p3->Fill(ntrk_3_0p3);            

            namu_5_dR0p7->Fill(ntrk_5_0p7);
            namu_5_dR0p5->Fill(ntrk_5_0p5);
            namu_5_dR0p3->Fill(ntrk_5_0p3);            

        }

        // EMTF plots
        for (uint igm = 0; igm < *(mtkt.n_gen_mu); ++igm)
        {
            float eta_gm = mtkt.gen_mu_eta.At(igm);
            float phi_gm = mtkt.gen_mu_phi.At(igm);

            // float eta_gm = rndmService->Uniform(1.2, 2.4);
            // float phi_gm = rndmService->Uniform(-1.*TMath::Pi(), TMath::Pi());

            if (fabs(eta_gm) < fiducial_eta_min || fabs(eta_gm) > fiducial_eta_max)
                continue;

            auto best_emtf  = findBest(eta_gm, phi_gm, mtkt.EMTF_mu_pt,  mtkt.EMTF_mu_eta,  mtkt.EMTF_mu_phi,  true, 99999, false); // no eta cuts for the emtf (scattering is large)
            int ibest_emtf  = best_emtf.first;
            if (ibest_emtf < 0) continue;
            
            float emtf_pt    = mtkt.EMTF_mu_pt.At(ibest_emtf);
            float emtf_eta   = mtkt.EMTF_mu_eta.At(ibest_emtf);
            float emtf_theta = to_mpio2_pio2(eta_to_theta(mtkt.EMTF_mu_eta.At(ibest_emtf)));
            float emtf_phi   = deg_to_rad(mtkt.EMTF_mu_phi.At(ibest_emtf));

            int ntrk_2_0p7 = 0;
            int ntrk_2_0p5 = 0;
            int ntrk_2_0p3 = 0;

            int ntrk_3_0p7 = 0;
            int ntrk_3_0p5 = 0;
            int ntrk_3_0p3 = 0;

            int ntrk_5_0p7 = 0;
            int ntrk_5_0p5 = 0;
            int ntrk_5_0p3 = 0;
            
            int ntrk_L1TTalgo = 0;

            // find how many tracks are around
            for (uint it = 0; it < *(mtkt.n_L1TT_trk); ++it)
            {
                float tk_eta = mtkt.L1TT_trk_eta.At(it);
                float tk_phi = mtkt.L1TT_trk_phi.At(it);
                float tk_pt  = mtkt.L1TT_trk_pt.At(it);
                float tk_p   = mtkt.L1TT_trk_p.At(it);
                float tk_z       = mtkt.L1TT_trk_z.At(it);
                float tk_chi2    = mtkt.L1TT_trk_chi2.At(it);
                float tk_nstubs  = mtkt.L1TT_trk_nstubs.At(it);

                float dR = deltaR(emtf_eta, emtf_phi, tk_eta, tk_phi);
                
                if (dR < 0.7 && tk_pt > 2.0) ++ ntrk_2_0p7;
                if (dR < 0.5 && tk_pt > 2.0) ++ ntrk_2_0p5;
                if (dR < 0.3 && tk_pt > 2.0) ++ ntrk_2_0p3;

                if (dR < 0.7 && tk_pt > 3.0) ++ ntrk_3_0p7;
                if (dR < 0.5 && tk_pt > 3.0) ++ ntrk_3_0p5;
                if (dR < 0.3 && tk_pt > 3.0) ++ ntrk_3_0p3;

                if (dR < 0.7 && tk_pt > 5.0) ++ ntrk_5_0p7;
                if (dR < 0.5 && tk_pt > 5.0) ++ ntrk_5_0p5;
                if (dR < 0.3 && tk_pt > 5.0) ++ ntrk_5_0p3;
            
                // same selection as L1TT impl
                if (dR*dR < 0.5 && tk_pt > 2.0 && fabs(tk_z) < 25. && tk_chi2 < 100. && tk_nstubs > 3 && tk_p > 3.5 && fabs(tk_eta) > 1.2 && fabs(tk_eta) < 2.5)
                    ++ntrk_L1TTalgo;

            }
            
            naemtf_2_dR0p7->Fill(ntrk_2_0p7);
            naemtf_2_dR0p5->Fill(ntrk_2_0p5);
            naemtf_2_dR0p3->Fill(ntrk_2_0p3);            

            naemtf_3_dR0p7->Fill(ntrk_3_0p7);
            naemtf_3_dR0p5->Fill(ntrk_3_0p5);
            naemtf_3_dR0p3->Fill(ntrk_3_0p3);            

            naemtf_5_dR0p7->Fill(ntrk_5_0p7);
            naemtf_5_dR0p5->Fill(ntrk_5_0p5);
            naemtf_5_dR0p3->Fill(ntrk_5_0p3);                     

            naemtf_L1TTalgo->Fill(ntrk_L1TTalgo);            

        }

        int nemtf_2 = 0;
        int nemtf_3 = 0;
        int nemtf_5 = 0;
        int nemtf_10 = 0;

        int nemtf_2_60deg = 0;
        int nemtf_3_60deg = 0;
        int nemtf_5_60deg = 0;
        int nemtf_10_60deg = 0;

        // EMTF muitliplicites plots
        for (uint iemtf = 0; iemtf < *(mtkt.n_EMTF_mu); ++iemtf)
        {
            float emtf_pt    = mtkt.EMTF_mu_pt.At(iemtf);
            float emtf_eta   = mtkt.EMTF_mu_eta.At(iemtf);
            float emtf_theta = to_mpio2_pio2(eta_to_theta(mtkt.EMTF_mu_eta.At(iemtf)));
            float emtf_phi   = deg_to_rad(mtkt.EMTF_mu_phi.At(iemtf));

            // use only tracks in events where no gen mu is in the corresponding endcap
            // to avoid biases from the gen mu track itself

            bool endcap_empty = false;
            if (emtf_eta > 0)
                endcap_empty = (ngm_ep == 0 ? true : false);
            if (emtf_eta < 0)
                endcap_empty = (ngm_em == 0 ? true : false);
            if (iconfig == 4)
                endcap_empty = true; // bypass this for nu gun events

            if (endcap_empty)
            {
                if (emtf_eta > 0) // do not apply abs, so I count on a single endcap
                {
                    if (emtf_pt > 2) ++nemtf_2;
                    if (emtf_pt > 3) ++nemtf_3;
                    if (emtf_pt > 5) ++nemtf_5;
                    if (emtf_pt > 10) ++nemtf_10;

                    // phi in radians
                    if (emtf_pt > 2 && emtf_phi > 0 && emtf_phi < 1.0472) ++nemtf_2_60deg;
                    if (emtf_pt > 3 && emtf_phi > 0 && emtf_phi < 1.0472) ++nemtf_3_60deg;
                    if (emtf_pt > 5 && emtf_phi > 0 && emtf_phi < 1.0472) ++nemtf_5_60deg;
                    if (emtf_pt > 10 && emtf_phi > 0 && emtf_phi < 1.0472) ++nemtf_10_60deg;

                }
                            
                EMTF_pt -> Fill(emtf_pt);
                // if (emtf_pt > 2) track_eta_2->Fill(EMTF_eta);
                // if (emtf_pt > 3) track_eta_3->Fill(EMTF_eta);
                // if (emtf_pt > 5) track_eta_5->Fill(EMTF_eta);
                // if (emtf_pt > 10) track_eta_10->Fill(EMTF_eta);

            }
        }
        nEMTF_2 ->Fill(nemtf_2);
        nEMTF_3 ->Fill(nemtf_3);
        nEMTF_5 ->Fill(nemtf_5);
        nEMTF_10 ->Fill(nemtf_10);

        nEMTF_2_60deg ->Fill(nemtf_2_60deg);
        nEMTF_3_60deg ->Fill(nemtf_3_60deg);
        nEMTF_5_60deg ->Fill(nemtf_5_60deg);
        nEMTF_10_60deg ->Fill(nemtf_10_60deg);

    }

    fOut->Write();

}
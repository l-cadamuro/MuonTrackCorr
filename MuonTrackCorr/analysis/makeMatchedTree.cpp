#include <iostream>
#include <string>
#include <utility>
#include <algorithm>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
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

#define fiducial_eta_min 1.2
#define fiducial_eta_max 2.4

#define DEBUG false

// c++ -lm -o makeMatchedTree makeMatchedTree.cpp `root-config --glibs --cflags` -lTreePlayer
// ./makeMatchedTree plotType[0|1|2|3|4] suffix sftor sftor_init doRelax[0|1] quantile[90|95|99]

// hit structure to store
// S1
// S2
// S3
// S4
// and for each station:
// best CSC --> ring eta phi ...
// best RPC --> ring eta phi ...
// best GEM --> ring eta phi ...
// NOTE: need to solve ambiguities in defining the "BEST" hit
// NOTE2: check if ME0 is included and use it in case
// NOTE3: what to do for hits in chambers that are shifted

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
    bool phiIsInDeg = false, float dRmax = 99999, bool apply_fiducial_theta = true,
    bool pickClosest = false)
{
    std::vector<pair<float, int>> vGood;
    std::vector<pair<float, int>> vGood_closest;
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
        double dR = deltaR(eta_tm, phi_tm, this_eta, this_phi);
        if (dR > dRmax)
            continue;
        vGood.push_back(make_pair(pts.At(ic), ic));
        vGood_closest.push_back(make_pair(dR, ic));
    }

    pair<int, int> results = make_pair(-1, 0);
    if (vGood.size() > 0)
    {
        if (pickClosest)
        {
            sort(vGood_closest.begin(), vGood_closest.end());
            results.first = vGood_closest.at(0).second; // pick closest --> first element
            results.second = vGood_closest.size();            
        }
        else
        {
            sort(vGood.begin(), vGood.end());
            results.first = vGood.at(vGood.size()-1).second; // pick highest pT --> last element
            results.second = vGood.size();            
        }
    }
    return results;
}


// contains the hits to the "best" hits per each station - identified by idx
struct bestHits {
    bestHits() : 
        CSC ({-1,-1,-1,-1}),
        RPC ({-1,-1,-1,-1}),
        GEM ({-1,-1,-1,-1}),
        //
        nCSC(0),
        nRPC(0),
        nGEM(0),
        //
        rmsCSC_theta ({0,0,0,0}),
        rmsRPC_theta ({0,0,0,0}),
        rmsGEM_theta ({0,0,0,0}),
        rmsCSC_phi ({0,0,0,0}),
        rmsRPC_phi ({0,0,0,0}),
        rmsGEM_phi ({0,0,0,0}),
        //
        dmaxCSC_theta ({0,0,0,0}),
        dmaxRPC_theta ({0,0,0,0}),
        dmaxGEM_theta ({0,0,0,0}),
        dmaxCSC_phi ({0,0,0,0}),
        dmaxRPC_phi ({0,0,0,0}),
        dmaxGEM_phi ({0,0,0,0})
        {}
    std::array<int,4> CSC;
    std::array<int,4> RPC;
    std::array<int,4> GEM;
    int nCSC;
    int nRPC;
    int nGEM;
    // the spread of alternative hits when choosing
    std::array<float,4> rmsCSC_theta;
    std::array<float,4> rmsRPC_theta;
    std::array<float,4> rmsGEM_theta;
    std::array<float,4> rmsCSC_phi;
    std::array<float,4> rmsRPC_phi;
    std::array<float,4> rmsGEM_phi;
    // the max distance of alternative hits when choosing
    std::array<float,4> dmaxCSC_theta;
    std::array<float,4> dmaxRPC_theta;
    std::array<float,4> dmaxGEM_theta;
    std::array<float,4> dmaxCSC_phi;
    std::array<float,4> dmaxRPC_phi;
    std::array<float,4> dmaxGEM_phi;
};

/*
void setBHvalues(
    bestHits& bh,
    std::vector<std::tuple<float,float,int>>& CSCs,
    std::vector<std::tuple<float,float,int>>& RPCs,
    std::vector<std::tuple<float,float,int>>& GEMs)
{
    // completely arbitrary - take the 1st hit
    for (int is = 0; is < 4; ++is) // loop on 4 stations
    {
        bool hasCSC = (CSCs.size() > 0);
        bool hasRPC = (RPCs.size() > 0);
        bool hasGEM = (GEMs.size() > 0);
        
        bh.CSC = (hasCSC ? get<2>(CSCs.at(0)) : -1);
    }

    bh.nCSC = CSCs.size();
    bh.nRPC = RPCs.size();
    bh.nGEM = GEMs.size();

    return;
}

// selects the "best hits" 
std::pair<bestHits, bestHits> findBestHits (MuTkTree& mtkt)
{

    bestHits bh_ep;
    bestHits bh_en;

    std::vector<std::tuple<float,float,int>> CSCs_ep; // theta, phi, idx
    std::vector<std::tuple<float,float,int>> RPCs_ep; // theta, phi, idx
    std::vector<std::tuple<float,float,int>> GEMs_ep; // theta, phi, idx

    std::vector<std::tuple<float,float,int>> CSCs_en; // theta, phi, idx
    std::vector<std::tuple<float,float,int>> RPCs_en; // theta, phi, idx
    std::vector<std::tuple<float,float,int>> GEMs_en; // theta, phi, idx

    for (int ihit = 0; ihit < *(mtkt.n_mu_hit); ++ihit)
    {
        // accumulator_set<double, stats<tag::variance> > acc;
        // for_each(a_vec.begin(), a_vec.end(), bind<void>(ref(acc), _1));

        // to reduce the number of if-else, create refs to the correct endcap
        bestHits& rbh                  = (mtkt.mu_hit_endcap.At(ihit) > 0 ? bh_ep   : bh_en);
        auto& vhCSC  = (mtkt.mu_hit_endcap.At(ihit) > 0 ? CSCs_ep : CSCs_en);
        auto& vhRPC  = (mtkt.mu_hit_endcap.At(ihit) > 0 ? RPCs_ep : RPCs_en);
        auto& vhGEM  = (mtkt.mu_hit_endcap.At(ihit) > 0 ? GEMs_ep : GEMs_en);

        int type = mtkt.mu_hit_type.At(ihit);
        auto tp = make_tuple(mtkt.mu_hit_sim_theta.At(ihit), mtkt.mu_hit_sim_phi.At(ihit), ihit);
        
        if (type == 1){
            vhCSC.push_back(tp);
        }
        else if (type == 2){
            vhRPC.push_back(tp);
        }
        else if (type == 3){
            vhGEM.push_back(tp);
        }
        else{
            cout << "Cannot understand hit type " << type << ", skipping..." << endl;
            continue;
        }
    }

    // process the info that was stored    
    // endcap +
    setBHvalues(bh_ep, CSCs_ep, RPCs_ep, GEMs_ep);
    setBHvalues(bh_en, CSCs_en, RPCs_en, GEMs_en);

    return make_pair(bh_ep,bh_en);
}
*/

/*
// selects the "best hits" 
std::pair<bestHits, bestHits> findBestHits (MuTkTree& mtkt)
{
    std::vector<int> hits_sel;
    for (int ihit = 0; ihit < *(mtkt.n_mu_hit); ++ihit)
    {
        int endcap    = mtkt.mu_hit_endcap.At(ihit);
        int type      = mtkt.mu_hit_type.At(ihit);
        int station   = mtkt.mu_hit_station.At(ihit);
        int neigh     = mtkt.mu_hit_neighbor.At(ihit);

        // test : only S1 CSC hits
        if (endcap < 0)   continue;
        if (type != 1)    continue;
        if (station != 1) continue;
        if (neigh == 1)   continue;
        hits_sel.push_back(ihit);
    }

    if (hits_sel.size() > 1)
    {
        cout << "------- I got " << hits_sel.size() << " hits" << endl;  
        for (int idx : hits_sel)
        {
            cout << "   endcap : "    <<  mtkt.mu_hit_endcap.At(idx)
                 << "   station : "   <<  mtkt.mu_hit_station.At(idx)
                 << "   ring : "      <<  mtkt.mu_hit_ring.At(idx)
                 << "   sector : "    <<  mtkt.mu_hit_sector.At(idx)
                 << "   subsector : " <<  mtkt.mu_hit_subsector.At(idx)
                 << "   chamber : "   <<  mtkt.mu_hit_chamber.At(idx)
                 << "   cscid : "     <<  mtkt.mu_hit_cscid.At(idx)
                 << "   bx : "        <<  mtkt.mu_hit_bx.At(idx)
                 << "   type : "      <<  mtkt.mu_hit_type.At(idx)
                 << "   neighbor : "  <<  mtkt.mu_hit_neighbor.At(idx)
                 << "   sim_phi : "   <<  mtkt.mu_hit_sim_phi.At(idx)
                 << "   sim_theta : " <<  mtkt.mu_hit_sim_theta.At(idx)
                 << "   sim_eta : "   <<  mtkt.mu_hit_sim_eta.At(idx)
                 << endl;
        }
    }

    // fake return
    bestHits bh_ep;
    bestHits bh_en;
    return make_pair(bh_ep,bh_en);

}
*/

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

void dumpHits(MuTkTree& mtkt)
{
    cout << "------- I got " << *(mtkt.n_mu_hit) << " hits" << endl;  
    for (int idx = 0; idx < *(mtkt.n_mu_hit) ; ++idx)
    {
        cout << "   endcap : "    <<  mtkt.mu_hit_endcap.At(idx)
             << "   station : "   <<  mtkt.mu_hit_station.At(idx)
             << "   ring : "      <<  mtkt.mu_hit_ring.At(idx)
             << "   sector : "    <<  mtkt.mu_hit_sector.At(idx)
             << "   subsector : " <<  mtkt.mu_hit_subsector.At(idx)
             << "   chamber : "   <<  mtkt.mu_hit_chamber.At(idx)
             << "   cscid : "     <<  mtkt.mu_hit_cscid.At(idx)
             << "   bx : "        <<  mtkt.mu_hit_bx.At(idx)
             << "   type : "      <<  mtkt.mu_hit_type.At(idx)
             << "   neighbor : "  <<  mtkt.mu_hit_neighbor.At(idx)
             << "   sim_phi : "   <<  mtkt.mu_hit_sim_phi.At(idx)
             << "   sim_theta : " <<  mtkt.mu_hit_sim_theta.At(idx)
             << "   sim_eta : "   <<  mtkt.mu_hit_sim_eta.At(idx)
             << endl;
    }
}

void dumpTkMu(MuTkTree& mtkt)
{
    cout << "------- This event has " << *(mtkt.n_L1_TkMu) << " TkMu" << endl;  
    for (int idx = 0; idx < *(mtkt.n_L1_TkMu) ; ++idx)
    {
        cout << "  pt : " << mtkt.L1_TkMu_pt.At(idx)
             << "  eta : " << mtkt.L1_TkMu_eta.At(idx)
             << "  phi : " << mtkt.L1_TkMu_phi.At(idx)
             << endl;
    }
}

void dumpGenMu(MuTkTree& mtkt)
{
    cout << "------- This event has " << *(mtkt.n_gen_mu) << " gen mu" << endl;  
    for (int idx = 0; idx < *(mtkt.n_gen_mu) ; ++idx)
    {
        cout << "  pt : " << mtkt.gen_mu_pt.At(idx)
             << "  eta : " << mtkt.gen_mu_eta.At(idx)
             << "  phi : " << mtkt.gen_mu_phi.At(idx)
             << endl;
    }
}

void dumpEMTF(MuTkTree& mtkt)
{
    cout << "------- This event has " << *(mtkt.n_EMTF_mu) << " EMTF mu" << endl;  
    for (int idx = 0; idx < *(mtkt.n_EMTF_mu) ; ++idx)
    {
        cout << "  pt : " << mtkt.EMTF_mu_pt.At(idx)
             << "  eta : " << mtkt.EMTF_mu_eta.At(idx)
             << "  phi : " << mtkt.EMTF_mu_phi.At(idx)
             << endl;
    }
}

void dumpTracks(MuTkTree& mtkt)
{
    cout << "------- This event has " << *(mtkt.n_L1TT_trk) << " L1TT tracks" << endl;  
    for (int idx = 0; idx < *(mtkt.n_L1TT_trk) ; ++idx)
    {
        cout << "  pt : " << mtkt.L1TT_trk_pt.At(idx)
             << "  eta : " << mtkt.L1TT_trk_eta.At(idx)
             << "  phi : " << mtkt.L1TT_trk_phi.At(idx)
             << endl;
    }
}


void dumpUpgTkMu(MuTkTree& mtkt, std::vector<int> corr_mu_idxs, bool remove_neg = false)
{
    cout << " ---- the UpgMuTk vector contains " << corr_mu_idxs.size() << " elements" << endl;
    cout << " --------------- of which " << count_if (corr_mu_idxs.begin(), corr_mu_idxs.end(), [](int i){return i >= 0;}) << " non-zero" << endl;
    if (remove_neg) cout  << " --------------- listing only good ones " << endl;
    for (int itrack = 0; itrack < corr_mu_idxs.size(); ++itrack)
    {
        int iEMTF = corr_mu_idxs.at(itrack);
        if (iEMTF < 0 && remove_neg)
            continue;
        cout << " itrk: " << itrack << " pt: " << mtkt.L1TT_trk_pt.At(itrack) << " eta: " << mtkt.L1TT_trk_eta.At(itrack) << " phi: " << mtkt.L1TT_trk_phi.At(itrack) << endl;
        if (iEMTF < 0)
            cout << " >>> iEMTF : " << iEMTF << endl;
        else
            cout << " >>> iEMTF : " << iEMTF << " pt: " << mtkt.EMTF_mu_pt.At(iEMTF) << " eta: " << mtkt.EMTF_mu_eta.At(iEMTF) << " phi: " << mtkt.EMTF_mu_phi.At(iEMTF) << endl;
    }
}


bool debugHitRefs(MuTkTree& mtkt)
{
    bool somethingBad = false;
    for (uint iEMTF = 0; iEMTF < *(mtkt.n_EMTF_mu); ++iEMTF)
    {
        int iref = mtkt.EMTF_mu_hitref2.At(iEMTF);
        if (iref < 0) continue;
        double eta_emtf = mtkt.EMTF_mu_eta.At(iEMTF);
        double eta_S2   = mtkt.mu_hit_sim_eta.At(iref);
        if (eta_emtf * eta_S2 < 0){
            cout << "etmf : " << eta_emtf << " " << eta_S2 << endl;
            somethingBad = true;
        }
    }
    return somethingBad;
}

bool single_mu_in_endcap (MuTkTree& mtkt)
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

    if (np > 1) return false; // 2 or more mus in eta+
    if (nm > 1) return false; // 2 or more mus in eta-
    if (np == 0 && nm == 0) return false; // no mu in boht eta+ and eta-
    return true;
}


int main(int argc, char** argv)
{

    // the default
    
    // string filelist = "filelist/MuMu_flatPt_0PU_25Apr_TkMu.txt";
    // string outputname = "matched_tree_MuMu_flatPt_0PU_25Apr_TkMu.root";

    // string filelist = "filelist/MuMu_flatPt_0PU_23Apr2018.txt";
    // string outputname = "matched_tree_MuMu_flatPt_0PU_23Apr2018.root";

    // string filelist = "filelist/MuMu_OneOverPt_0PU_23Apr2018.txt";
    // string outputname = "matched_tree_MuMu_OneOverPt_0PU_23Apr2018.root";

    // specifying a config from cmd line

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
        outputname = "matched_tree_MuMu_flatPt_0PU.root";            
    }
    if (iconfig == 1) {
        cout << "... customised to MuMu gun, PU0, 1/pT" << endl;
        filelist = "filelist/MuMu_OneOverPt_0PU_3Mag_TkMu_moreinfotrk.txt";
        outputname = "matched_tree_MuMu_OneOverPt_0PU.root";
    }
    if (iconfig == 2) {
        cout << "... customised to ZMuMu, PU0" << endl;
        filelist = "filelist/ZToMuMu_RelVal_PU0_3Mag_TkMu_moreinfotrk.txt";
        outputname = "matched_tree_ZToMuMu_0PU.root";
    }
    if (iconfig == 3) {
        cout << "... customised to ZMuMu, PU200" << endl;
        filelist = "filelist/ZToMuMu_RelVal_PU200_3Mag_TkMu_moreinfotrk.txt";
        outputname = "matched_tree_ZToMuMu_200PU.root";
    }
    if (iconfig == 4) {
        cout << "... customised to b jets, PU0" << endl;
        filelist = "filelist/BjetToMu_endcap_PosNegCat_0PU_25Giu_TkMu_moreinfotrk.txt";
        outputname = "matched_tree_Bjets_0PU.root";
    }
    // Nov review plots
    if (iconfig == 5) {
        cout << "... customised to single Mu, PU 200, DW corr w/o relax" << endl;
        filelist = "filelist/SingleMu_FlatPt-2to100_L1TPU200_12Ott_DWcorr_CMSSWdefaultNoRelax.txt";
        outputname = "matched_tree_SingleMu_PU200_DWcorr_CMSSWdefaultNoRelax.root";
    }
    if (iconfig == 6) {
        cout << "... customised to single Mu, PU 200, DW corr with relax" << endl;
        filelist = "filelist/SingleMu_FlatPt-2to100_L1TPU200_12Ott_DWcorr_relax0p5At6GeV.txt";
        outputname = "matched_tree_SingleMu_PU200_DWcorr_relax0p5At6GeV.root";
    }
    if (iconfig == 7) {
        cout << "... customised to single Mu, PU 200, TP corr dr 0.7" << endl;
        filelist = "filelist/SingleMu_FlatPt-2to100_L1TPU200_12Ott_TPcorr.txt";
        outputname = "matched_tree_SingleMu_PU200_TPcorr.root";
    }
    if (iconfig == 8) {
        cout << "... customised to single Mu, PU 200, TP corr dr 0.2" << endl;
        filelist = "filelist/SingleMu_FlatPt-2to100_L1TPU200_12Ott_TPcorr_SvenPars.txt";
        outputname = "matched_tree_SingleMu_PU200_TPcorr_SvenPars.root";
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

    // --- correlator safety factor
    float sftor = 0.5;
    if (argc > 3)
        sftor = std::stof(argv[3]);

    float sftor_initial = 0.0;
    if (argc > 4)
        sftor_initial = std::stof(argv[4]);

    bool doRelax = true;
    if (argc > 5)
        doRelax = (std::stoi(argv[5]) == 0 ? false : true);

    int quantile = 95;
    if (argc > 6)
        quantile = std::stoi(argv[6]);

    //////- ------- - ------- - ------- - ------- - -------

    // string filelist = "filelist/MuMu_flatPt_0PU_25Apr_TkMu_prePhiFix.txt";
    // string outputname = "matched_tree_MuMu_flatPt_0PU_25Apr_TkMu_prePhiFix.root";

    // string filelist = "filelist/debug_tkmu.txt";
    // string outputname = "matched_tree_DEBUG.root";


    /////////////////////////////////////////////////////////////////////

    // to select gen muons
    // float fiducial_eta_min = 1.2;
    // float fiducial_eta_max = 2.4;

    // to match with gen particles - NOTE: for mumu gun use 99999 since it is enough to check endcap sign
    // for Z->mumu use a meaningful cone, but note that it is not well defined for a match with the EMTF because of the bend
    // float dRmax = 0.3;
    float dRmax = 99999.;
    // float dRmax = 0.1;
    // float dRmax = 0.01;

    /////////////////////////////////////////////////////////////////////

    int maxEvts = -1;


    cout << "... running on filelist " << filelist << endl;

    TChain* ch = new TChain("Ntuplizer/MuonTrackTree");
    MuTkTree mtkt (ch);

    /*
    TTreeReader mtkt (ch);
    /////////////////////////////////////////////////////////////////////
    // Readers to access the data (delete the ones you do not need).
    
    TTreeReaderValue<UInt_t> n_EMTF_mu     = {mtkt, "n_EMTF_mu"};
    TTreeReaderArray<float> EMTF_mu_pt     = {mtkt, "EMTF_mu_pt"};
    TTreeReaderArray<float> EMTF_mu_pt_xml = {mtkt, "EMTF_mu_pt_xml"};
    TTreeReaderArray<float> EMTF_mu_eta    = {mtkt, "EMTF_mu_eta"};
    TTreeReaderArray<float> EMTF_mu_theta  = {mtkt, "EMTF_mu_theta"};
    TTreeReaderArray<float> EMTF_mu_phi    = {mtkt, "EMTF_mu_phi"};
    TTreeReaderArray<int> EMTF_mu_charge   = {mtkt, "EMTF_mu_charge"};
    TTreeReaderArray<int> EMTF_mu_mode     = {mtkt, "EMTF_mu_mode"};
    TTreeReaderArray<int> EMTF_mu_endcap   = {mtkt, "EMTF_mu_endcap"};
    TTreeReaderArray<int> EMTF_mu_sector   = {mtkt, "EMTF_mu_sector"};
    TTreeReaderArray<int> EMTF_mu_bx       = {mtkt, "EMTF_mu_bx"};
    TTreeReaderArray<int> EMTF_mu_hitref1  = {mtkt, "EMTF_mu_hitref1"};
    TTreeReaderArray<int> EMTF_mu_hitref2  = {mtkt, "EMTF_mu_hitref2"};
    TTreeReaderArray<int> EMTF_mu_hitref3  = {mtkt, "EMTF_mu_hitref3"};
    TTreeReaderArray<int> EMTF_mu_hitref4  = {mtkt, "EMTF_mu_hitref4"};
    
    TTreeReaderValue<UInt_t> n_L1TT_trk    = {mtkt, "n_L1TT_trk"};
    TTreeReaderArray<float> L1TT_trk_pt    = {mtkt, "L1TT_trk_pt"};
    TTreeReaderArray<float> L1TT_trk_eta   = {mtkt, "L1TT_trk_eta"};
    TTreeReaderArray<float> L1TT_trk_phi   = {mtkt, "L1TT_trk_phi"};
    
    TTreeReaderValue<UInt_t> n_gen_mu      = {mtkt, "n_gen_mu"};
    TTreeReaderArray<float> gen_mu_pt      = {mtkt, "gen_mu_pt"};
    TTreeReaderArray<float> gen_mu_eta     = {mtkt, "gen_mu_eta"};
    TTreeReaderArray<float> gen_mu_phi     = {mtkt, "gen_mu_phi"};
    TTreeReaderArray<float> gen_mu_e       = {mtkt, "gen_mu_e"};
    
    TTreeReaderValue<UInt_t> n_mu_hit        = {mtkt, "n_mu_hit"};
    TTreeReaderArray<short> mu_hit_endcap    = {mtkt, "mu_hit_endcap"};
    TTreeReaderArray<short> mu_hit_station   = {mtkt, "mu_hit_station"};
    TTreeReaderArray<short> mu_hit_ring      = {mtkt, "mu_hit_ring"};
    TTreeReaderArray<short> mu_hit_sector    = {mtkt, "mu_hit_sector"};
    TTreeReaderArray<short> mu_hit_subsector = {mtkt, "mu_hit_subsector"};
    TTreeReaderArray<short> mu_hit_chamber   = {mtkt, "mu_hit_chamber"};
    TTreeReaderArray<short> mu_hit_cscid     = {mtkt, "mu_hit_cscid"};
    TTreeReaderArray<short> mu_hit_bx        = {mtkt, "mu_hit_bx"};
    TTreeReaderArray<short> mu_hit_type      = {mtkt, "mu_hit_type"};
    TTreeReaderArray<short> mu_hit_neighbor  = {mtkt, "mu_hit_neighbor"};
    TTreeReaderArray<float> mu_hit_sim_phi   = {mtkt, "mu_hit_sim_phi"};
    TTreeReaderArray<float> mu_hit_sim_theta = {mtkt, "mu_hit_sim_theta"};
    TTreeReaderArray<float> mu_hit_sim_eta   = {mtkt, "mu_hit_sim_eta"};
    */


    /////////////////////////////////////////////////////////////////////

    TFile* fOut = new TFile (outputname.c_str(), "recreate");
    TTree* tOut = new TTree("tree", "tree");

    double gen_pt;
    double gen_eta;
    double gen_theta;
    double gen_phi;
    int    gen_charge;
    // double gen_z;
    double trk_pt;
    double trk_eta;
    double trk_theta;
    double trk_phi;
    double trk_chi2;
    int    trk_nstubs;
    int    trk_charge;
    int    trk_mult;
    // double trk_z;
    double tkmu_pt;
    double tkmu_eta;
    double tkmu_theta;
    double tkmu_phi;
    int    tkmu_mult;
    //
    double myimpltkmu_pt;
    double myimpltkmu_eta;
    double myimpltkmu_theta;
    double myimpltkmu_phi;
    int    myimpltkmu_mult;
    int    myimpltkmu_narb;
    //
    double upgtkmu_pt;
    double upgtkmu_eta;
    double upgtkmu_theta;
    double upgtkmu_phi;
    int    upgtkmu_mult;
    int    upgtkmu_narb;
    //
    // double tkmu_z;
    double emtf_pt;
    double emtf_xml_pt;
    double emtf_eta;
    double emtf_theta;
    double emtf_phi;
    int    emtf_charge;
    int    emtf_mode;
    int    emtf_mult;
    // position in S1
    bool   has_S1;
    int    S1_type;
    double S1_phi;
    double S1_eta;
    double S1_theta;
    // position in S2
    bool   has_S2;
    int    S2_type;
    double S2_phi;
    double S2_eta;
    double S2_theta;
    // position in S3
    bool   has_S3;
    int    S3_type;
    double S3_phi;
    double S3_eta;
    double S3_theta;
    // position in S4
    bool   has_S4;
    int    S4_type;
    double S4_phi;
    double S4_eta;
    double S4_theta;

    tOut->Branch("gen_pt",     &gen_pt);
    tOut->Branch("gen_eta",    &gen_eta);
    tOut->Branch("gen_theta",  &gen_theta);
    tOut->Branch("gen_phi",    &gen_phi);
    tOut->Branch("gen_charge", &gen_charge);
    // tOut->Branch("gen_z", & gen_z);
    
    tOut->Branch("trk_pt",     &trk_pt);
    tOut->Branch("trk_eta",    &trk_eta);
    tOut->Branch("trk_theta",  &trk_theta);
    tOut->Branch("trk_phi",    &trk_phi);
    tOut->Branch("trk_chi2",    &trk_chi2);
    tOut->Branch("trk_nstubs",    &trk_nstubs);
    tOut->Branch("trk_charge", &trk_charge);
    tOut->Branch("trk_mult",   &trk_mult); // how many valid trk were found in the event;
    // tOut->Branch("trk_z", &trk_z);

    tOut->Branch("tkmu_pt",    &tkmu_pt);
    tOut->Branch("tkmu_eta",   &tkmu_eta);
    tOut->Branch("tkmu_theta", &tkmu_theta);
    tOut->Branch("tkmu_phi",   &tkmu_phi);
    tOut->Branch("tkmu_mult",  &tkmu_mult); // how many valid trk were found in the event;

    tOut->Branch("myimpltkmu_pt",    &myimpltkmu_pt);
    tOut->Branch("myimpltkmu_eta",   &myimpltkmu_eta);
    tOut->Branch("myimpltkmu_theta", &myimpltkmu_theta);
    tOut->Branch("myimpltkmu_phi",   &myimpltkmu_phi);
    tOut->Branch("myimpltkmu_mult",  &myimpltkmu_mult); // how many valid trk were found in the event;
    tOut->Branch("myimpltkmu_narb",  &myimpltkmu_narb);

    tOut->Branch("upgtkmu_pt",    &upgtkmu_pt);
    tOut->Branch("upgtkmu_eta",   &upgtkmu_eta);
    tOut->Branch("upgtkmu_theta", &upgtkmu_theta);
    tOut->Branch("upgtkmu_phi",   &upgtkmu_phi);
    tOut->Branch("upgtkmu_mult",  &upgtkmu_mult);
    tOut->Branch("upgtkmu_narb",  &upgtkmu_narb);

    tOut->Branch("emtf_pt",     &emtf_pt);
    tOut->Branch("emtf_xml_pt", &emtf_xml_pt);
    tOut->Branch("emtf_eta",    &emtf_eta);
    tOut->Branch("emtf_theta",  &emtf_theta);
    tOut->Branch("emtf_phi",    &emtf_phi);
    tOut->Branch("emtf_charge", &emtf_charge);
    tOut->Branch("emtf_mode",   &emtf_mode);
    tOut->Branch("emtf_mult",   &emtf_mult);  // how many valid trk were found in the event;

    tOut->Branch("has_S1",   &has_S1);
    tOut->Branch("S1_type",  &S1_type);
    tOut->Branch("S1_phi",   &S1_phi);
    tOut->Branch("S1_eta",   &S1_eta);
    tOut->Branch("S1_theta", &S1_theta);

    tOut->Branch("has_S2",   &has_S2);
    tOut->Branch("S2_type",  &S2_type);
    tOut->Branch("S2_phi",   &S2_phi);
    tOut->Branch("S2_eta",   &S2_eta);
    tOut->Branch("S2_theta", &S2_theta);

    tOut->Branch("has_S3",   &has_S3);
    tOut->Branch("S3_type",  &S3_type);
    tOut->Branch("S3_phi",   &S3_phi);
    tOut->Branch("S3_eta",   &S3_eta);
    tOut->Branch("S3_theta", &S3_theta);

    tOut->Branch("has_S4",   &has_S4);
    tOut->Branch("S4_type",  &S4_type);
    tOut->Branch("S4_phi",   &S4_phi);
    tOut->Branch("S4_eta",   &S4_eta);
    tOut->Branch("S4_theta", &S4_theta);


    /////////////////////////////////////////////////////////////////////


    int appd = appendFromFileList (ch, filelist);
    cout << "... read out " << appd << " files" << endl;

    //////////////////////////////

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

    // TFile* fIn_theta = TFile::Open ();
    // TFile* fIn_phi   = TFile::Open ();
    // TFile* fIn_theta = TFile::Open ("correlator_data/matching_windows_theta_q99.root");
    // TFile* fIn_phi   = TFile::Open ("correlator_data/matching_windows_phi_q99.root");
    TFile* fIn_theta = TFile::Open (fIn_theta_name.c_str());
    TFile* fIn_phi   = TFile::Open (fIn_phi_name.c_str());
    Correlator corr (bounds, fIn_theta, fIn_phi);
    corr.set_safety_factor(sftor);
    // corr.set_sf_initialrelax(sftor_initial, 0.0);
    // corr.set_sf_initialrelax(0.0, sftor_initial);
    corr.set_sf_initialrelax(sftor_initial);
    corr.set_do_relax_factor(doRelax);
    fIn_theta->Close();
    fIn_phi->Close();

    Correlator_L1TTgroup_impl corrL1TT_impl;

    //////////////////////////////

    for (uint iEv = 0; true; ++iEv)
    {
        if (!mtkt.Next()) break;

        if (maxEvts > -1 && iEv > maxEvts)
            break;

        if (iEv % 10000 == 0 || DEBUG)
            cout << "... processing " << iEv << endl;

        // dumpGenMu(mtkt);

        // auto  bhits = findBestHits (mtkt);
        // cout << bhits.first.nCSC << " " << bhits.second.nCSC << endl;

        // filter out events with >=2 mus in an endcap, or with no muons in both endcaps (for Zmumu)
        if (!single_mu_in_endcap(mtkt))
            continue;

        // ------------- correlator ---------------

        std::vector<int> n_arb_corr;
        auto corr_mu_idxs = corr.find_match(mtkt, &n_arb_corr); // for each trk, the emtfmu that matches
        // // split in the two endcaps to assing to the gen mu
        std::vector<std::tuple<float, int, int>> corr_mu_pos; // trk pt, trk idx, emtf idx
        std::vector<std::tuple<float, int, int>> corr_mu_neg; // trk pt, trk idx, emtf idx
        for (uint itrk = 0; itrk < corr_mu_idxs.size(); ++itrk)            
        {
            int iemtf = corr_mu_idxs.at(itrk);
            if (iemtf < 0) continue; // not a matched mu
            float m_trk_pt  = mtkt.L1TT_trk_pt.At(itrk);
            float m_trk_eta = mtkt.L1TT_trk_eta.At(itrk);
            if (m_trk_eta > 0)
                corr_mu_pos.push_back(make_tuple(m_trk_pt, itrk, iemtf));
            else
                corr_mu_neg.push_back(make_tuple(m_trk_pt, itrk, iemtf));
        }
        
        sort(corr_mu_pos.begin(), corr_mu_pos.end());
        sort(corr_mu_neg.begin(), corr_mu_neg.end());

        // ------------------------------------------

        // ------------- the CMSSW correlator in my implementation ---------------

        std::vector<int> n_arb_mycorr;
        auto mycorr_mu_idxs = corrL1TT_impl.find_match(mtkt, &n_arb_mycorr); // for each trk, the emtfmu that matches
        // // split in the two endcaps to assing to the gen mu
        std::vector<std::tuple<float, int, int>> mycorr_mu_pos; // trk pt, trk idx, emtf idx
        std::vector<std::tuple<float, int, int>> mycorr_mu_neg; // trk pt, trk idx, emtf idx
        for (uint itrk = 0; itrk < mycorr_mu_idxs.size(); ++itrk)            
        {
            int iemtf = mycorr_mu_idxs.at(itrk);
            if (iemtf < 0) continue; // not a matched mu
            float m_trk_pt  = mtkt.L1TT_trk_pt.At(itrk);
            float m_trk_eta = mtkt.L1TT_trk_eta.At(itrk);
            if (m_trk_eta > 0)
                mycorr_mu_pos.push_back(make_tuple(m_trk_pt, itrk, iemtf));
            else
                mycorr_mu_neg.push_back(make_tuple(m_trk_pt, itrk, iemtf));
        }
        
        sort(mycorr_mu_pos.begin(), mycorr_mu_pos.end());
        sort(mycorr_mu_neg.begin(), mycorr_mu_neg.end());


        // // good, this never happens
        // if (mycorr_mu_pos.size() + mycorr_mu_neg.size() > *(mtkt.n_EMTF_mu))
        //     cout << "I do not understand "
        //          << mycorr_mu_pos.size() << " + "
        //          << mycorr_mu_neg.size()
        //          << " =? " << count_if(mycorr_mu_idxs.begin(), mycorr_mu_idxs.end(), [](int i){return i >= 0;})
        //          << " > "  <<  *(mtkt.n_EMTF_mu)
        //          << endl;

        // ------------------------------------------

        // // I rarely get 4 gen muons instead of 2 in Zmumu (PU200)
        // // but tney really seem not to be clones between them (maybe muons from gamma->mumu radiation?)
        // // not an issue anyway
        // if (*(mtkt.n_gen_mu) != 2){
        //     cout << "not 2 gen mus ?? " << *(mtkt.n_gen_mu) << endl;
        //     dumpGenMu(mtkt);
        // }

        // loop on gen muons
        for (uint igm = 0; igm < *(mtkt.n_gen_mu); ++igm)
        {
            float eta = mtkt.gen_mu_eta.At(igm);
            float aeta = std::abs(eta);
            if (aeta < fiducial_eta_min || aeta > fiducial_eta_max)
                continue;

            gen_pt     = mtkt.gen_mu_pt.At(igm);
            gen_eta    = mtkt.gen_mu_eta.At(igm);
            gen_theta  = to_mpio2_pio2(eta_to_theta(mtkt.gen_mu_eta.At(igm)));
            gen_phi    = mtkt.gen_mu_phi.At(igm);
            gen_charge = mtkt.gen_mu_charge.At(igm);

            // pick up closest for trk muons and trks, but not fOr EMTF where mutliplicity is much smaller and highest pT is a good choice
            auto best_emtf  = findBest(gen_eta, gen_phi, mtkt.EMTF_mu_pt,  mtkt.EMTF_mu_eta,  mtkt.EMTF_mu_phi,  true, dRmax, false, false); // no eta cuts for the emtf (scattering is large)
            auto best_trk   = findBest(gen_eta, gen_phi, mtkt.L1TT_trk_pt, mtkt.L1TT_trk_eta, mtkt.L1TT_trk_phi, false, dRmax, true, true);
            auto best_tkmu  = findBest(gen_eta, gen_phi, mtkt.L1_TkMu_pt,  mtkt.L1_TkMu_eta,  mtkt.L1_TkMu_phi,  false, dRmax, true, true);

            int ibest_emtf = best_emtf.first;
            int ibest_trk  = best_trk.first;
            int ibest_tkmu = best_tkmu.first;

            int ibest_upgtkmu = -1;
            if (gen_eta > 0 && corr_mu_pos.size() > 0)
                ibest_upgtkmu = get<1>(corr_mu_pos.back()); // get idx of track
            if (gen_eta < 0 && corr_mu_neg.size() > 0)
                ibest_upgtkmu = get<1>(corr_mu_neg.back()); // get idx of track

            int ibest_myimpltkmu = -1;
            if (gen_eta > 0 && mycorr_mu_pos.size() > 0)
                ibest_myimpltkmu = get<1>(mycorr_mu_pos.back()); // get idx of track
            if (gen_eta < 0 && mycorr_mu_neg.size() > 0)
                ibest_myimpltkmu = get<1>(mycorr_mu_neg.back()); // get idx of track



            int nbest_emtf    = best_emtf.second;
            int nbest_trk     = best_trk.second;
            int nbest_tkmu    = best_tkmu.second;
            int nbest_upgtkmu    = (gen_eta > 0 ? corr_mu_pos.size()   : corr_mu_neg.size());
            int nbest_myimpltkmu = (gen_eta > 0 ? mycorr_mu_pos.size() : mycorr_mu_neg.size());

            // if (DEBUG && nbest_myimpltkmu > nbest_emtf){
            //     cout << "Do not understand : " << nbest_myimpltkmu << " " << nbest_emtf << " etagen " << gen_eta << endl;
            //     cout << " POS side " << mycorr_mu_pos.size() << endl;
            //     cout << " NEG side " << mycorr_mu_neg.size() << endl;
            //     cout << "TOT emtf  " << *(mtkt.n_EMTF_mu) << endl;
            //     dumpEMTF(mtkt);
            //     cout << endl;
            // }

            emtf_pt     = ( ibest_emtf >= 0 ? mtkt.EMTF_mu_pt.At(ibest_emtf)                               : -999.);
            emtf_xml_pt = ( ibest_emtf >= 0 ? mtkt.EMTF_mu_pt_xml.At(ibest_emtf)                           : -999.);
            emtf_eta    = ( ibest_emtf >= 0 ? mtkt.EMTF_mu_eta.At(ibest_emtf)                              : -999.);
            emtf_theta  = ( ibest_emtf >= 0 ? to_mpio2_pio2(eta_to_theta(mtkt.EMTF_mu_eta.At(ibest_emtf))) : -999.);
            emtf_phi    = ( ibest_emtf >= 0 ? deg_to_rad(mtkt.EMTF_mu_phi.At(ibest_emtf))                  : -999.);
            emtf_charge = ( ibest_emtf >= 0 ? mtkt.EMTF_mu_charge.At(ibest_emtf)                           : -999);
            emtf_mode   = ( ibest_emtf >= 0 ? mtkt.EMTF_mu_mode.At(ibest_emtf)                             : -999.);
            emtf_mult   = nbest_emtf;

            trk_pt      = ( ibest_trk >= 0 ? mtkt.L1TT_trk_pt.At(ibest_trk)                                 : -999.);
            trk_eta     = ( ibest_trk >= 0 ? mtkt.L1TT_trk_eta.At(ibest_trk)                                : -999.);
            trk_theta   = ( ibest_trk >= 0 ? to_mpio2_pio2(eta_to_theta(mtkt.L1TT_trk_eta.At(ibest_trk)))   : -999.);
            trk_phi     = ( ibest_trk >= 0 ? mtkt.L1TT_trk_phi.At(ibest_trk)                                : -999.);
            trk_chi2    = ( ibest_trk >= 0 ? mtkt.L1TT_trk_chi2.At(ibest_trk)                               : -999.);
            trk_nstubs  = ( ibest_trk >= 0 ? mtkt.L1TT_trk_nstubs.At(ibest_trk)                             : -999);
            trk_charge  = ( ibest_trk >= 0 ? mtkt.L1TT_trk_charge.At(ibest_trk)                             : -999);
            trk_mult    = nbest_trk;

            tkmu_pt      = ( ibest_tkmu >= 0 ? mtkt.L1_TkMu_pt.At(ibest_tkmu)                                 : -999.);
            tkmu_eta     = ( ibest_tkmu >= 0 ? mtkt.L1_TkMu_eta.At(ibest_tkmu)                                : -999.);
            tkmu_theta   = ( ibest_tkmu >= 0 ? to_mpio2_pio2(eta_to_theta(mtkt.L1_TkMu_eta.At(ibest_tkmu)))   : -999.);
            tkmu_phi     = ( ibest_tkmu >= 0 ? mtkt.L1_TkMu_phi.At(ibest_tkmu)                                : -999.);
            // tkmu_charge  = ( ibest_tkmu >= 0 ? mtkt.L1_TkMu_charge.At(ibest_tkmu)                             : -999);
            tkmu_mult    = nbest_tkmu;

            // cout << " ... this  gen mu has pt : " <<  gen_pt << " eta : " << gen_eta << " phi : " << gen_phi << endl;
            // cout << " ... chosen tk mu has pt : " <<  tkmu_pt << " eta : " << tkmu_eta << " phi : " << tkmu_phi << endl;

            // will simply pick the properties from the L1T tracks
            upgtkmu_pt      = ( ibest_upgtkmu >= 0 ? mtkt.L1TT_trk_pt.At(ibest_upgtkmu)                                 : -999.);
            upgtkmu_eta     = ( ibest_upgtkmu >= 0 ? mtkt.L1TT_trk_eta.At(ibest_upgtkmu)                                : -999.);
            upgtkmu_theta   = ( ibest_upgtkmu >= 0 ? to_mpio2_pio2(eta_to_theta(mtkt.L1TT_trk_eta.At(ibest_upgtkmu)))   : -999.);
            upgtkmu_phi     = ( ibest_upgtkmu >= 0 ? mtkt.L1TT_trk_phi.At(ibest_upgtkmu)                                : -999.);
            upgtkmu_mult    = nbest_upgtkmu;
            upgtkmu_narb    = ( ibest_upgtkmu >= 0 ? n_arb_corr.at(ibest_upgtkmu) : 0);

            // will simply pick the properties from the L1T tracks
            myimpltkmu_pt      = ( ibest_myimpltkmu >= 0 ? mtkt.L1TT_trk_pt.At(ibest_myimpltkmu)                                 : -999.);
            myimpltkmu_eta     = ( ibest_myimpltkmu >= 0 ? mtkt.L1TT_trk_eta.At(ibest_myimpltkmu)                                : -999.);
            myimpltkmu_theta   = ( ibest_myimpltkmu >= 0 ? to_mpio2_pio2(eta_to_theta(mtkt.L1TT_trk_eta.At(ibest_myimpltkmu)))   : -999.);
            myimpltkmu_phi     = ( ibest_myimpltkmu >= 0 ? mtkt.L1TT_trk_phi.At(ibest_myimpltkmu)                                : -999.);
            myimpltkmu_mult    = nbest_myimpltkmu;
            myimpltkmu_narb    = ( ibest_myimpltkmu >= 0 ? n_arb_mycorr.at(ibest_myimpltkmu) : 0);

            // fill below if there is an EMTF and it has the hit in S1 / S2 / S3 / S4
            int ihitS1 = (ibest_emtf >= 0 ? mtkt.EMTF_mu_hitref1.At(ibest_emtf)                      : -1);
            has_S1   = ( ihitS1 >= 0 ? true                                                          : false);
            S1_type  = ( ihitS1 >= 0 ? mtkt.mu_hit_type.At(ihitS1)                                   : -1);
            S1_phi   = ( ihitS1 >= 0 ? deg_to_rad(mtkt.mu_hit_sim_phi.At(ihitS1))                    : -999.);
            S1_eta   = ( ihitS1 >= 0 ? mtkt.mu_hit_sim_eta.At(ihitS1)                                : -999.);
            S1_theta = ( ihitS1 >= 0 ? to_mpio2_pio2(deg_to_rad(mtkt.mu_hit_sim_theta.At(ihitS1)))   : -999.);

            int ihitS2 = (ibest_emtf >= 0 ? mtkt.EMTF_mu_hitref2.At(ibest_emtf)                      : -1);
            has_S2   = ( ihitS2 >= 0 ? true                                                          : false);
            S2_type  = ( ihitS2 >= 0 ? mtkt.mu_hit_type.At(ihitS2)                                   : -1);
            S2_phi   = ( ihitS2 >= 0 ? deg_to_rad(mtkt.mu_hit_sim_phi.At(ihitS2))                    : -999.);
            S2_eta   = ( ihitS2 >= 0 ? mtkt.mu_hit_sim_eta.At(ihitS2)                                : -999.);
            S2_theta = ( ihitS2 >= 0 ? to_mpio2_pio2(deg_to_rad(mtkt.mu_hit_sim_theta.At(ihitS2)))   : -999.);

            int ihitS3 = (ibest_emtf >= 0 ? mtkt.EMTF_mu_hitref3.At(ibest_emtf)                      : -1);
            has_S3   = ( ihitS3 >= 0 ? true                                                          : false);
            S3_type  = ( ihitS3 >= 0 ? mtkt.mu_hit_type.At(ihitS3)                                   : -1);
            S3_phi   = ( ihitS3 >= 0 ? deg_to_rad(mtkt.mu_hit_sim_phi.At(ihitS3))                    : -999.);
            S3_eta   = ( ihitS3 >= 0 ? mtkt.mu_hit_sim_eta.At(ihitS3)                                : -999.);
            S3_theta = ( ihitS3 >= 0 ? to_mpio2_pio2(deg_to_rad(mtkt.mu_hit_sim_theta.At(ihitS3)))   : -999.);

            int ihitS4 = (ibest_emtf >= 0 ? mtkt.EMTF_mu_hitref4.At(ibest_emtf)                      : -1);
            has_S4   = ( ihitS4 >= 0 ? true                                                          : false);
            S4_type  = ( ihitS4 >= 0 ? mtkt.mu_hit_type.At(ihitS4)                                   : -1);
            S4_phi   = ( ihitS4 >= 0 ? deg_to_rad(mtkt.mu_hit_sim_phi.At(ihitS4))                    : -999.);
            S4_eta   = ( ihitS4 >= 0 ? mtkt.mu_hit_sim_eta.At(ihitS4)                                : -999.);
            S4_theta = ( ihitS4 >= 0 ? to_mpio2_pio2(deg_to_rad(mtkt.mu_hit_sim_theta.At(ihitS4)))   : -999.);

            // cout << " my CMSSW impl : " << myimpltkmu_narb << " my algo : " <<  upgtkmu_narb << endl;

            // debug
            // if (S2_eta < 0 && emtf_eta > 0 && has_S2 && (emtf_mode &  (1 << 2))) // check mode to ensure I have something in S2 --> determines position
            // {
            //     cout << "What ?? S2_eta/phi : " << S2_eta << " " << S2_phi << " EMTF eta/phi" << emtf_eta << " " << emtf_phi << endl;
            //     dumpHits(mtkt);
            // }

            /*
            if (gen_eta > 0)
            {
                cout << " pt : " << gen_pt << "  eta : " << gen_eta << " phi : " << gen_phi << endl; 
                if (ibest_emtf >= 0)
                {
                    int ih1 = mtkt.EMTF_mu_hitref1.At(ibest_emtf);
                    cout << " ====> CHOSEN HIT , E POS" << endl;
                    if (ih1 >= 0)
                    {
                        cout << "   endcap : "    <<  mtkt.mu_hit_endcap.At(ih1)
                             << "   station : "   <<  mtkt.mu_hit_station.At(ih1)
                             << "   ring : "      <<  mtkt.mu_hit_ring.At(ih1)
                             << "   sector : "    <<  mtkt.mu_hit_sector.At(ih1)
                             << "   subsector : " <<  mtkt.mu_hit_subsector.At(ih1)
                             << "   chamber : "   <<  mtkt.mu_hit_chamber.At(ih1)
                             << "   cscid : "     <<  mtkt.mu_hit_cscid.At(ih1)
                             << "   bx : "        <<  mtkt.mu_hit_bx.At(ih1)
                             << "   type : "      <<  mtkt.mu_hit_type.At(ih1)
                             << "   neighbor : "  <<  mtkt.mu_hit_neighbor.At(ih1)
                             << "   sim_phi : "   <<  mtkt.mu_hit_sim_phi.At(ih1)
                             << "   sim_theta : " <<  mtkt.mu_hit_sim_theta.At(ih1)
                             << "   sim_eta : "   <<  mtkt.mu_hit_sim_eta.At(ih1)
                             << endl;
                    }
                    else
                        cout << " .... NONE ... " << endl;
                }
                else{
                    int nemtf = 0;
                    for (uint ie = 0; ie < *(mtkt.n_EMTF_mu); ++ie)
                    {
                        if (mtkt.EMTF_mu_eta.At(ie) > 0)
                            ++nemtf;
                    }
                    cout << " ====> NO EMTF DONE " << nemtf << endl;
                }
            }
            */
 

            tOut->Fill();


        }


        // dumpGenMu(mtkt);
        // // dumpTracks(mtkt);
        // dumpEMTF(mtkt);
        // dumpTkMu(mtkt);
        // dumpUpgTkMu(mtkt, corr_mu_idxs);
        // cout << endl << " ============================ " << endl;

        // if (debugHitRefs(mtkt))
        //     cout << " ==> something bad in evt " << iEv << endl << endl << endl;

        // looks like there is a fraction of the events (4 / 500k) that has tracks with pt > 10^6 GeV
        // for (uint itrk = 0; itrk < *n_L1TT_trk; ++itrk)
        //     if (L1TT_trk_pt.At(itrk) > 1000000)
        //         cout << "Track " << L1TT_trk_pt.At(itrk) << " " << L1TT_trk_eta.At(itrk) << " " << L1TT_trk_phi.At(itrk) << endl;

        // cout << " ----------- END EVENT ----------- " << endl;
    }

    fOut->cd();
    tOut->Write();
    fOut->Close();

}
#include <iostream>
#include <string>
#include <utility>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include "TTree.h"
#include "TMath.h"
#include "TChain.h"
#include "TFile.h"

#include "MuTkTree.h"

#include <boost/accumulators/accumulators.hpp>
#include <boost/accumulators/statistics/stats.hpp>

using namespace std;
using namespace boost::accumulators; // for mean and std

// c++ -lm -o makeMatchedTree makeMatchedTree.cpp `root-config --glibs --cflags` -lTreePlayer

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

// return pair of idx best (first) amnd num possible cands (second)
std::pair<int, int> findBest(float eta_tm, TTreeReaderArray<float>& pts, TTreeReaderArray<float>& etas)
{
    std::vector<pair<float, int>> vGood;
    for (uint ic = 0; ic < pts.GetSize(); ++ic)
    {
        if ( eta_tm * etas.At(ic) < 0.0) // opposite endcap
            continue; // reject those that are in opposite hemispheres
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

int main()
{
    string filelist = "filelist/MuMu_flatPt_0PU_12Apr2018_hitinfo_fix.txt";
    string outputname = "matched_tree_MuMu_flatPt_0PU_12Apr2018_hitinfo.root";

    /////////////////////////////////////////////////////////////////////

    // to select gen muons
    float fiducial_eta_min = 1.2;
    float fiducial_eta_max = 2.4;

    /////////////////////////////////////////////////////////////////////


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
    int    trk_mult;
    // double trk_z;
    double emtf_pt;
    double emtf_xml_pt;
    double emtf_eta;
    double emtf_theta;
    double emtf_phi;
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
    
    tOut->Branch("trk_pt",    &trk_pt);
    tOut->Branch("trk_eta",   &trk_eta);
    tOut->Branch("trk_theta", &trk_theta);
    tOut->Branch("trk_phi",   &trk_phi);
    tOut->Branch("trk_mult",  &trk_mult); // how many valid trk were found in the event;
    // tOut->Branch("trk_z", &trk_z);

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

    for (uint iEv = 0; true; ++iEv)
    {
        if (!mtkt.Next()) break;

        if (iEv % 10000 == 0)
            cout << "... processing " << iEv << endl;

        // auto  bhits = findBestHits (mtkt);
        // cout << bhits.first.nCSC << " " << bhits.second.nCSC << endl;

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
            // gen_charge = mtkt.gen_mu_charge.At(igm); // FIXME
            gen_charge = -999;

            auto best_emtf = findBest(eta, mtkt.EMTF_mu_pt, mtkt.EMTF_mu_eta);
            auto best_trk  = findBest(eta, mtkt.L1TT_trk_pt, mtkt.L1TT_trk_eta);

            int ibest_emtf = best_emtf.first;
            int ibest_trk = best_trk.first;

            int nbest_emtf = best_emtf.second;
            int nbest_trk = best_trk.second;

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
            trk_mult    = nbest_trk;

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
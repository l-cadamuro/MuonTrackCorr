#include <string>
#include <iostream>
#include <vector>
#include <memory>
#include <algorithm>
#include "TH1D.h"
#include "TH1F.h"
#include "TFile.h"


class RateCalculator{
    public:
        RateCalculator(std::string name, std::string title = "");
        ~RateCalculator(){};
        void feedPt(float pt) {v_pt_.push_back(pt);};  // update with a valid muon candidate
        void process(); // process the muons received and update internal histos - to be called once for each event!
        void setStyle  (int color);
        bool makeRatePlot();
        TH1D* getRatePlot(){return h_singlemu_rate_.get();}
        void saveToFile(TFile* fOut);

        std::string           name_;
        std::vector<float>    v_pt_;           // per-event selected muons pt
        std::unique_ptr<TH1D> h_leading_pt_;    // the histogram of the leading pt muon
        std::unique_ptr<TH1D> h_singlemu_rate_; // only created when making rate!
};


RateCalculator::RateCalculator(std::string name, std::string title)
{
    name_ = name;
    std::string the_title = (title.empty() ? name_ : title);
    title = title + ";Highest muon p_{T} [GeV]; Events";
    h_leading_pt_ = std::unique_ptr<TH1D>(new TH1D(Form("%s_lead_mu_pt", name_.c_str()) , title.c_str(), 200, 0, 100));
    v_pt_.clear();
}

void RateCalculator::process()
{
        std::sort(v_pt_.begin(), v_pt_.end());
        h_leading_pt_->Fill( v_pt_.size() > 0 ? v_pt_.back() : -1); // fill witih highest pt, else underflow
        v_pt_.clear(); // get ready for a new event
        return;
}


bool RateCalculator::makeRatePlot()
{
    if (h_singlemu_rate_)
    {
        std::cout << "** ERROR: RateCalculator: cannot make rate for " << name_ << " , plot already exists, skipping..." << std::endl;
        return false;
    }

    h_singlemu_rate_ = std::unique_ptr<TH1D>(new TH1D(
        (std::string("rate_")+std::string(h_leading_pt_->GetName())).c_str(),
        (std::string("Rate ")+std::string(h_leading_pt_->GetTitle())).c_str(),
        h_leading_pt_->GetNbinsX(),
        h_leading_pt_->GetBinLowEdge(1),
        h_leading_pt_->GetBinLowEdge(h_leading_pt_->GetNbinsX()+1)
    ));
    h_singlemu_rate_->GetXaxis()->SetTitle(h_leading_pt_->GetXaxis()->GetTitle());
    h_singlemu_rate_->GetYaxis()->SetTitle("Rate reduction");

    // copy style
    h_singlemu_rate_->SetLineColor  (h_leading_pt_->GetLineColor());
    h_singlemu_rate_->SetLineWidth  (h_leading_pt_->GetLineWidth());
    h_singlemu_rate_->SetMarkerColor(h_leading_pt_->GetMarkerColor());
    h_singlemu_rate_->SetMarkerStyle(h_leading_pt_->GetMarkerStyle());

    /// fixme: can be set as a tgraoherrors to get errors
    double tot_entries = h_leading_pt_->Integral(-1, -1);
    if (tot_entries != double(h_leading_pt_->GetEntries()))
        std::cout << "** ERROR: RateCalculator: entries and integral do not match " << std::endl;
    
    std::cout << name_ << " " << tot_entries << " " << h_leading_pt_->GetEntries() << std::endl;

    if (tot_entries != 0)
    {
        for (uint ibin = 1; ibin < h_leading_pt_->GetNbinsX()+1; ++ibin)
        {
            double this_integral = h_leading_pt_->Integral(ibin, -1);
            double rate_red = this_integral/tot_entries;
            h_singlemu_rate_->SetBinContent(ibin, rate_red);
        }
    }
    return true;
}

void RateCalculator::setStyle (int color)
{
    h_leading_pt_->SetLineColor(color);
    h_leading_pt_->SetLineWidth(2);
    
    if (h_singlemu_rate_){
        h_singlemu_rate_->SetLineColor(color);
        h_singlemu_rate_->SetLineWidth(2);
    }
    return;

}

void RateCalculator::saveToFile(TFile* fOut)
{
    fOut->cd();
    h_leading_pt_->Write();
    h_singlemu_rate_->Write();
}

// take the TF1 that are an input to the correlator implementation
// and create new files with the x and y axes discretized

#include <math.h>

// this is a bit of a crude solution, but works fine and is fast
double roundUp(double numToRound, double precision)
{
    bool is_neg = (numToRound < 0);
    
    // work with pos numbers only
    if (is_neg)
        numToRound *= -1;

    // start the search from the division rounded down
    double psum = floor(numToRound/precision)*precision - 2*precision;
    double old  = psum;
    // cout << "PSUM " << psum << " OLD = " << old << " target = " << numToRound << " precision = " << precision << endl;
    double result;
    while (true)
    {
        psum += precision;
        // cout << "TARGET = " << numToRound << "  PREC = " << precision << " old = " << old << " psum  = " << psum << endl;
        if (old < numToRound && psum >= numToRound)
        {
            double dold  = TMath::Abs(old - numToRound);
            double dpsum = TMath::Abs(psum - numToRound);
            if (dold < dpsum)
                result = old;
            else
                result = psum;
            break;
        }
        old = psum;
    }

    if (is_neg)
        result *= -1; // back again with sign

    // cout << "TARGET = " << numToRound << "  PREC = " << precision << " GET  = " << result << endl;
    return result;
}

// this will just concatenate if values to build the TF1
// if a quantization > 0 is passed, the output is rounded to the closest value that is multiple of quantization
TString generate_str_TH1_to_TF1(TH1* hIn, double quantization = -1)
{
    TString res = "";
    TString buff_l;
    TString buff_h;
    TString buff_val;
    double val;

    // the underflow
    buff_l = TString("");
    buff_l += hIn->GetBinLowEdge(1);
    val = hIn->GetBinContent(1);
    if (quantization > 0)
        val = roundUp(val, quantization);


    buff_val = TString("");
    buff_val += val;
    res += Form("(x < %s)*%s + ", buff_l.Data(), buff_val.Data());
    
    // cout << " >>> " << buff_l << " " << buff_h << " " << buff_val << " --- " << hIn->GetBinLowEdge(1) << " " << hIn->GetBinContent(1) << endl;

    for (uint ibin = 1; ibin <= hIn->GetNbinsX(); ++ibin)
    {
        buff_l   = TString("");
        buff_l   += hIn->GetBinLowEdge(ibin);
        buff_h   = TString("");
        buff_h   += hIn->GetBinLowEdge(ibin+1);
        val = hIn->GetBinContent(ibin);
        if (quantization > 0)
            val = roundUp(val, quantization);
        buff_val = TString("");
        buff_val += val;

        res += Form("(x >= %s && x < %s)*%s + ", buff_l.Data(), buff_h.Data(), buff_val.Data());
    }

    // the overflow
    buff_l = TString("");
    buff_l += hIn->GetBinLowEdge(hIn->GetNbinsX()+1);
    val = hIn->GetBinContent(hIn->GetNbinsX());
    if (quantization > 0)
        val = roundUp(val, quantization);
    buff_val = TString("");
    buff_val += val;
    res += Form("(x >= %s)*%s", buff_l.Data(), buff_val.Data());

    return res;
}

TF1* TH1_to_TF1 (TH1* hIn, TString new_name, double quantization = -1)
{
    TString expr = generate_str_TH1_to_TF1(hIn, quantization);
    TF1* f_after_binning = new TF1(new_name, expr, hIn->GetBinLowEdge(1), hIn->GetBinLowEdge(hIn->GetNbinsX()+1));
    // cout << expr << endl;
    return f_after_binning;
}

TH1D* TF1_to_TH1 (TF1* fIn, TString name, int nbins, double xlow, double xhigh)
{

    // build an histogram out of TF1
    TH1D* h_from_fIn = new TH1D(name, name, nbins, xlow, xhigh);
    h_from_fIn->SetDirectory(0);
    for (uint ibin = 1; ibin <= h_from_fIn->GetNbinsX(); ++ibin)
    {
        double bc = h_from_fIn->GetBinCenter(ibin);
        // cout << ibin << " " << bc << endl;
        h_from_fIn->SetBinContent(ibin, fIn->Eval(bc));
    }
    return h_from_fIn;
}

TF1* quantize (TF1* fIn, double precision_x, double precision_y)
{
    cout << "Making " << fIn->GetName() << " deltaX = " << precision_x << " deltaY = " << precision_y << endl; 

    double xmin, xmax;
    fIn->GetRange(xmin, xmax);

    // adjust xmax to fit in an exact number of steps
    xmax = roundUp(xmax-xmin, precision_x) + xmin;
    // just a check
    if ( fmod (xmax-xmin,precision_x) != 0)
        cout << "@@@ WARNING: something wrong with func " <<  fIn->GetName() << " after adjusting xmin, xmax to " << xmin << " , " << xmax << endl;
    int nbins = round((xmax-xmin)/precision_x);

    // make the histo
    auto h = TF1_to_TH1 (fIn, TString("h_") + fIn->GetName(), nbins, xmin, xmax);
    // cout << "+++++++ " << h->GetBinContent(3) << endl;
    auto f = TH1_to_TF1 (h, TString("quant_") + fIn->GetName(), precision_y);
    
    // for (uint i = 0; i < 100; ++i)
    //     cout << "@@@@ " << fIn->Eval(i) << " >>>> " << f->Eval(i) << endl;
    
    return f;
}

// root -l quantize_windows_TF1.C'("../correlator_data/matching_windows_phi_q90.root", "prova_quant.root", 10, 5)'
void quantize_windows_TF1(TString fileIn_name, TString fileOut_name, double precision_x = 1, double precision_y = 0.001)
{
    // correlator_data/matching_windows_phi_q90.root
    // correlator_data/matching_windows_theta_q90.root

    // open the input file
    TFile* fileIn = new TFile(fileIn_name);

    // create output
    TFile* fileOut = new TFile(fileOut_name, "recreate");

    // files contain 10 eta bins, fit_low_%i
    for (uint ibin = 1; ibin <= 10; ++ibin)
    {
        for (TString bname : {"low", "cent", "high"})
        {
            TString name = Form("fit_%s_%i", bname.Data(), ibin);
            TF1* fIn = (TF1*) fileIn->Get(name);
            TF1* fOut = quantize(fIn, precision_x, precision_y);
            // for (uint i = 0; i < 100; ++i)
            //     cout << fIn->Eval(i) << " >>>> " << fOut->Eval(i) << endl;

            // fOut->SetLineColor(kBlue);
            fileOut->cd();
            fOut->SetName(fIn->GetName());
            fOut->Write();
        }
    }

}
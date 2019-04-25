// makes TF1 fully  text, removing [i] parameters
// it's the only way to make multiplication work
TF1* deparametrize(TF1* in_f, TString name)
{
    TString expr = in_f->GetTitle();
    int npar = in_f->GetNpar();
    for (uint ip = 0; ip < npar; ++ip)
    {
        double pval = in_f->GetParameter(ip);
        TString spval = Form("%f", pval);
        expr.ReplaceAll(Form("[%i]", ip), spval);
    }

    double xmin, xmax;
    in_f->GetRange(xmin, xmax);
    TF1* out_f = new TF1(name, expr, xmin, xmax);
    return out_f;
}


void embed_relaxation(TString fileIn_name, TString fileOut_name, double xstart = 2, double xstop = 6, double ystart = 0, double ystop = 0.5)
{

    TF1* frlx_wp = new TF1("frlx_wp", "(x<[0])*[2] + (x>=[0] && x<[1])*([2] + (x-[0])*([3]-[2])/([1]-[0])) + (x>=[1])*[3]", 0, 200); // xlow -> 0, xup -> 1, ylow -> 2, yup -> 3
    frlx_wp->SetParameters(xstart, xstop, ystart, ystop);
    TF1* frlx = deparametrize(frlx_wp, "frlx");

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
            TF1* fOut;
            TF1* fBuf;

            double xmin, xmax;
            fIn->GetRange(xmin, xmax);

            TString bufname = Form("wdw_%s_%i", bname.Data(), ibin);

            if (bname == "low")
            {
                fBuf = deparametrize(fIn, bufname);
                fOut = new TF1(bufname + "_wrlx", Form("(1-frlx)*%s", bufname.Data()), xmin, xmax);
            }
            else if (bname == "cent")
            {
                // nothing to do here
                fOut = fIn;
            }
            else if (bname == "high")
            {
                fBuf = deparametrize(fIn, bufname);
                fOut = new TF1(bufname + "_wrlx", Form("(1+frlx)*%s", bufname.Data()), xmin, xmax);
            }

            // TF1* fOut = quantize(fIn, precision_x, precision_y);
            // for (uint i = 0; i < 100; ++i)
            //     cout << fIn->Eval(i) << " >>>> " << fOut->Eval(i) << endl;

            // fOut->SetLineColor(kBlue);
            fileOut->cd();
            fOut->SetName(fIn->GetName());
            fOut->Write();
        }
    }
}
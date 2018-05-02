#ifndef MATCHWINDOW_H
#define MATCHWINDOW_H

#include "TF1.h"
#include <string>
#include <memory>
#include <iostream>

/*
** class  : MatchWindod
** author : L.Cadamuro (UF)
** date   : 25/12/2018
** brief  : encodes the lower and upper bounds to match a track to a muon
**          to be flexible, limits are given as strings to create a TF1 function
*/

class MatchWindow
{
    public:
        MatchWindow();
        MatchWindow(std::string name);
        ~MatchWindow();
        void SetName(std::string name) {name_ = name;}
        void SetLower(std::string formula);
        void SetUpper(std::string formula);
        void SetLower(TF1* formula);
        void SetUpper(TF1* formula);
        
        // bool matches (double pt);
        double bound_low  (double pt) {return f_low->Eval(pt);}
        double bound_high (double pt) {return f_high->Eval(pt);}


    private:
        std::string name_;
        std::shared_ptr<TF1> f_low;
        std::shared_ptr<TF1> f_high;
};

MatchWindow::MatchWindow(){
    name_ = "";
}

MatchWindow::MatchWindow(std::string name){
    SetName(name);
}

MatchWindow::~MatchWindow(){

}

void MatchWindow::SetLower(std::string formula)
{
    // if (f_low)
    //     throw std::runtime_error("Cannot initialize twice f_low");
    // f_low = std::shared_ptr<TF1> (new TF1 ((name_ + std::string("low")).c_str(), formula.c_str(), 0, 1000));
    TF1 f ("tmp", formula.c_str(), 0, 1000);
    SetLower(&f);
}

void  MatchWindow::SetUpper(std::string formula)
{
    // if (f_high)
    //     throw std::runtime_error("Cannot initialize twice f_high");
    // f_high = std::shared_ptr<TF1> (new TF1 ((name_ + std::string("high")).c_str(), formula.c_str(), 0, 1000));
    TF1 f ("tmp", formula.c_str(), 0, 1000);
    SetUpper(&f);
}

void MatchWindow::SetLower(TF1* formula)
{
    if (f_low)
        throw std::runtime_error("Cannot initialize twice f_low");
    f_low = std::shared_ptr<TF1> ((TF1*) formula->Clone ((name_ + std::string("low")).c_str()));
}

void  MatchWindow::SetUpper(TF1* formula)
{
    if (f_high)
        throw std::runtime_error("Cannot initialize twice f_high");
    f_high = std::shared_ptr<TF1> ((TF1*) formula->Clone ((name_ + std::string("high")).c_str()));
}

#endif // MATCHWINDOW_H
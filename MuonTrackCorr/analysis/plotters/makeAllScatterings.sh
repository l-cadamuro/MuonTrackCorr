# DPHI_TITLE="q^{gen} #times (#varphi_{CSC hit} - #varphi_{gen}) - <q^{gen} #times (#varphi_{CSC hit} - #varphi_{gen})>"
DPHI_TITLE="q^{gen} #times (#varphi_{CSC hit} - #varphi_{gen}) - avg."

##### dphi scatter plots
### in ME1/1
python compare_scattering.py --cut "gen_pt > 5  && gen_pt < 7  && abs(gen_eta) > 1.4 && abs(gen_eta) < 1.6" --title "5 < p_{T}^{gen} < 7 GeV, 1.4 < |#eta^{gen}| < 1.6;${DPHI_TITLE}; a.u."   --shift --xmin -0.1 --xmax 0.1 --nbins 100 --oname "scattering/scat_dphi_pt_5_7_eta_1p4_1p6.pdf"   --input '../matched_tree_MuMu_OneOverPt_0PU_23Apr2018.root'
python compare_scattering.py --cut "gen_pt > 15 && gen_pt < 20 && abs(gen_eta) > 1.4 && abs(gen_eta) < 1.6" --title "15 < p_{T}^{gen} < 20 GeV, 1.4 < |#eta^{gen}| < 1.6;${DPHI_TITLE}; a.u." --shift --xmin -0.1 --xmax 0.1 --nbins 100 --oname "scattering/scat_dphi_pt_15_20_eta_1p4_1p6.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'
python compare_scattering.py --cut "gen_pt > 50 && gen_pt < 60 && abs(gen_eta) > 1.4 && abs(gen_eta) < 1.6" --title "50 < p_{T}^{gen} < 60 GeV, 1.4 < |#eta^{gen}| < 1.6;${DPHI_TITLE}; a.u." --shift --xmin -0.1 --xmax 0.1 --nbins 100 --oname "scattering/scat_dphi_pt_50_60_eta_1p4_1p6.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'

### in ME1/2 1.7/1.9
python compare_scattering.py --cut "gen_pt > 5  && gen_pt < 7  && abs(gen_eta) > 1.7 && abs(gen_eta) < 1.9" --title "5 < p_{T}^{gen} < 7 GeV, 1.7 < |#eta^{gen}| < 1.9;${DPHI_TITLE}; a.u."   --shift --xmin -0.1 --xmax 0.1 --nbins 100 --oname "scattering/scat_dphi_pt_5_7_eta_1p7_1p9.pdf"   --input '../matched_tree_MuMu_OneOverPt_0PU_23Apr2018.root'
python compare_scattering.py --cut "gen_pt > 15 && gen_pt < 20 && abs(gen_eta) > 1.7 && abs(gen_eta) < 1.9" --title "15 < p_{T}^{gen} < 20 GeV, 1.7 < |#eta^{gen}| < 1.9;${DPHI_TITLE}; a.u." --shift --xmin -0.1 --xmax 0.1 --nbins 100 --oname "scattering/scat_dphi_pt_15_20_eta_1p7_1p9.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'
python compare_scattering.py --cut "gen_pt > 50 && gen_pt < 60 && abs(gen_eta) > 1.7 && abs(gen_eta) < 1.9" --title "50 < p_{T}^{gen} < 60 GeV, 1.7 < |#eta^{gen}| < 1.9;${DPHI_TITLE}; a.u." --shift --xmin -0.1 --xmax 0.1 --nbins 100 --oname "scattering/scat_dphi_pt_50_60_eta_1p7_1p9.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'

### in ME1/2 2.1/2.3
python compare_scattering.py --cut "gen_pt > 5  && gen_pt < 7  && abs(gen_eta) > 2.1 && abs(gen_eta) < 2.3" --title "5 < p_{T}^{gen} < 7 GeV, 2.1 < |#eta^{gen}| < 2.3;${DPHI_TITLE}; a.u."   --shift --xmin -0.1 --xmax 0.1 --nbins 100 --oname "scattering/scat_dphi_pt_5_7_eta_2p1_2p3.pdf"   --input '../matched_tree_MuMu_OneOverPt_0PU_23Apr2018.root'
python compare_scattering.py --cut "gen_pt > 15 && gen_pt < 20 && abs(gen_eta) > 2.1 && abs(gen_eta) < 2.3" --title "15 < p_{T}^{gen} < 20 GeV, 2.1 < |#eta^{gen}| < 2.3;${DPHI_TITLE}; a.u." --shift --xmin -0.1 --xmax 0.1 --nbins 100 --oname "scattering/scat_dphi_pt_15_20_eta_2p1_2p3.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'
python compare_scattering.py --cut "gen_pt > 50 && gen_pt < 60 && abs(gen_eta) > 2.1 && abs(gen_eta) < 2.3" --title "50 < p_{T}^{gen} < 60 GeV, 2.1 < |#eta^{gen}| < 2.3;${DPHI_TITLE}; a.u." --shift --xmin -0.1 --xmax 0.1 --nbins 100 --oname "scattering/scat_dphi_pt_50_60_eta_2p1_2p3.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'


# DTHETA_TITLE="#eta^{gen}/|#eta^{gen}| #times (#theta_{CSC hit} - #theta_{gen}) - <#eta^{gen}/|#eta^{gen}| #times (#theta_{CSC hit} - #theta_{gen})>"
DTHETA_TITLE="#eta^{gen}/|#eta^{gen}| #times (#theta_{CSC hit} - #theta_{gen}) - avg."

##### dphi scatter plots
### in ME1/1
python compare_scattering.py --cut "gen_pt > 5  && gen_pt < 7  && abs(gen_eta) > 1.4 && abs(gen_eta) < 1.6" --title "5 < p_{T}^{gen} < 7 GeV, 1.4 < |#eta^{gen}| < 1.6;${DTHETA_TITLE}; a.u."   --shift --xmin -0.05 --xmax 0.05 --nbins 100 --oname "scattering/scat_dtheta_pt_5_7_eta_1p4_1p6.pdf"   --input '../matched_tree_MuMu_OneOverPt_0PU_23Apr2018.root' --dtheta
python compare_scattering.py --cut "gen_pt > 15 && gen_pt < 20 && abs(gen_eta) > 1.4 && abs(gen_eta) < 1.6" --title "15 < p_{T}^{gen} < 20 GeV, 1.4 < |#eta^{gen}| < 1.6;${DTHETA_TITLE}; a.u." --shift --xmin -0.05 --xmax 0.05 --nbins 100 --oname "scattering/scat_dtheta_pt_15_20_eta_1p4_1p6.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'    --dtheta
python compare_scattering.py --cut "gen_pt > 50 && gen_pt < 60 && abs(gen_eta) > 1.4 && abs(gen_eta) < 1.6" --title "50 < p_{T}^{gen} < 60 GeV, 1.4 < |#eta^{gen}| < 1.6;${DTHETA_TITLE}; a.u." --shift --xmin -0.05 --xmax 0.05 --nbins 100 --oname "scattering/scat_dtheta_pt_50_60_eta_1p4_1p6.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'    --dtheta

### in ME1/2 1.7/1.9
python compare_scattering.py --cut "gen_pt > 5  && gen_pt < 7  && abs(gen_eta) > 1.7 && abs(gen_eta) < 1.9" --title "5 < p_{T}^{gen} < 7 GeV, 1.7 < |#eta^{gen}| < 1.9;${DTHETA_TITLE}; a.u."   --shift --xmin -0.05 --xmax 0.05 --nbins 100 --oname "scattering/scat_dtheta_pt_5_7_eta_1p7_1p9.pdf"   --input '../matched_tree_MuMu_OneOverPt_0PU_23Apr2018.root' --dtheta
python compare_scattering.py --cut "gen_pt > 15 && gen_pt < 20 && abs(gen_eta) > 1.7 && abs(gen_eta) < 1.9" --title "15 < p_{T}^{gen} < 20 GeV, 1.7 < |#eta^{gen}| < 1.9;${DTHETA_TITLE}; a.u." --shift --xmin -0.05 --xmax 0.05 --nbins 100 --oname "scattering/scat_dtheta_pt_15_20_eta_1p7_1p9.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'    --dtheta
python compare_scattering.py --cut "gen_pt > 50 && gen_pt < 60 && abs(gen_eta) > 1.7 && abs(gen_eta) < 1.9" --title "50 < p_{T}^{gen} < 60 GeV, 1.7 < |#eta^{gen}| < 1.9;${DTHETA_TITLE}; a.u." --shift --xmin -0.05 --xmax 0.05 --nbins 100 --oname "scattering/scat_dtheta_pt_50_60_eta_1p7_1p9.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'    --dtheta

### in ME1/2 2.1/2.3
python compare_scattering.py --cut "gen_pt > 5  && gen_pt < 7  && abs(gen_eta) > 2.1 && abs(gen_eta) < 2.3" --title "5 < p_{T}^{gen} < 7 GeV, 2.1 < |#eta^{gen}| < 2.3;${DTHETA_TITLE}; a.u."   --shift --xmin -0.05 --xmax 0.05 --nbins 100 --oname "scattering/scat_dtheta_pt_5_7_eta_2p1_2p3.pdf"   --input '../matched_tree_MuMu_OneOverPt_0PU_23Apr2018.root' --dtheta
python compare_scattering.py --cut "gen_pt > 15 && gen_pt < 20 && abs(gen_eta) > 2.1 && abs(gen_eta) < 2.3" --title "15 < p_{T}^{gen} < 20 GeV, 2.1 < |#eta^{gen}| < 2.3;${DTHETA_TITLE}; a.u." --shift --xmin -0.05 --xmax 0.05 --nbins 100 --oname "scattering/scat_dtheta_pt_15_20_eta_2p1_2p3.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'    --dtheta
python compare_scattering.py --cut "gen_pt > 50 && gen_pt < 60 && abs(gen_eta) > 2.1 && abs(gen_eta) < 2.3" --title "50 < p_{T}^{gen} < 60 GeV, 2.1 < |#eta^{gen}| < 2.3;${DTHETA_TITLE}; a.u." --shift --xmin -0.05 --xmax 0.05 --nbins 100 --oname "scattering/scat_dtheta_pt_50_60_eta_2p1_2p3.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'    --dtheta


### cross check
python compare_scattering.py --cut "gen_pt > 50 && gen_pt < 60 && abs(gen_eta) > 2.1 && abs(gen_eta) < 2.3" --title "50 < p_{T}^{gen} < 60 GeV, 2.1 < |#eta^{gen}| < 2.3;${DTHETA_TITLE}; a.u." --shift --xmin -0.02 --xmax 0.02 --nbins 100 --oname "scattering/scat_dtheta_pt_50_60_eta_2p1_2p3.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'    --dtheta
python compare_scattering.py --cut "gen_pt > 50 && gen_pt < 60 && abs(gen_eta) > 2.1 && abs(gen_eta) < 2.3" --title "50 < p_{T}^{gen} < 60 GeV, 2.1 < |#eta^{gen}| < 2.3;${DTHETA_TITLE}; a.u."         --xmin -0.02 --xmax 0.02 --nbins 100 --oname "scattering/scat_dtheta_pt_50_60_eta_2p1_2p3.pdf" --input '../matched_tree_MuMu_flatPt_0PU_23Apr2018.root'    --dtheta


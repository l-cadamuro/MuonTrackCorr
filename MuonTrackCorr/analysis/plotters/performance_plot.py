import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

fIn = ROOT.TFile.Open('../plots_JFsynch_pt20_eta1p2_2p4_scaledPt_tree.root')
tIn = fIn.Get('tree')

c1_square = ROOT.TCanvas('c1_square', 'c1_square', 600, 600)
c1_rect   = ROOT.TCanvas('c1_rect', 'c1_rect')

c1_square.SetLeftMargin(0.15)
c1_square.SetBottomMargin(0.15)
c1_square.SetRightMargin(0.2)
# c1_square.SetTopMargin(0.15)

save_in = 'performance_plots'

##### make the plots. Each entry is a line with
##### draw_string selection histo plot_opts myoptions_string
plots = [
    
    ######## EMTF plots 2D pT resolution
    # (
    #     'emtf_xml_pt : gen_pt',
    #     'emtf_pt > 0',
    #     ROOT.TH2D('EMTF_pt_vs_gen_pt', '; p_{T}^{gen} ; p_{T}^{EMTF xml} ; a.u.', 200, 0, 200, 200, 0, 200),
    #     'colz',
    #     'square-logz'
    # ),
    # ##
    # (
    #     '(emtf_xml_pt - gen_pt)/gen_pt : gen_pt',
    #     'emtf_pt > 0',
    #     ROOT.TH2D('EMTF_pt_vs_gen_pt_rel', '; p_{T}^{gen} ; (p_{T}^{EMTF xml}/p_{T}^{gen}) - 1 ; a.u.', 400, 0, 400, 200, -1, 20),
    #     'colz',
    #     'square-logz'
    # ),
    # ##
    # (
    #     '(emtf_xml_pt - gen_pt)/gen_pt : gen_pt',
    #     'emtf_pt > 0',
    #     ROOT.TH2D('EMTF_pt_vs_gen_pt_rel_zoom', '; p_{T}^{gen} ; (p_{T}^{EMTF xml}/p_{T}^{gen}) - 1 ; a.u.', 400, 0, 400, 200, -1, 1),
    #     'colz',
    #     'square-logz'
    # ),
    # ######## track plots 2D pT resolution
    # (
    #     'trk_pt : gen_pt',
    #     'trk_pt > 0',
    #     ROOT.TH2D('track_pt_vs_gen_pt', '; p_{T}^{gen} ; p_{T}^{track} ; a.u.', 200, 0, 200, 200, 0, 200),
    #     'colz',
    #     'square-logz'
    # ),
    # ##
    # (
    #     '(trk_pt - gen_pt)/gen_pt : gen_pt',
    #     'trk_pt > 0',
    #     ROOT.TH2D('track_pt_vs_gen_pt_rel', '; p_{T}^{gen} ; (p_{T}^{track}/p_{T}^{gen}) - 1 ; a.u.', 400, 0, 400, 200, -1, 20),
    #     'colz',
    #     'square-logz'
    # ),
    # ##
    # (
    #     '(trk_pt - gen_pt)/gen_pt : gen_pt',
    #     'trk_pt > 0',
    #     ROOT.TH2D('track_pt_vs_gen_pt_rel_zoom', '; p_{T}^{gen} ; (p_{T}^{track}/p_{T}^{gen}) - 1 ; a.u.', 400, 0, 400, 200, -1, 1),
    #     'colz',
    #     'square-logz'
    # )
    ######## displacement plots
    # (
    #     'emtf_theta - gen_theta : gen_pt',
    #     'emtf_pt > 0',
    #     ROOT.TH2D('emtf_gen_dtheta', '; p_{T}^{gen} ; #theta^{EMTF} - #theta^{gen} ; a.u.', 400, 0, 400, 200, -0.2, 0.2),
    #     'colz',
    #     'square-logz'
    # ),
    # (
    #     'emtf_theta - gen_theta : gen_pt',
    #     'emtf_pt > 0',
    #     ROOT.TH2D('emtf_gen_dtheta_zoom', '; p_{T}^{gen} ; #theta^{EMTF} - #theta^{gen} ; a.u.', 300, 0, 30, 200, -0.2, 0.2),
    #     'colz',
    #     'square-logz'
    # ),
    ##
    # (
    #     'trk_theta - gen_theta : gen_pt',
    #     'trk_pt > 0',
    #     ROOT.TH2D('track_gen_dtheta', '; p_{T}^{gen} ; #theta^{track} - #theta^{gen} ; a.u.', 400, 0, 400, 200, -0.01, 0.01),
    #     'colz',
    #     'square-logz'
    # ),
    # (
    #     'trk_theta - gen_theta : gen_pt',
    #     'trk_pt > 0',
    #     ROOT.TH2D('track_gen_dtheta_zoom', '; p_{T}^{gen} ; #theta^{track} - #theta^{gen} ; a.u.', 300, 0, 30, 200, -0.01, 0.01),
    #     'colz',
    #     'square-logz'
    # ),
    ##
    # (
    #     'emtf_phi - gen_phi : gen_pt',
    #     'emtf_pt > 0',
    #     ROOT.TH2D('emtf_gen_dphi', '; p_{T}^{gen} ; #varphi^{EMTF} - #varphi^{gen} ; a.u.', 400, 0, 400, 200, -0.2, 0.2),
    #     'colz',
    #     'square-logz'
    # ),
    # (
    #     'emtf_phi - gen_phi : gen_pt',
    #     'emtf_pt > 0',
    #     ROOT.TH2D('emtf_gen_dphi_zoom', '; p_{T}^{gen} ; #varphi^{EMTF} - #varphi^{gen} ; a.u.', 300, 0, 30, 200, -1.2, 1.2),
    #     'colz',
    #     'square-logz'
    # ),
    ##
    # (
    #     'trk_phi - gen_phi : gen_pt',
    #     'trk_pt > 0',
    #     ROOT.TH2D('track_gen_dphi', '; p_{T}^{gen} ; #varphi^{track} - #varphi^{gen} ; a.u.', 400, 0, 400, 200, -0.01, 0.01),
    #     'colz',
    #     'square-logz'
    # ),
    # (
    #     'trk_phi - gen_phi : gen_pt',
    #     'trk_pt > 0',
    #     ROOT.TH2D('track_gen_dphi_zoom', '; p_{T}^{gen} ; #varphi^{track} - #varphi^{gen} ; a.u.', 300, 0, 30, 200, -0.01, 0.01),
    #     'colz',
    #     'square-logz'
    # ),
    ######################### emtf vs tracks
    # (
    #     'emtf_xml_pt : trk_pt',
    #     'trk_pt > 0 && emtf_pt > 0',
    #     ROOT.TH2D('track_vs_emtf_pt', '; p_{T}^{track} ; p_{T}^{EMTF xml} ; a.u.', 300, 0, 300, 300, 0, 300),
    #     'colz',
    #     'square-logz'
    # ),
    # (
    #     'TMath::Sqrt((emtf_eta - trk_eta)*(emtf_eta - trk_eta) +  TVector2::Phi_mpi_pi(emtf_phi - trk_phi)*TVector2::Phi_mpi_pi(emtf_phi - trk_phi)) : gen_pt',
    #     'trk_pt > 0 && emtf_pt > 0',
    #     ROOT.TH2D('deltaR_track_emtf_vs_gen_pt', '; p_{T}^{gen} ; #DeltaR(track, EMTF); a.u.', 300, 0, 300, 3000, 0, 3),
    #     'colz',
    #     'square-logy'
    # ),
    # (
    #     'emtf_eta - trk_eta: gen_pt',
    #     'trk_pt > 0 && emtf_pt > 0',
    #     ROOT.TH2D('delta_eta_track_emtf_vs_gen_pt', '; p_{T}^{gen} ; #Delta#eta(track, EMTF); a.u.', 300, 0, 300, 3000, 0, 0.5),
    #     'colz',
    #     'square-logy'
    # ),
    # (
    #     'TVector2::Phi_mpi_pi(emtf_phi - trk_phi) : gen_pt',
    #     'trk_pt > 0 && emtf_pt > 0',
    #     ROOT.TH2D('deltaPhi_track_emtf_vs_gen_pt', '; p_{T}^{gen} ; #Delta#varphi(track, EMTF); a.u.', 300, 0, 300, 3000, 0, 3),
    #     'colz',
    #     'square-logy'
    # ),
    # (
    #     'TVector2::Phi_mpi_pi(emtf_phi - trk_phi) : emtf_xml_pt',
    #     'trk_pt > 0 && emtf_pt > 0',
    #     ROOT.TH2D('deltaPhi_track_emtf_vs_emtf_pt', '; p_{T}^{EMTF xml} ; #Delta#varphi(track, EMTF); a.u.', 300, 0, 300, 3000, 0, 3),
    #     'colz',
    #     'square-logy'
    # ),
    (
        'TMath::Sqrt((emtf_eta - trk_eta)*(emtf_eta - trk_eta) +  TVector2::Phi_mpi_pi(emtf_phi - trk_phi)*TVector2::Phi_mpi_pi(emtf_phi - trk_phi)) : 1./gen_pt',
        'trk_pt > 0 && emtf_pt > 0',
        ROOT.TH2D('deltaR_track_emtf_vs_OneOvergen_pt', '; 1/p_{T}^{gen} ; #DeltaR(track, EMTF); a.u.', 300, 0, 0.25, 3000, 0, 3),
        'colz',
        'square-logy'
    ),
    (
        'emtf_eta - trk_eta: 1./gen_pt',
        'trk_pt > 0 && emtf_pt > 0',
        ROOT.TH2D('delta_eta_track_emtf_vs_OneOvergen_pt', '; 1/p_{T}^{gen} ; #Delta#eta(track, EMTF); a.u.', 300, 0, 0.25, 3000, 0, 0.5),
        'colz',
        'square-logy'
    ),
    (
        'TVector2::Phi_mpi_pi(emtf_phi - trk_phi) : 1./gen_pt',
        'trk_pt > 0 && emtf_pt > 0',
        ROOT.TH2D('deltaPhi_track_emtf_vs_OneOvergen_pt', '; 1/p_{T}^{gen} ; #Delta#varphi(track, EMTF); a.u.', 300, 0, 0.25, 3000, 0, 3),
        'colz',
        'square-logy'
    ),
    (
        'TVector2::Phi_mpi_pi(emtf_phi - trk_phi) : 1./emtf_xml_pt',
        'trk_pt > 0 && emtf_pt > 0',
        ROOT.TH2D('deltaPhi_track_emtf_vs_OneOveremtf_pt', '; 1/p_{T}^{EMTF xml} ; #Delta#varphi(track, EMTF); a.u.', 300, 0, 0.25, 3000, 0, 3),
        'colz',
        'square-logy'
    ),
]

for idx, pl in enumerate(plots):
    
    print '... plot', idx, 'of', len(plots)-1

    draw_string = pl[0]
    selection = pl[1]
    histo = pl[2]
    plot_opts = pl[3]
    myoptions_string = pl[4]

    mycanv = c1_square
    if 'rect' in myoptions_string:
        mycanv = c1_rect
    elif 'square' in myoptions_string:
        mycanv = c1_square
    mycanv.cd()
    mycanv.SetLogx(False)
    mycanv.SetLogy(False)
    mycanv.SetLogz(False)

    if 'logx' in myoptions_string: mycanv.SetLogx(True)
    if 'logy' in myoptions_string: mycanv.SetLogy(True)
    if 'logz' in myoptions_string: mycanv.SetLogz(True)


    print '....... PLOT: ', '%s >> %s' % (draw_string, histo.GetName())
    print '....... SEL:  ', selection
    
    tIn.Draw('%s >> %s' % (draw_string, histo.GetName()), selection)
    histo.GetXaxis().SetTitleOffset(1.3)
    histo.GetYaxis().SetTitleOffset(1.3)
    histo.GetZaxis().SetTitleOffset(1.3)
    histo.GetXaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetTitleSize(0.05)
    histo.GetZaxis().SetTitleSize(0.05)

    if plot_opts:
        histo.Draw(plot_opts)
    else:
        histo.Draw()

    # print save_in + '/' + histo.GetName()+'.pdf'
    mycanv.Print(save_in + '/' + histo.GetName()+'.pdf', 'pdf')

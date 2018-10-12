import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def set_single_h(h, pl):
    nb = h.GetNbinsX()
    xmin = h.GetXaxis().GetBinLowEdge(1)
    xmax = h.GetXaxis().GetBinLowEdge(nb+1)
    if 'xmin' in pl: xmin = pl['xmin']
    if 'xmax' in pl: xmax = pl['xmax']
    h.GetXaxis().SetRangeUser(xmin, xmax)
    h.GetXaxis().SetTitleOffset(1.2)
    h.GetYaxis().SetTitleOffset(1.4)
    h.GetXaxis().SetTitleSize(0.055)
    h.GetYaxis().SetTitleSize(0.055)
    h.GetXaxis().SetLabelSize(0.045)
    h.GetYaxis().SetLabelSize(0.045)
    if 'title' in pl: h.SetTitle(pl['title'])
    if 'norm' in pl and h.Integral() > 0: h.Scale(pl['norm']/h.Integral())
    if 'msize' in pl: h.SetMarkerSize(pl['msize'])
    if 'mstyle' in pl: h.SetMarkerStyle(pl['mstyle'])
    if 'lwidth' in pl: h.SetLineWidth(pl['lwidth'])
    if 'lstyle' in pl: h.SetLineStyle(pl['lstyle'])

def redrawBorder(c1):
    # this little macro redraws the axis tick marks and the pad border lines.
    ROOT.gPad.Update();
    ROOT.gPad.RedrawAxis();
    l = ROOT.TLine ()
    l.SetLineWidth(c1.GetFrameLineWidth())
    l.DrawLine(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUymax(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax());
    l.DrawLine(ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax());


# fIn = ROOT.TFile.Open('../trk_plots_ZToMuMu_200PU_21Mag.root')
# fIn = ROOT.TFile.Open('../trk_plots_ZToMuMu_200PU_21Mag_alltrks.root')
fIn = ROOT.TFile.Open('../trk_plots_NeutrinoGun_200PU_mults.root')

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetFrameLineWidth(3)
c1.SetLeftMargin(0.15)
c1.SetBottomMargin(0.15)

plots = [
    # {
    #     'name' : 'nTracks_2',
    #     'logy'  : False,
    #     'logx'  : True,
    #     'xmin' : 1,
    #     'xmax' : 100,
    # },
    # {
    #     'name' : 'nTracks_3',
    #     'logy'  : False,
    #     'logx'  : True,
    #     'xmin' : 1,
    #     'xmax' : 100,
    # },
    # {
    #     'name' : 'nTracks_5',
    #     'logy'  : False,
    #     'logx'  : True,
    #     'xmin' : 1,
    #     'xmax' : 100,
    # },
    # {
    #     'name' : 'nTracks_10',
    #     'logy'  : False,
    #     'logx'  : True,
    #     'xmin' : 1,
    #     'xmax' : 100,
    # },
    {
        'namelist' : ['nTracks_2', 'nTracks_3', 'nTracks_5', 'nTracks_10'],
        'legends' : ['p_{T} > 2 GeV', 'p_{T} > 3 GeV', 'p_{T} > 5 GeV', 'p_{T} > 10 GeV'],
        'colors' : [ROOT.kRed, ROOT.kOrange+1, ROOT.kGreen+1, ROOT.kBlue],
        'title'  : ';N_{tracks}; a.u.',
        'norm' : 1.0,
        'logy'   : False,
        'logx'   : True,
        'xmin' : 1,
        'xmax' : 100,
        'ymax' : 0.5,
        'msize' :  0,
        'lwidth' : 3,
        'drawstyle' : 'E hist'
    },
    {
        'namelist' : ['nTracks_2_60deg', 'nTracks_3_60deg', 'nTracks_5_60deg', 'nTracks_10_60deg'],
        'legends' : ['p_{T} > 2 GeV', 'p_{T} > 3 GeV', 'p_{T} > 5 GeV', 'p_{T} > 10 GeV'],
        'colors' : [ROOT.kRed, ROOT.kOrange+1, ROOT.kGreen+1, ROOT.kBlue],
        'title'  : ';N_{tracks} with 0 < #varphi < 60#circ; a.u.',
        'norm' : 1.0,
        'logy'   : False,
        'logx'   : True,
        'xmin' : 1,
        'xmax' : 100,
        'ymax' : 0.5,
        'msize' :  0,
        'lwidth' : 3,
        'drawstyle' : 'E hist'
    },
    {
        'namelist' : ['nEMTF_2', 'nEMTF_3', 'nEMTF_5', 'nEMTF_10'][1:],
        'legends' : ['p_{T} > 2 GeV', 'p_{T} > 3 GeV', 'p_{T} > 5 GeV', 'p_{T} > 10 GeV'][1:],
        'colors' : [ROOT.kRed, ROOT.kOrange+1, ROOT.kGreen+1, ROOT.kBlue][1:],
        'title'  : ';N_{EMTF}; a.u.',
        'norm' : 1.0,
        'logy'   : True,
        'logx'   : False,
        'xmin' : 0,
        'xmax' : 10,
        'msize' :  0,
        'lwidth' : 3,
        'drawstyle' : 'E hist'
    },
    {
        'namelist' : ['nEMTF_2_60deg', 'nEMTF_3_60deg', 'nEMTF_5_60deg', 'nEMTF_10_60deg'][1:],
        'legends' : ['p_{T} > 2 GeV', 'p_{T} > 3 GeV', 'p_{T} > 5 GeV', 'p_{T} > 10 GeV'][1:],
        'colors' : [ROOT.kRed, ROOT.kOrange+1, ROOT.kGreen+1, ROOT.kBlue][1:],
        'title'  : ';N_{EMTF} with 0 < #varphi < 60#circ; a.u.',
        'norm' : 1.0,
        'logy'   : True,
        'logx'   : False,
        'xmin' : 0,
        'xmax' : 10,
        'msize' :  0,
        'lwidth' : 3,
        'drawstyle' : 'E hist'
    },
    # ############
    {
        'name' : 'track_pt',
        'logy'  : True,
        'xmin' : 0,
        'xmax' : 500,
    },
    {
        'name' : 'track_pt',
        'logy'  : True,
        'xmin' : 1,
        'xmax' : 500,
        'logx' : True,
        'oname': 'track_pt_logx.pdf'
    },
    {
        'name' : 'EMTF_pt',
        'logy'  : True,
        'xmin' : 0,
        'xmax' : 150,
    },
    # #
    # {
    #     'name' : 'track_eta_2',
    # },
    # {
    #     'name' : 'track_eta_3',
    # },
    # {
    #     'name' : 'track_eta_5',
    # },
    # {
    #     'name' : 'track_eta_10',
    # },
    {
        'namelist' : ['track_eta_2', 'track_eta_3', 'track_eta_5', 'track_eta_10'],
        'legends' : ['p_{T} > 2 GeV', 'p_{T} > 3 GeV', 'p_{T} > 5 GeV', 'p_{T} > 10 GeV'],
        'colors' : [ROOT.kRed, ROOT.kOrange+1, ROOT.kGreen+1, ROOT.kBlue],
        'title'  : ';#eta_{track}; a.u.',
        'norm' : 1.0,
        'lcoords' : (0.6, 0.7, 0.88, 0.88),
        'ymax' : 0.045,
    },
]


for pl in plots:
    
    ### an overlay
    if 'namelist' in pl:

        hs = []
        namelist = pl['namelist']
        colors   = pl['colors'] if 'colors' in pl else None
        legends  = pl['legends'] if 'legends' in pl else None
        for idx, name in enumerate(namelist):
            h = fIn.Get(name)
            hs.append(h)

        if 'norm' in pl:
            for h in hs:
                if h.Integral() > 0: h.Scale(pl['norm']/h.Integral())

        mmaxs = [h.GetMaximum() for h in hs]

        c1.SetLogx(False)
        c1.SetLogy(False)
        if 'logy' in pl: c1.SetLogy(pl['logy'])
        if 'logx' in pl: c1.SetLogx(pl['logx'])

        for idx, h in enumerate(hs):
            
            set_single_h(h, pl)
            
            if idx == 0:
                ymax = 1.15*max(mmaxs)
                if 'ymax' in pl: ymax = pl['ymax']
                h.SetMaximum(ymax)

            if legends:
                if idx == 0:
                    lx1, lx2, ly1, ly2 = 0.6, 0.6, 0.88, 0.88
                    if 'lcoords' in pl: lx1, lx2, ly1, ly2 = pl['lcoords']
                    leg = ROOT.TLegend(lx1, lx2, ly1, ly2)
                    leg.SetFillStyle(0)
                    leg.SetBorderSize(0)
                leg.AddEntry(h, legends[idx], 'l')

            col = colors[idx] if colors else idx+1
            h.SetLineColor(col)
            h.SetMarkerColor(col)
            h.SetMarkerStyle(8)
            h.SetMarkerSize(0.4)

            # if 'fit' in pl:
            #     h.Fit(pl['fit'])

            drawstyle = ''
            if 'drawstyle' in pl:
                drawstyle = pl['drawstyle']
            if idx == 0:
                print h.Integral()
                h.Draw(drawstyle)
            else:
                print h.Integral()
                h.Draw(drawstyle + ' same')
        
        if legends: leg.Draw()
        if not c1.GetLogx() and not c1.GetLogy(): redrawBorder(c1)
        oname = 'track_plots/overlay_%s.pdf' % namelist[0]
        if 'oname' in pl: oname = 'track_plots/' + pl['oname']
        c1.Print(oname, 'pdf')
    
    #### a signle plot
    else:
        name = pl['name']
        h = fIn.Get(name)
        c1.SetLogx(False)
        c1.SetLogy(False)
        if 'logy' in pl: c1.SetLogy(pl['logy'])
        if 'logx' in pl: c1.SetLogx(pl['logx'])
        set_single_h(h, pl)
        h.Draw()
        oname = 'track_plots/%s.pdf' % name
        if 'oname' in pl: oname = 'track_plots/' + pl['oname']
        c1.Print(oname, 'pdf')

import ROOT
import collections
import copy
import random

ROOT.gStyle.SetOptStat(0)
random.seed(1)

class cut:
    def __init__(self, val):
        self.cut = val
    
    def concat(self, one, two):
        """ concatenate two strings """
        proto = '({one}) && ({two})'
        return proto.format(one=one, two=two)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return cut(self.concat(self.cut, other.cut))
        elif isinstance(other, basestring):
            return cut(self.concat(self.cut, other))
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))

    def __iadd__(self, other):
        self.cut = self.cut + other
        return self

    def __str__(self):
        rep = 'CUT: ' + self.cut
        return rep

class histo:
    def __init__(self, name, title, expr, cut, nbins, range_binning):
        """ if nbins < 0, range_binning defines the user binning with boundaries
        if nbins >= 0, range_binning is the usual xmin / xmax """
        self.name  = name
        self.title = title
        self.expr  = expr
        self.cut   = cut
        self.nbins = nbins
        if self.nbins < 0:
            self.userBinning = True
            self.nbins       = len(range_binning) - 1
            self.binning     = array('d',range_binning)
        else:
            self.userBinning = False
            if len(range_binning) != 2:
                raise RuntimeError('histo : range_binning malformed: expect exactly two values')
            self.xmin = float(range_binning[0])
            self.xmax = float(range_binning[1])

        if self.userBinning:
            self.histo = ROOT.TH1D(self.name, self.title, self.nbins, self.binning)
        else:
            self.histo = ROOT.TH1D(self.name, self.title, self.nbins, self.xmin, self.xmax)
        
        self.histo.SetDirectory(0)

    def set_properties(self, properties):
        self.properties = copy.deepcopy(properties)

    def build_histo(self, tIn):
        self.histo.SetDirectory(ROOT.gDirectory) ## needed to make the ttree aware of this histo
        tIn.Draw('{expr} >> {hname}'.format(expr=self.expr, hname=self.name), self.cut)
        if 'norm' in self.properties and self.histo.Integral() > 0:
            self.histo.Scale(self.properties['norm']/self.histo.Integral())
        self.histo.SetDirectory(0) 

#############################################################################################

class plotMaker:
    def __init__(self):
        self.histos = collections.OrderedDict()
        self.plot_alone_if_in_overlay = False
        self.plot_name_proto = '{hname}.pdf'
        self.rootfile_output = None
        self.def_col_palette = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1, ROOT.kBlack, ROOT.kMagenta, ROOT.kCyan, ROOT.kOrange]

    def load_histos(self, histo_defs):
        print '... loading histos'
        for hd in histo_defs:
            properties = histo_defs[hd]
            name  = properties['name']
            title = properties['title'] if 'title' in properties else name
            expr  = properties['expr']
            cut   = properties['cut']   if 'cut' in properties else ''
            if 'nbins' in properties:
                nbins = properties['nbins']
                xmin  = properties['xmin']
                xmax  = properties['xmax']
                range_binning = (xmin, xmax)
            else:
                nbins = -1
                range_binning = properties['binning']
            this_h = histo(name, title, expr, cut, nbins, range_binning)
            this_h.set_properties(properties) ## will copy also some unneeded properties

            self.histos[hd] = this_h
        print '... loaded', len(self.histos), 'histos'

    def build_histos(self, tIn):
        print "... building", len(self.histos), 'histos'
        for idx, hname in enumerate(self.histos):
            h = self.histos[hname]
            if idx%10 == 0:
                print ' >>> bulding {} / {}'.format(idx, len(self.histos))
            h.build_histo(tIn)

    def set_overlays(self, overlays):
        self.overlays = copy.deepcopy(overlays)
        self.all_to_overlay = []
        for ovr in self.overlays.values():
            self.all_to_overlay.extend(ovr['parts'])
        self.all_to_overlay = list(set(self.all_to_overlay))

    def plot_all(self, do_png=False):

        try: self.c1
        except AttributeError:
            print '... building internally a canvas'
            self.c1 = ROOT.TCanvas('c1', 'c1', 600, 600)

        ## first plot all plots intended to be done alone
        print "... plotting individual plots"
        for hname in self.histos:
            h = self.histos[hname]
            if not self.plot_alone_if_in_overlay and hname in self.all_to_overlay:
                continue
            plotname = self.plot_name_proto.format(hname=hname)
            h.histo.Draw()
            self.c1.Print(plotname, 'pdf')
            if do_png: self.c1.Print(plotname.replace('.pdf', '.png'), 'png')

        ## now plot the overlays
        print "... plotting overlays"
        for ovr, vals in self.overlays.items():
            frame  = self.histos[vals['parts'][0]].histo.Clone(ovr)
            if 'title' in vals: frame.SetTitle(vals['title'])
            nelems = len(vals['parts'])
            if nelems > len(self.def_col_palette): ## expand the palette
                rndmcol = lambda: random.randint(0,255)
                for i in range(nelems - len(self.def_col_palette)):
                    col = ROOT.TColor.GetColor('#%02X%02X%02X' % (rndmcol(), rndmcol(), rndmcol()))
                    self.def_col_palette.append(col)

            mmaxs = [self.histos[h].histo.GetMaximum() for h in vals['parts']]
            mmax  = max(mmaxs)

            frame.SetMaximum(1.15*mmax)
            frame.Draw()

            ## build the legend
            leg = ROOT.TLegend(0.6, 0.6, 0.88, 0.88)
            leg.SetFillStyle(0)
            leg.SetBorderSize(0)

            # plot the frame
            for idx, el in enumerate(vals['parts']):
                the_h = self.histos[el].histo
                the_h.SetLineColor(self.def_col_palette[idx])
                the_h.Draw('same')
                leg_name = vals['leg'][el] if 'leg' in vals and el in vals['leg'] else el
                leg.AddEntry(the_h, leg_name, 'l')
            leg.Draw()
            plotname = self.plot_name_proto.format(hname=ovr)
            if 'logy' in vals: self.c1.SetLogy(vals['logy'])    
            self.c1.Print(plotname, 'pdf')
            if do_png: self.c1.Print(plotname.replace('.pdf', '.png'), 'png')

            ## reset the canvas defaults
            self.c1.SetLogy(True)

        ## dump to file if required - just the individual plots, no need for overlays
        if self.rootfile_output:
            print "... saving to file: ", self.rootfile_output.GetName()
            for hname in self.histos:
                h = self.histos[hname]
                self.rootfile_output.cd()
                h.histo.Write()
import numpy
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i"  , "--input"     , dest = "input"     ,  help = "input file"       , default = ''                        )
parser.add_argument("-d"  , "--diff"      , dest = "diff"      ,  help = "plot differences" , default = False, action='store_true')
parser.add_argument("-l"  , "--leg"       , dest = "leg"       ,  help = "legend labels"    , default = ''                        )

options = parser.parse_args()
if not options.input:   
  parser.error('Input filename not given')

import ROOT
import math
from   ROOT  import TFile, TTree, gDirectory, TH1F, TCanvas, TLegend, gPad, gStyle, gROOT, TGaxis, TPad, TGraphErrors
from   array import array
from   itertools import product

gROOT.SetBatch(True)
gStyle.SetOptStat('emr')
gStyle.SetOptFit(1)
gStyle.SetTitleAlign(23)
gStyle.SetPadLeftMargin(0.16)
gStyle.SetPadBottomMargin(0.16)
TGaxis.SetMaxDigits(3)

namefiles = options.input.split(',')
nfiles   = len(namefiles)
files    = []

print 'number of input files is ' + str(nfiles)
for i in range(0, nfiles):
  print 'opening file ' + str(i) + ': ' + namefiles[i]
  files.append(TFile.Open(namefiles[i]   , 'r') )


pc        = TCanvas('pc', 'pc', 400,400)
colorlist = [ROOT.kBlack, ROOT.kGray+1, ROOT.kRed, ROOT.kOrange-3, ROOT.kViolet, ROOT.kViolet-9]


def doHisto(file, var, what, i):

  pEff1  = file.Get(var[0] + '_' + str(i) + what  )
  
  pEff1.SetLineColor  (colorlist[0])
  pEff1.SetMarkerColor(colorlist[0])
  pEff1.SetMarkerStyle(8)
  pEff1.SetMarkerSize(0.8)
  pEff1.SetTitle(";" + var[1] + ";" + var[2])
  
  pc.cd()
  pEff1.Rebin(var[3])
  pEff1.Draw()

  thef = ROOT.TF1 ('thef', 'gaus', float(pEff1.GetMean() - 3*pEff1.GetRMS()), pEff1.GetMean() + 3*pEff1.GetRMS())
  pEff1.Fit('thef', 'R')
#   pc.SaveAs( pEff1.GetName() + '_278820.pdf')
  width = thef.GetParameter(2)
  err   = thef.GetParError(2)
  return width,err




ytitle = 'events'

variables = [
#  name          # x axis title            # y title   # rebin    # x range [not used]      # y range[not used]  # pdf name                     # legend position         #y range ratio          
 ('diffX'          , 'resolution X [cm]'    , ytitle,   1         , ( -2.4 , 2.4),          (0. , 12E-3),         'resolutionX_'      ,  (0.55 , 0.85, 0.68, 0.85),  (0.9  , 1.05  )),
 ('diffY'          , 'resolution Y [cm]'    , ytitle,   1         , ( -2.4 , 2.4),          (0. , 12E-3),         'resolutionY_'      ,  (0.55 , 0.85, 0.68, 0.85),  (0.9  , 1.05  )),
 ('diffZ'          , 'resolution Z [cm]'    , ytitle,   1         , ( -2.4 , 2.4),          (0. , 25E-3),         'resolutionZ_'      ,  (0.55 , 0.85, 0.68, 0.85),  (0.9  , 1.05  )),
 ('pullX'          , 'pull X [cm]'          , ytitle,   2         , ( -2.4 , 2.4),          (-2. , 4.   ),         'pullX_'            ,  (0.18 , 0.45, 0.18, 0.42),  (0.9  , 1.05  )),
 ('pullY'          , 'pull Y [cm]'          , ytitle,   2         , ( -2.4 , 2.4),          (-2. , 4.   ),         'pullY_'            ,  (0.18 , 0.45, 0.18, 0.42),  (0.9  , 1.05  )),
 ('pullZ'          , 'pull Z [cm]'          , ytitle,   2         , ( -2.4 , 2.4),          (-2. , 4.   ),         'pullZ_'            ,  (0.18 , 0.45, 0.18, 0.42),  (0.9  , 1.05  )),
]   

       #          # min number of  #max number of   # x title for final graph
wrt = [('Trks'  ,       2,         80,               '# tracks in the split vertex'),#   40), 
       ('Vtx'   ,       2,         40,               '# vertices in the event'     ),#   25)
       ('sumPt' ,       0,         20,               'sumPt [GeV]'     ),#   25)
      ]

for ix, var in product(wrt,variables):
  nc      = TCanvas('nc', 'nc', 400, 400)
  graphs  = []

  l = TLegend(var[7][0], var[7][2], var[7][1], var[7][3])
  l.SetBorderSize(0)
  l.SetTextSize(0.028)

  for j,jfile in enumerate(files):
    they    = []
    theyerr = []
    thex    = []
    for i in range( ix[1], ix[2]):

      width, err = doHisto(files[j] , var, ix[0], i)

      if 'diff' in var[0]:
        they   .append(width/math.sqrt(2))
        theyerr.append(err/math.sqrt(2))
      else:  
        they   .append(width)
        theyerr.append(err)
    
      if 'sumPt' not in ix[0]:
        thex   .append(float(i))
      else:
        thex   .append(float(i*10+5))
       
    yvec      = numpy.array( they           )
    yerrvec   = numpy.array( theyerr        )
    xvec      = numpy.array( thex           )
  
    if 'sumPt' not in ix[0]:
      xerrvec   = numpy.array( [0.5 for i in yvec]     )
    else:
      xerrvec   = numpy.array( [5 for i in yvec]     )
  
    g = ROOT.TGraphErrors( len(yvec), xvec, yvec, xerrvec, yerrvec)
    nc.cd()
  
    print colorlist[j]
    g.SetLineColor  (colorlist[j])
    g.SetMarkerColor(colorlist[j])
    g.SetMarkerStyle(8 )
    g.SetMarkerSize(0.8)
    g.SetTitle('')
    g.GetXaxis().SetTitle(ix[3])
    g.GetYaxis().SetTitle(var[1])
    g.GetYaxis().SetRangeUser(var[5][0], var[5][1])
    graphs.append(g)

  nc.cd()
  for j,jgraph in enumerate(graphs):
    jgraph.Draw('AP'*(j==0) + 'P same'*(j!=0))
  
    if options.leg:
      l.AddEntry(jgraph , options.leg.split(',')[j]  , "pel")

    nc.Update()
    nc.Modified()

  if options.leg:
    l.Draw()

  gPad.SetGridx(True)
  gPad.SetGridy(True)
  nc.SaveAs( 'pull_resolution_plots/' + var[6] + 'vs' + ix[0] + '_Run278820_RelVal.pdf')


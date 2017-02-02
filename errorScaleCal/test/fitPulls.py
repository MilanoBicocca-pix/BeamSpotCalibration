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
from   ROOT  import TFile, TTree, gDirectory, TH1F, TCanvas, TLegend, gPad, gStyle, TGaxis, TPad, TGraphErrors
from   array import array

gStyle.SetOptStat('emr')
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
colorlist = [ROOT.kBlack, ROOT.kRed, ROOT.kGreen+1, ROOT.kAzure+1, ROOT.kViolet]
min_tracks = 2
max_tracks = 30

def doHisto(file, var, i):

  pEff1  = file.Get(var[0] + '_' + str(i*2) + 'Trks'  )
  
  pEff1.SetLineColor  (ROOT.kBlack)
  pEff1.SetMarkerColor(ROOT.kBlack)
  pEff1.SetMarkerStyle(8)
  pEff1.SetMarkerSize(0.8)
  pEff1.SetTitle(";" + var[1] + ";" + var[2])
  
  pc.cd()
  pEff1.Draw()

  thef = ROOT.TF1 ('thef', 'gaus', -4, 4)
  pEff1.Fit('thef')
  pc.SaveAs( pEff1.GetName() + '.pdf')
  width = thef.GetParameter(2)
  err   = thef.GetParError(2)
  return width,err




ytitle = 'events'

variables = [
#  name          # x axis title            # y title   # rebin    # x range [not used]      # y range[not used]  # pdf name                     # legend position         #y range ratio          
 ('pullX'          , 'pull X [cm]'         , ytitle,   1         , ( -2.4 , 2.4),          (0.8 , 1.01),         'pullX_'      ,  (0.18 , 0.35, 0.18, 0.32),  (0.9  , 1.05  )),
 ('pullY'          , 'pull Y [cm]'         , ytitle,   1         , ( -2.4 , 2.4),          (0.8 , 1.01),         'pullY_'      ,  (0.18 , 0.35, 0.18, 0.32),  (0.9  , 1.05  )),
 ('pullZ'          , 'pull Z [cm]'         , ytitle,   1         , ( -2.4 , 2.4),          (0.8 , 1.01),         'pullZ_'      ,  (0.18 , 0.35, 0.18, 0.32),  (0.9  , 1.05  )),
] 



for var in variables:
  
  l = TLegend(var[7][0], var[7][2], var[7][1], var[7][3])
  l.SetBorderSize(0)
  l.SetTextSize(0.028)

  they    = []
  theyerr = []
  thex    = []
  for i in range( min_tracks, max_tracks):
    width, err = doHisto(files[0] , var, i)

    they   .append(width)
    theyerr.append(err)
    thex   .append(float(i*2))
  
  yvec      = numpy.array( they           )
  yerrvec   = numpy.array( theyerr        )
  xvec      = numpy.array( thex           )
  xerrvec   = numpy.array( [1 for i in yvec]     )

  g = ROOT.TGraphErrors( len(yvec), xvec, yvec, xerrvec, yerrvec)
  nc = TCanvas()
  nc.cd()

  g.SetLineColor  (ROOT.kBlack)
  g.SetMarkerColor(ROOT.kBlack)
  g.SetMarkerStyle(8 )
  g.SetMarkerSize(0.8)
  g.SetTitle('')
  g.GetXaxis().SetTitle('# tracks in the original vertex')
  g.GetYaxis().SetTitle('gaussian width from fit to pull')
  g.GetYaxis().SetRangeUser(0.7, 1.5)
  g.Draw('AP')
    
#     if options.leg:
# #       labels = []
# #       labels.append( options.leg.split(',')[i] )
#       l.AddEntry(pEff1 , options.leg.split(',')[i]  , "pel")

  if options.leg:
    l.Draw()
    
  gPad.SetGridx(True)
  gPad.SetGridy(True)
  nc.SaveAs("" +  var[6] + "_width_pulls.pdf")




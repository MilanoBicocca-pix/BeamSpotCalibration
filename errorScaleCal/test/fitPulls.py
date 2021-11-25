from __future__ import print_function

import ROOT
import os
import math
import numpy
from itertools import product

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input' , nargs='+')
parser.add_argument('--output', default = './fit_results')
parser.add_argument('--label' , nargs='+', default = None)
parser.add_argument('--legend', action = 'store_true')
args = parser.parse_args()

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1)
ROOT.gStyle.SetTitleAlign(23)
ROOT.gStyle.SetPadLeftMargin(0.16)
ROOT.gStyle.SetPadBottomMargin(0.16)
ROOT.TGaxis.SetMaxDigits(3)

step_pt=2

if not os.path.exists('/'.join([args.output, 'fits'])):
  os.makedirs('/'.join([args.output, 'fits']))

if args.label is None:
  args.label = ['file_%s' %i for i in range(len(args.input))]

class Var:
  def __init__(self, name, title, rebin, yrange, legend_position):
    self.name  = name
    self.title = title
    self.rebin = rebin
    self.yrange = yrange
    self.legend_position = legend_position

class Bin:
  def __init__(self, name, lo, hi, title):
    self.name  = name
    self.title = title
    self.lo    = lo
    self.hi    = hi

variables = [
  #Var('diffX', 'resolution X [cm]', (0., 12E-3), 1, (0.55 , 0.85, 0.68, 0.85)),
  #Var('diffY', 'resolution Y [cm]', (0., 12E-3), 1, (0.55 , 0.85, 0.68, 0.85)),
  #Var('diffZ', 'resolution Z [cm]', (0., 25E-3), 1, (0.55 , 0.85, 0.68, 0.85)),
  Var('pullX', 'pull X [cm]', 1, (0., 2.), (0.8, 0.7, 0.85, 0.85)),
  Var('pullY', 'pull Y [cm]', 1, (0., 2.), (0.8, 0.7, 0.85, 0.85)),
  Var('pullZ', 'pull Z [cm]', 1, (0., 2.), (0.8, 0.7, 0.85, 0.85)),
]

wrt = [
  Bin('Trks' , 5, 35, '# tracks in the split vertex'),
  Bin('Vtx'  , 1, 6,  '# vertices in the event'     ),
  Bin('sumPt', 0, 24, 'sumPt [GeV]'                 ),
]

colorlist = [ROOT.kBlack, ROOT.kGray+1, ROOT.kRed, ROOT.kOrange-3, ROOT.kViolet, ROOT.kViolet-9]

## first fit the unbinned pulls and diffs
for var in variables:
  yval, yerr = [], []
  for j,(ff, lab) in enumerate(zip(args.input, args.label)):
    fit_can = ROOT.TCanvas()
    fit_can.cd()
    
    tfile = ROOT.TFile.Open(ff, 'READ')
    binh = tfile.Get('%s_unbinned' %var.name)

    binh.SetTitle('%s - %s' %(var.title, lab))
    binh.Rebin(var.rebin)

    fitf = ROOT.TF1("gaussian", "gaus", float(binh.GetMean() - 3*binh.GetRMS()), binh.GetMean() + 3*binh.GetRMS())
    fitf.SetParameters(binh.GetEntries(), binh.GetMean(), binh.GetRMS())
    binh.Fit('gaussian', 'R')
    width = fitf.GetParameter(2)
    error = fitf.GetParError(2)

    binh.Draw("HIST")
    fitf.Draw("SAME")
    fit_can.SaveAs('%s/fits/%s_unbinned_%s.pdf' %(args.output, var.name, lab))

    yval.append(width / math.sqrt(2) if 'diff' in var.name else width)
    yerr.append(error / math.sqrt(2) if 'diff' in var.name else error)
  
  histo = ROOT.TH1F("h%s" %var.name, var.title, len(yval), 0, len(yval))
  histo.GetXaxis().SetTitle("file")
  histo.GetYaxis().SetTitle(var.title)
  histo.SetLineColor(ROOT.kBlack)
  histo.SetMarkerColor(ROOT.kBlack)
  histo.SetMarkerStyle(20)
  
  for i,(yv,ye) in enumerate(zip(yval, yerr)):
    histo.SetBinContent(i+1, yv)
    histo.SetBinError(i+1, ye)
    histo.GetXaxis().SetBinLabel(i+1, args.label[i])
  
  can = ROOT.TCanvas()
  can.cd()
  can.SetGridy()
  histo.Draw("PEX0")
  can.SaveAs("%s/%s_unbinned.pdf" %(args.output, var.name))

## now fit the binned histograms
for ix, var in product(wrt,variables):
  graphs  = []
  l = ROOT.TLegend(*var.legend_position)
  l.SetBorderSize(0)
  l.SetTextSize(0.028)

  for j,(ff, lab) in enumerate(zip(args.input, args.label)):
    yval, yerr, xval = [], [], []
    
    for i in range( ix.lo, ix.hi):
      tfile = ROOT.TFile.Open(ff, 'READ')

      fit_can = ROOT.TCanvas()
      fit_can.cd()

      if 'sumPt' in ix.name and i%step_pt != 0 : continue

      binh = tfile.Get('%s_%d%s' %(var.name, i, ix.name))

      binh.SetTitle('%s %s_%d - %s' %(var.title, ix.name, i, lab))
      binh.Rebin(var.rebin)

      fitf = ROOT.TF1("gaussian", "gaus", float(binh.GetMean() - 3*binh.GetRMS()), binh.GetMean() + 3*binh.GetRMS())
      binh.Fit('gaussian', 'R')
      width = fitf.GetParameter(2)
      error = fitf.GetParError(2)

      yval.append(width / math.sqrt(2) if 'diff' in var.name else width)
      yerr.append(error / math.sqrt(2) if 'diff' in var.name else error)
      xval.append(float(i))

      binh.Draw("HIST")
      fitf.Draw("SAME")
      fit_can.SaveAs("%s/fits/%s_%d%s.pdf" %(args.output, var.name, i, ix.name))
    
    yvalv = numpy.array(yval, dtype = numpy.float)
    yerrv = numpy.array(yerr, dtype = numpy.float)
    xvalv = numpy.array(xval, dtype = numpy.float)
    xerrv = numpy.array([step_pt/2. for i in yvalv], dtype = numpy.float) if 'sumPt' in ix.name else numpy.array([0.5 for i in yvalv], dtype = numpy.float)

    g = ROOT.TGraphErrors( len(yvalv), xvalv, yvalv, xerrv, yerrv)
    g.SetLineColor  (colorlist[j])
    g.SetMarkerColor(colorlist[j])
    g.SetMarkerStyle(8)
    g.SetMarkerSize(0.8)
    g.SetTitle('')
    g.GetXaxis().SetTitle(ix.title)
    g.GetYaxis().SetTitle(var.title)
    g.GetYaxis().SetRangeUser(*var.yrange)
    graphs.append(g)

  can = ROOT.TCanvas()
  can.cd()
  for j,jgraph in enumerate(graphs):
    jgraph.Draw('AP'*(j==0) + 'P same'*(j!=0))

    l.AddEntry(jgraph, args.label[j], "pel")
      
    can.Update()
    can.Modified()
    
  if args.legend: l.Draw()
    
  can.SetGridx(True)
  can.SetGridy(True)

  can.SaveAs('%s/%s_vs_%s.pdf' %(args.output, var.name, ix.name))

print ('all done')

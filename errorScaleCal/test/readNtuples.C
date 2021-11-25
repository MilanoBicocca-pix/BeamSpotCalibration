#include "TROOT.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TTree.h"
#include "TBranch.h"

#include <iostream>
#include <algorithm>
#include <vector>
#include <map>

#include "BeamSpotCalibration/errorScaleCal/src/pvTree.h"

// standard cuts for 13 TeV collisions
//int max_n_tracks   = 80;
//int max_n_vertices = 40;
int max_n_tracks   = 35;
int max_n_vertices = 6;
int max_sum_pt     = 25;
int max_res        = 10;
int sum_pt_step    = 2;

// these cuts are for high purity workflow and refer to the sub-vertex
//int   cut_n_tracks   = 30;
//float cut_sum_pt     = 50;
int   cut_n_tracks   = 3;
float cut_sum_pt     = 1;

float cut_max_sum_pt = 999999;

void readNtuples(){
  
  TChain* tree = new TChain("errorScaleCal/pvTree"); 
//   tree -> Add("/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/crab_errorScale_SeptReReco_2018A/180905_143455/0000/ntuple_errorScaleCalibration_*.root");
//   tree -> Add("/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/crab_errorScale_SeptReReco_2018B/180905_143540/0000/ntuple_errorScaleCalibration_*.root");
//   tree -> Add("/eos/cms/store/group/phys_tracking/beamspot/13TeV/2018/StreamExpressAlignment/crab_errorScale_SeptReReco_2018C/180905_143644/0000/ntuple_errorScaleCalibration_*.root");
//   tree -> Add("ntuples_278820_JetHT_newAlignment_VtxSelection_part2.root/errorScaleCal/pvTree");
//   tree -> Add("ntuples_278820_ZeroBias_newAlignment_VtxSelection.root/errorScaleCal/pvTree");
//   tree -> Add("ntuples_278820_ZeroBias_newAlignment_VtxSelection_part2.root/errorScaleCal/pvTree");
//   tree -> Add("ntuples_RelValTTBar_PU25.root/errorScaleCal/pvTree");
  tree -> Add("ntuple_errorScaleCalibration_beammTestLHC_ExpressPhysics_FEVT_newTkAl_newAPE_346512.root");

//  TFile* outfile = TFile::Open("pulls_RelValTTBar.root","RECREATE");
//  TFile* outfile = TFile::Open("pulls_Run2018C_JetHT_selected.root","RECREATE");
  TFile* outfile = TFile::Open("pulls_beammTestLHC_ExpressPhysics_FEVT_newTkAl_newAPE_346512.root","RECREATE");
  std::cout << "output file: " << outfile -> GetName() << std::endl;
  
  std::map<std::string, TH1F*> hpulls_ ;
  std::map<std::string, TH1F*> hdiffs_ ;
  
  hpulls_["pullX_unbinned"] = new TH1F("pullX_unbinned", "pullX_unbinned", 500, -10, 10);
  hpulls_["pullY_unbinned"] = new TH1F("pullY_unbinned", "pullY_unbinned", 500, -10, 10);
  hpulls_["pullZ_unbinned"] = new TH1F("pullZ_unbinned", "pullZ_unbinned", 500, -10, 10);
  hdiffs_["diffX_unbinned"] = new TH1F("diffX_unbinned", "diffX_unbinned", 300, -.15, .15);
  hdiffs_["diffY_unbinned"] = new TH1F("diffY_unbinned", "diffY_unbinned", 300, -.15, .15);
  hdiffs_["diffZ_unbinned"] = new TH1F("diffZ_unbinned", "diffZ_unbinned", 300, -.3, .3);

  for (int i = cut_n_tracks; i < max_n_tracks; i ++){
    hpulls_[Form("pullX_%dTrks",i)]  = new TH1F( Form("pullX_%dTrks",i),  Form("pullX_%dTrks",i),  500, -10 , 10. );	
    hpulls_[Form("pullY_%dTrks",i)]  = new TH1F( Form("pullY_%dTrks",i),  Form("pullY_%dTrks",i),  500, -10 , 10. );	
    hpulls_[Form("pullZ_%dTrks",i)]  = new TH1F( Form("pullZ_%dTrks",i),  Form("pullZ_%dTrks",i),  500, -10 , 10. );	
    hdiffs_[Form("diffX_%dTrks",i)]  = new TH1F( Form("diffX_%dTrks",i),  Form("diffX_%dTrks",i),  300, -.15, .15 );  
    hdiffs_[Form("diffY_%dTrks",i)]  = new TH1F( Form("diffY_%dTrks",i),  Form("diffY_%dTrks",i),  300, -.15, .15 );  
    hdiffs_[Form("diffZ_%dTrks",i)]  = new TH1F( Form("diffZ_%dTrks",i),  Form("diffZ_%dTrks",i),  300, -.3 , .3  );    
  }
  for (int i = 1; i < max_n_vertices; i ++){
    hpulls_[Form("pullX_%dVtx",i)]   = new TH1F( Form("pullX_%dVtx",i),   Form("pullX_%dVtx",i),   500, -10 , 10. );	
    hpulls_[Form("pullY_%dVtx",i)]   = new TH1F( Form("pullY_%dVtx",i),   Form("pullY_%dVtx",i),   500, -10 , 10. );	
    hpulls_[Form("pullZ_%dVtx",i)]   = new TH1F( Form("pullZ_%dVtx",i),   Form("pullZ_%dVtx",i),   500, -10 , 10. );	
    hdiffs_[Form("diffX_%dVtx",i)]   = new TH1F( Form("diffX_%dVtx",i),   Form("diffX_%dVtx",i),   300, -.15, .15 );  
    hdiffs_[Form("diffY_%dVtx",i)]   = new TH1F( Form("diffY_%dVtx",i),   Form("diffY_%dVtx",i),   300, -.15, .15 );  
    hdiffs_[Form("diffZ_%dVtx",i)]   = new TH1F( Form("diffZ_%dVtx",i),   Form("diffZ_%dVtx",i),   300, -.3 , .3  );	
  }
  for (int i = 0; i < max_sum_pt; i += sum_pt_step){
    hpulls_[Form("pullX_%dsumPt",i)] = new TH1F( Form("pullX_%dsumPt",i), Form("pullX_%dsumPt",i), 500, -10 , 10. );    
    hpulls_[Form("pullY_%dsumPt",i)] = new TH1F( Form("pullY_%dsumPt",i), Form("pullY_%dsumPt",i), 500, -10 , 10. );    
    hpulls_[Form("pullZ_%dsumPt",i)] = new TH1F( Form("pullZ_%dsumPt",i), Form("pullZ_%dsumPt",i), 500, -10 , 10. );    
    hdiffs_[Form("diffX_%dsumPt",i)] = new TH1F( Form("diffX_%dsumPt",i), Form("diffX_%dsumPt",i), 300, -.15, .15 );  
    hdiffs_[Form("diffY_%dsumPt",i)] = new TH1F( Form("diffY_%dsumPt",i), Form("diffY_%dsumPt",i), 300, -.15, .15 );  
    hdiffs_[Form("diffZ_%dsumPt",i)] = new TH1F( Form("diffZ_%dsumPt",i), Form("diffZ_%dsumPt",i), 300, -.3 , .3  );    
  }
  for (int i = 0; i < max_res; i ++){
    hpulls_[Form("pullX_%dRes",i)]   = new TH1F( Form("pullX_%dRes",i),   Form("pullX_%dRes",i),   500, -10,  10. );   
    hpulls_[Form("pullY_%dRes",i)]   = new TH1F( Form("pullY_%dRes",i),   Form("pullY_%dRes",i),   500, -10,  10. );   
    hpulls_[Form("pullZ_%dRes",i)]   = new TH1F( Form("pullZ_%dRes",i),   Form("pullZ_%dRes",i),   500, -10,  10. );   
  }

  PVevent* ev = new PVevent();
  tree -> SetBranchAddress("event", &ev);

  int nentries = tree->GetEntries();
  std::cout << "Number of entries = " << nentries << std::endl;

  for (Int_t eventNo=0; eventNo < nentries; eventNo++)
  {
    Int_t IgetEvent   = tree   -> GetEvent(eventNo);
    
    unsigned int npv = ev->pvs.size();
    for (int ipv = 0; ipv < npv; ipv++){
      
      // select the pv        
      PVcand thePV = ev -> pvs.at(ipv);

      //std::cout << "n_subVtx1: " << thePV.n_subVtx1 << "n_subVtx2: " << thePV.n_subVtx2 << std::endl;
      //std::cout << "sumPt_subVtx1: " << thePV.sumPt_subVtx1 << "sumPt_subVtx2: " << thePV.sumPt_subVtx1 << std::endl;

      if (thePV.ipos != 0                                                               ) continue;
      if (thePV.n_subVtx1     < cut_n_tracks   || thePV.n_subVtx2     < cut_n_tracks    ) continue;
      if (thePV.sumPt_subVtx1 < cut_sum_pt     || thePV.sumPt_subVtx2 < cut_sum_pt      ) continue;
      if (thePV.sumPt_subVtx1 > cut_max_sum_pt || thePV.sumPt_subVtx2 > cut_max_sum_pt  ) continue;

      float dX   = thePV.x_subVtx1 - thePV.x_subVtx2;
      float dY   = thePV.y_subVtx1 - thePV.y_subVtx2;
      float dZ   = thePV.z_subVtx1 - thePV.z_subVtx2;
      float errX = sqrt( pow(thePV.xErr_subVtx1,2) + pow(thePV.xErr_subVtx2,2) );
      float errY = sqrt( pow(thePV.yErr_subVtx1,2) + pow(thePV.yErr_subVtx2,2) );
      float errZ = sqrt( pow(thePV.zErr_subVtx1,2) + pow(thePV.zErr_subVtx2,2) );

      hpulls_["pullX_unbinned"] -> Fill(dX / errX);
      hpulls_["pullY_unbinned"] -> Fill(dY / errY);
      hpulls_["pullZ_unbinned"] -> Fill(dZ / errZ);
      hdiffs_["diffX_unbinned"] -> Fill(dX);
      hdiffs_["diffY_unbinned"] -> Fill(dY);
      hdiffs_["diffZ_unbinned"] -> Fill(dZ);

      if (thePV.n_subVtx1 > 2 && thePV.n_subVtx1 < max_n_tracks){
          
        hpulls_[Form("pullX_%dTrks", thePV.n_subVtx1)] ->  Fill( dX / errX );
        hdiffs_[Form("diffX_%dTrks", thePV.n_subVtx1)] ->  Fill( dX );

        hpulls_[Form("pullY_%dTrks", thePV.n_subVtx1)] ->  Fill( dY / errY );
        hdiffs_[Form("diffY_%dTrks", thePV.n_subVtx1)] ->  Fill( dY );

        hpulls_[Form("pullZ_%dTrks", thePV.n_subVtx1)] ->  Fill( dZ / errZ );
        hdiffs_[Form("diffZ_%dTrks", thePV.n_subVtx1)] ->  Fill( dZ );
      }
      
      if (ev->nVtx > 0 && ev->nVtx < max_n_vertices){
        hpulls_[Form("pullX_%dVtx", ev->nVtx)] ->  Fill( dX / errX );
        hpulls_[Form("pullY_%dVtx", ev->nVtx)] ->  Fill( dY / errY );
        hpulls_[Form("pullZ_%dVtx", ev->nVtx)] ->  Fill( dZ / errZ );
        hdiffs_[Form("diffX_%dVtx", ev->nVtx)] ->  Fill( dX );
        hdiffs_[Form("diffY_%dVtx", ev->nVtx)] ->  Fill( dY );
        hdiffs_[Form("diffZ_%dVtx", ev->nVtx)] ->  Fill( dZ );
      }

      for (int i=0; i < max_sum_pt; i += sum_pt_step){
      
        if (thePV.sumPt_subVtx1 > i && thePV.sumPt_subVtx1 < i+sum_pt_step &&
            thePV.sumPt_subVtx2 > i && thePV.sumPt_subVtx2 < i+sum_pt_step 
           ){
        
          hpulls_[Form("pullX_%dsumPt", i)] ->  Fill( dX / errX );
          hdiffs_[Form("diffX_%dsumPt", i)] ->  Fill( dX );

          hpulls_[Form("pullY_%dsumPt", i)] ->  Fill( dY / errY );
          hdiffs_[Form("diffY_%dsumPt", i)] ->  Fill( dY );

          hpulls_[Form("pullZ_%dsumPt", i)] ->  Fill( dZ / errZ );
          hdiffs_[Form("diffZ_%dsumPt", i)] ->  Fill( dZ );
        }
      }
      
      for (int i=0; i < max_res; i++){
        if (fabs(dX) > i*10E-4 && fabs(dX) < (i+1)*10E-4){
          hpulls_[Form("pullX_%dRes", i)] ->  Fill( dX / errX );
        }
        if (fabs(dY) > i*10E-4 && fabs(dY) < (i+1)*10E-4){
          hpulls_[Form("pullY_%dRes", i)] ->  Fill( dY / errY );
        }
        if (fabs(dZ) > i*10E-4 && fabs(dZ) < (i+1)*10E-4){
          hpulls_[Form("pullZ_%dRes", i)] ->  Fill( dZ / errZ );
        }
      }
    }//end loop PV
  } //end loop events

  outfile -> cd();

  hpulls_["pullX_unbinned"] -> Write();
  hpulls_["pullY_unbinned"] -> Write();
  hpulls_["pullZ_unbinned"] -> Write();
  hdiffs_["diffX_unbinned"] -> Write();
  hdiffs_["diffY_unbinned"] -> Write();
  hdiffs_["diffZ_unbinned"] -> Write();

  for (int i = cut_n_tracks; i < max_n_tracks; i ++){
    hpulls_[Form("pullX_%dTrks",i)]  -> Write();
    hpulls_[Form("pullY_%dTrks",i)]  -> Write();
    hpulls_[Form("pullZ_%dTrks",i)]  -> Write();
    hdiffs_[Form("diffX_%dTrks",i)]  -> Write();
    hdiffs_[Form("diffY_%dTrks",i)]  -> Write();
    hdiffs_[Form("diffZ_%dTrks",i)]  -> Write();
  }

  for (int i = 1; i < max_n_vertices; i ++){
    hpulls_[Form("pullX_%dVtx" ,i)]  -> Write();
    hpulls_[Form("pullY_%dVtx" ,i)]  -> Write();
    hpulls_[Form("pullZ_%dVtx" ,i)]  -> Write();
    hdiffs_[Form("diffX_%dVtx" ,i)]  -> Write();
    hdiffs_[Form("diffY_%dVtx" ,i)]  -> Write();
    hdiffs_[Form("diffZ_%dVtx" ,i)]  -> Write();
  }

  for (int i = 0; i < max_sum_pt; i += sum_pt_step){
    hpulls_[Form("pullX_%dsumPt",i)] -> Write();
    hpulls_[Form("pullY_%dsumPt",i)] -> Write();
    hpulls_[Form("pullZ_%dsumPt",i)] -> Write();
    hdiffs_[Form("diffX_%dsumPt",i)] -> Write();
    hdiffs_[Form("diffY_%dsumPt",i)] -> Write();
    hdiffs_[Form("diffZ_%dsumPt",i)] -> Write();
  }

  for (int i = 0; i < max_res; i ++){
    hpulls_[Form("pullX_%dRes",i)]   -> Write();
    hpulls_[Form("pullY_%dRes",i)]   -> Write();
    hpulls_[Form("pullZ_%dRes",i)]   -> Write();
  }
  
  outfile -> Close();  
  tree    -> Delete();

  return;
}

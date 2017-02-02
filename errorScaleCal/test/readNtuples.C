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

// set max n_tracks per sub vtx (vtx/2)
int max_n_tracks = 30;

void readNtuples(){
  
  TChain* tree = new TChain("errorScaleCal/pvTree"); 
  tree -> Add("calib_278820_newAlignment_ntuples.root/errorScaleCal/pvTree");

  TFile* outfile = TFile::Open("pulls_onefile.root","RECREATE");
  std::cout << "output file: " << outfile -> GetName() << std::endl;
  
  std::map<std::string, TH1F*> hpulls_      ;
  for (int i = 2; i < max_n_tracks; i ++){
    hpulls_[Form("pullX_%dTrks",i*2)] = new TH1F( Form("pullX_%dTrks",i*2) , Form("pullX_%dTrks",i*2), 500,  -10, 10. );
    hpulls_[Form("pullY_%dTrks",i*2)] = new TH1F( Form("pullY_%dTrks",i*2) , Form("pullY_%dTrks",i*2), 500,  -10, 10. );
    hpulls_[Form("pullZ_%dTrks",i*2)] = new TH1F( Form("pullZ_%dTrks",i*2) , Form("pullZ_%dTrks",i*2), 500,  -10, 10. );
//     hdiffs_[Form("diffX_%dTrks",i)] = outfile_->make<TH1F>( Form("diffX_%dTrks",i) , Form("diffX_%dTrks",i), 100,   -2,  2. );
//     hdiffs_[Form("diffY_%dTrks",i)] = outfile_->make<TH1F>( Form("diffY_%dTrks",i) , Form("diffY_%dTrks",i), 100,   -2,  2. );
//     hdiffs_[Form("diffZ_%dTrks",i)] = outfile_->make<TH1F>( Form("diffZ_%dTrks",i) , Form("diffZ_%dTrks",i), 100,   -2,  2. );
  }

  
  pvEvent* ev      = new pvEvent();
  tree -> SetBranchAddress( "event", &ev);

  int nentries = tree->GetEntries();
  std::cout << "Number of entries = " << nentries << std::endl;

 
  for (Int_t eventNo=0; eventNo < nentries; eventNo++)
  {
    Int_t IgetEvent   = tree   -> GetEvent(eventNo);
    
    unsigned int npv = ev->pvs.size();
    for (int ipv = 0; ipv < npv; ipv++){
      
      // select the pv        
      pvCand thePV = ev -> pvs.at(ipv);
      if (thePV.n_subVtx1 < 2 || thePV.n_subVtx1 >= max_n_tracks) continue;
          
      float errX = sqrt( pow(thePV.xErr_subVtx1,2) + pow(thePV.xErr_subVtx2,2) );
      hpulls_[Form("pullX_%dTrks", thePV.n_subVtx1*2)] ->  Fill( (thePV.x_subVtx1 - thePV.x_subVtx2) / errX );

      float errY = sqrt( pow(thePV.yErr_subVtx1,2) + pow(thePV.yErr_subVtx2,2) );
      hpulls_[Form("pullY_%dTrks", thePV.n_subVtx1*2)] ->  Fill( (thePV.y_subVtx1 - thePV.y_subVtx2) / errY );

      float errZ = sqrt( pow(thePV.zErr_subVtx1,2) + pow(thePV.zErr_subVtx2,2) );
      hpulls_[Form("pullZ_%dTrks", thePV.n_subVtx1*2)] ->  Fill( (thePV.z_subVtx1 - thePV.z_subVtx2) / errZ );

    }//end loop PV
  } //end loop events
  

  outfile           -> cd();
  for (int i = 2; i < max_n_tracks; i ++){
    hpulls_[Form("pullX_%dTrks",i*2)]  -> Write();
    hpulls_[Form("pullY_%dTrks",i*2)]  -> Write();
    hpulls_[Form("pullZ_%dTrks",i*2)]  -> Write();
  }
  
  outfile -> Close();  
  tree    -> Delete();
  return;
}


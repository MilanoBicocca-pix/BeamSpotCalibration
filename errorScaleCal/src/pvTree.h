#ifndef  pvTree_h
#define  pvTree_h

#include "TROOT.h"
#include "TMath.h"
#include <vector>
#include <string>



class PVcand {
public:

  Int_t   nTrks;    
  Int_t   ipos;    

  Int_t   n_subVtx1;    
  Float_t x_subVtx1;
  Float_t y_subVtx1;
  Float_t z_subVtx1;

  Float_t xErr_subVtx1;
  Float_t yErr_subVtx1;
  Float_t zErr_subVtx1;
  Float_t sumPt_subVtx1;

  Int_t   n_subVtx2;    
  Float_t x_subVtx2;
  Float_t y_subVtx2;
  Float_t z_subVtx2;

  Float_t xErr_subVtx2;
  Float_t yErr_subVtx2;
  Float_t zErr_subVtx2;
  Float_t sumPt_subVtx2;
  
  Float_t CL_subVtx1;
  Float_t CL_subVtx2;

  Float_t minW_subVtx1;
  Float_t minW_subVtx2;
  
  PVcand(){};
  virtual ~PVcand(){};

  ClassDef(PVcand,1)
};


class PVevent {
public:

  Int_t   runNumber;             
  Int_t   luminosityBlockNumber; 
  Int_t   eventNumber;           

  Int_t   nVtx;                    

  std::vector <PVcand>        pvs;         

  PVevent(){};
  virtual ~PVevent(){};

  ClassDef(PVevent,1)
};


#endif


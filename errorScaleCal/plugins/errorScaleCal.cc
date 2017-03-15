// -*- C++ -*-
//
// Package:    BeamSpotCalibration/errorScaleCal
// Class:      errorScaleCal
// 
/**\class errorScaleCal errorScaleCal.cc BeamSpotCalibration/errorScaleCal/plugins/errorScaleCal.cc

*/
//
// Original Author:  Sara Fiorendi
//         Created:  Mon, 13 Jun 2016 15:07:11 GMT
//
//


// system include files
#include <memory>
#include <algorithm>    // std::sort
#include <vector>       // std::vector
#include "TRandom.h"
#include "TTree.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "Geometry/Records/interface/GlobalTrackingGeometryRecord.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

#include "BeamSpotCalibration/errorScaleCal/src/pvTree.h"


//
// class declaration
//

class errorScaleCal : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit errorScaleCal(const edm::ParameterSet&);
      ~errorScaleCal();

      virtual void beginEvent();
      static  void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
      static  bool mysorter (reco::Track i, reco::Track j) { return (i.pt () > j.pt()); }



   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      edm::InputTag      pvsTag_                        ;
      edm::EDGetTokenT<reco::VertexCollection> pvsToken_;

      edm::InputTag      tracksTag_                        ;
      edm::EDGetTokenT<reco::TrackCollection>  tracksToken_;
      
      double minVtxNdf_      ;
      double minVtxWgt_      ;


      edm::Service<TFileService> outfile_;

      TH1F * h_diffX ;
      TH1F * h_diffY ;
      TH1F * h_diffZ ;
      TH1F * h_pullX ;
      TH1F * h_pullY ;
      TH1F * h_pullZ ;

      TH1F * h_ntrks ;
      TH1F * h_wTrks1 ;
      TH1F * h_wTrks2 ;
      TRandom rand;

      pvEvent event_;
      TTree* tree_;

      // ----------member data ---------------------------
};

errorScaleCal::errorScaleCal(const edm::ParameterSet& iConfig):
  pvsTag_           (iConfig.getParameter<edm::InputTag>("vtxCollection")), 
  pvsToken_         (consumes<reco::VertexCollection>(pvsTag_)), 
  tracksTag_        (iConfig.getParameter<edm::InputTag>("trackCollection")), 
  tracksToken_      (consumes<reco::TrackCollection>(tracksTag_)),
  minVtxNdf_        (iConfig.getUntrackedParameter<double>("minVertexNdf")), 
  minVtxWgt_        (iConfig.getUntrackedParameter<double>("minVertexMeanWeight"))
{
}


errorScaleCal::~errorScaleCal()
{
}


// ------------ method called for each event  ------------
void
errorScaleCal::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  beginEvent(); 
  // Fill general info
  event_.runNumber             = iEvent.id().run();
  event_.luminosityBlockNumber = iEvent.id().luminosityBlock();
  event_.eventNumber           = iEvent.id().event();


  edm::ESHandle<TransientTrackBuilder>            theB                ;
  edm::ESHandle<GlobalTrackingGeometry>           theTrackingGeometry ;
  iSetup.get<GlobalTrackingGeometryRecord>().get(theTrackingGeometry) ;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);

  edm::Handle<reco::VertexCollection> vertices; 
  iEvent.getByToken(pvsToken_, vertices);
  const reco::VertexCollection pvtx  = *(vertices.product())  ;    

  edm::Handle<reco::TrackCollection> tracks; 
  iEvent.getByToken(tracksToken_, tracks);
  
  event_.nVtx = pvtx.size();

  int counter = -1;
  for (reco::VertexCollection::const_iterator pvIt = pvtx.begin(); pvIt!=pvtx.end(); pvIt++)        
  {
    reco::Vertex iPV = *pvIt;
    counter++;
    if (iPV.isFake()) continue;
    reco::Vertex::trackRef_iterator trki;

    // vertex selection as in bs code
     if ( iPV.ndof() < minVtxNdf_ || (iPV.ndof()+3.)/iPV.tracksSize()< 2*minVtxWgt_ )  continue;

    reco::TrackCollection allTracks;
    reco::TrackCollection groupOne, groupTwo;
    for (trki  = iPV.tracks_begin(); trki != iPV.tracks_end(); ++trki) 
    {
      if (trki->isNonnull()){
        reco::TrackRef trk_now(tracks, (*trki).key());
        allTracks.push_back(*trk_now);
      }
    }
     
    // order with decreasing pt 
    std::sort (allTracks.begin(), allTracks.end(), mysorter);
    
    int ntrks = allTracks.size();
    h_ntrks -> Fill( ntrks );
    
    // discard lowest pt track
    uint even_ntrks;
    ntrks % 2 == 0 ? even_ntrks = ntrks : even_ntrks = ntrks - 1;
    
    // split into two sets equally populated 
    for (uint tracksIt =0 ;  tracksIt < even_ntrks; tracksIt = tracksIt+2)
    {
      reco::Track  firstTrk  = allTracks.at(tracksIt);      
      reco::Track  secondTrk = allTracks.at(tracksIt + 1);      
      double therand = rand.Uniform (0, 1);
      if (therand > 0.5) {
        groupOne.push_back(firstTrk);  
        groupTwo.push_back(secondTrk);        
      }    
      else {
        groupOne.push_back(secondTrk);  
        groupTwo.push_back(firstTrk);        
      }                              
      
    }
     
    if  (! (groupOne.size() >= 2 && groupTwo.size() >= 2) )   continue;

    float sumPt1 = 0, sumPt2=0;

    // refit the two sets of tracks
    std::vector<reco::TransientTrack> groupOne_ttks;
    groupOne_ttks.clear();
    for (reco::TrackCollection::const_iterator itrk = groupOne.begin(); itrk != groupOne.end(); itrk++)
    {
      reco::TransientTrack tmpTransientTrack = (*theB).build(*itrk); 
      groupOne_ttks.push_back(tmpTransientTrack);
      sumPt1 += itrk->pt(); 
    }

    AdaptiveVertexFitter pvFitter;
    TransientVertex pvOne = pvFitter.vertex(groupOne_ttks);
    if (!pvOne.isValid())                                          continue;

    reco::Vertex onePV = pvOne;    


    std::vector<reco::TransientTrack> groupTwo_ttks;
    groupTwo_ttks.clear();
    for (reco::TrackCollection::const_iterator itrk = groupTwo.begin(); itrk != groupTwo.end(); itrk++)
    {
      reco::TransientTrack tmpTransientTrack = (*theB).build(*itrk); 
      groupTwo_ttks.push_back(tmpTransientTrack);
      sumPt2 += itrk->pt(); 
    }
    TransientVertex pvTwo = pvFitter.vertex(groupTwo_ttks);
    if (!pvTwo.isValid())                                          continue;

    reco::Vertex twoPV = pvTwo;    


    float theminW1 = 1.;
    float theminW2 = 1.;
    for (std::vector<reco::TransientTrack>::const_iterator otrk  = pvOne.originalTracks().begin(); otrk != pvOne.originalTracks().end(); ++otrk) 
    {
      h_wTrks1 -> Fill( pvOne.trackWeight(*otrk));
      if (pvOne.trackWeight(*otrk) < theminW1) theminW1 = pvOne.trackWeight(*otrk); 
    } 
    for (std::vector<reco::TransientTrack>::const_iterator otrk  = pvTwo.originalTracks().begin(); otrk != pvTwo.originalTracks().end(); ++otrk) 
    {
      h_wTrks2 -> Fill( pvTwo.trackWeight(*otrk));
      if (pvTwo.trackWeight(*otrk) < theminW2) theminW2 = pvTwo.trackWeight(*otrk); 
    } 


    int half_trks = twoPV.nTracks();
    
    h_diffX -> Fill(twoPV.x() - onePV.x());
    h_diffY -> Fill(twoPV.y() - onePV.y());
    h_diffZ -> Fill(twoPV.z() - onePV.z());
    
    double errX = sqrt( pow(twoPV.xError(),2) + pow(onePV.xError(),2) );
    double errY = sqrt( pow(twoPV.yError(),2) + pow(onePV.yError(),2) );
    double errZ = sqrt( pow(twoPV.zError(),2) + pow(onePV.zError(),2) );

    h_pullX -> Fill( (twoPV.x() - onePV.x()) / errX );
    h_pullY -> Fill( (twoPV.y() - onePV.y()) / errY );
    h_pullZ -> Fill( (twoPV.z() - onePV.z()) / errZ );
     
    
    // fill ntuples
    pvCand thePV;
    thePV.ipos  = counter;
    thePV.nTrks = ntrks; 

    thePV.n_subVtx1 = half_trks;
    thePV.x_subVtx1 = onePV.x();
    thePV.y_subVtx1 = onePV.y();
    thePV.z_subVtx1 = onePV.z();

    thePV.xErr_subVtx1  = onePV.xError();
    thePV.yErr_subVtx1  = onePV.yError();
    thePV.zErr_subVtx1  = onePV.zError();
    thePV.sumPt_subVtx1 = sumPt1;

    thePV.n_subVtx2 = half_trks; 
    thePV.x_subVtx2 = twoPV.x();
    thePV.y_subVtx2 = twoPV.y();
    thePV.z_subVtx2 = twoPV.z();

    thePV.xErr_subVtx2  = twoPV.xError();
    thePV.yErr_subVtx2  = twoPV.yError();
    thePV.zErr_subVtx2  = twoPV.zError();
    thePV.sumPt_subVtx2 = sumPt2;
    
    thePV.CL_subVtx1 =  TMath::Prob(pvOne.totalChiSquared(),(int)(pvOne.degreesOfFreedom() ));
    thePV.CL_subVtx2 =  TMath::Prob(pvTwo.totalChiSquared(),(int)(pvTwo.degreesOfFreedom() ));
    
    thePV.minW_subVtx1 = theminW1;
    thePV.minW_subVtx2 = theminW2;

    
    event_.pvs.push_back(thePV);
   
  }
  
  tree_ -> Fill();

}


// ------------ method called once each job just before starting event loop  ------------
void 
errorScaleCal::beginJob()
{

  h_diffX = outfile_->make<TH1F>( "h_diffX"  , "h_diffX", 100,  -2, 2. );
  h_diffY = outfile_->make<TH1F>( "h_diffY"  , "h_diffY", 100,  -2, 2. );
  h_diffZ = outfile_->make<TH1F>( "h_diffZ"  , "h_diffZ", 100,  -2, 2. );

  h_pullX = outfile_->make<TH1F>( "h_pullX"  , "h_pullX", 500,  -10, 10. );
  h_pullY = outfile_->make<TH1F>( "h_pullY"  , "h_pullY", 500,  -10, 10. );
  h_pullZ = outfile_->make<TH1F>( "h_pullZ"  , "h_pullZ", 500,  -10, 10. );

  h_ntrks = outfile_->make<TH1F>( "h_ntrks"  , "h_ntrks", 100,  0, 100 );
  h_wTrks1 = outfile_->make<TH1F>( "h_wTrks1"  , "h_wTrks1", 1000, -1,  1 );
  h_wTrks2 = outfile_->make<TH1F>( "h_wTrks2"  , "h_wTrks2", 1000, -1,  1 );
  
  
  
  tree_ = outfile_-> make<TTree>("pvTree","pvTree");
  tree_ -> Branch("event" ,&event_, 64000,2);
}

// ------------ method called once each job just after ending the event loop  ------------
void 
errorScaleCal::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
errorScaleCal::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


void errorScaleCal::beginEvent()
{
  event_.pvs.clear();
  event_.nVtx       = -1;
}

//define this as a plug-in
DEFINE_FWK_MODULE(errorScaleCal);

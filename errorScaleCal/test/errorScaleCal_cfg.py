'''
cfg to produce ntuples for error scale calibration
here doing refit of tracks and vertices using latest alignment 
'''

import FWCore.ParameterSet.Config as cms

process = cms.Process("errorScaleCal")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
# process.GlobalTag.globaltag = '80X_dataRun2_Prompt_v8'

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')

process.load('Configuration/StandardSequences/Services_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/data/Run2016G/ZeroBias/ALCARECO/TkAlMinBias-PromptReco-v1/000/278/822/00000/0846B306-6F64-E611-A280-02163E011C84.root'
    )
)

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.GlobalTag.globaltag = '80X_dataRun2_2016LegacyRepro_Candidate_v1'

process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
# remove the following lines if you run on RECO files
process.TrackRefitter.src = 'ALCARECOTkAlMinBias'
process.TrackRefitter.NavigationSchool = ''


## PV refit
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import offlinePrimaryVertices 
process.offlinePrimaryVerticesFromRefittedTrks  = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesFromRefittedTrks.TrackLabel                                       = cms.InputTag("TrackRefitter") 
process.offlinePrimaryVerticesFromRefittedTrks.vertexCollections.maxDistanceToBeam              = 1
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxNormalizedChi2             = 20
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minSiliconLayersWithHits      = 5
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxD0Significance             = 5.0 
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minPixelLayersWithHits        = 2   




process.errorScaleCal = cms.EDAnalyzer('errorScaleCal',
			vtxCollection    	= cms.InputTag("offlinePrimaryVerticesFromRefittedTrks"),
			trackCollection		= cms.InputTag("TrackRefitter"),		
			minVertexNdf        = cms.untracked.double(10.),
			minVertexMeanWeight = cms.untracked.double(0.5)
)
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("ntuple_errorScaleCalibration.root"),	
                                   closeFileFast = cms.untracked.bool(False)
                                   )

process.p = cms.Path(process.offlineBeamSpot                        + 
                     process.TrackRefitter                          + 
                     process.offlinePrimaryVerticesFromRefittedTrks +
                     process.errorScaleCal)

# process.p = cms.Path(process.errorScaleCal)

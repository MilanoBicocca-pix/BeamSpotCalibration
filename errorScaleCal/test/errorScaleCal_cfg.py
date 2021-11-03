'''
cfg to produce ntuples for error scale calibration
here doing refit of tracks and vertices using latest alignment 
'''

import FWCore.ParameterSet.Config as cms

process = cms.Process("errorScaleCal")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')

process.load('Configuration/StandardSequences/Services_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

# Cannot work on ALCARECO because tracks associated to PV are Ref to generalTracks
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    'file:/eos/cms/tier0/store/data/Commissioning2021/ZeroBias/AOD/PromptReco-v1/000/346/455/00000/3c04cffb-f6e4-4ad8-9ccc-dba93e029330.root'
    )
)

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.GlobalTag.globaltag = '120X_dataRun3_Express_v2'
# process.GlobalTag.toGet.append(
# cms.PSet(
#   connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
#   record = cms.string("TrackerAlignmentRcd"),
#   tag = cms.string("TrackerAlignment_v24_offline")),
# )
# process.GlobalTag.toGet.append(
# cms.PSet(
#   connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
#   record = cms.string("TrackerAlignmentErrorExtendedRcd"),
#   tag = cms.string("TrackerAlignmentExtendedErrors_v10_offline_IOVs")),
# )


process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.TrackRefitter.src = 'generalTracks'
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
#                                       vtxCollection       = cms.InputTag("offlinePrimaryVerticesFromRefittedTrks"),
#                                       trackCollection     = cms.InputTag("TrackRefitter"),
                                       vtxCollection       = cms.InputTag("offlinePrimaryVertices"),
                                       trackCollection     = cms.InputTag("generalTracks"),
                                       minVertexNdf        = cms.untracked.double(10.),
                                       minVertexMeanWeight = cms.untracked.double(0.5)
)
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("ntuple_errorScaleCalibration_beammTestLHC_provaAOD.root"),
                                   closeFileFast = cms.untracked.bool(False)
                                   )

#process.p = cms.Path(process.offlineBeamSpot                        +
#                     process.TrackRefitter                          +
#                     process.offlinePrimaryVerticesFromRefittedTrks +
#                     process.errorScaleCal)

process.p = cms.Path(process.errorScaleCal)

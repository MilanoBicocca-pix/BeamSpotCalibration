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
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/0265e3de-0d42-4375-93f1-b0c4e442737c.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/05d4e531-3560-40bd-ba85-d18f4fa78981.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/079965e6-60f7-4dec-b033-a27170d1e8d7.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/0a370855-3510-4e0c-bb8d-3699e4de3af1.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/0be5dbbd-c94c-463f-bbe2-4229d44a529a.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/11203985-92a5-40eb-81d3-f9046f7946ed.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/1132d334-ed74-4d2c-99d7-301f6b2ddf3a.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/132d39da-7258-495f-95b8-485c168b3672.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/136e3c4b-80e2-48fe-af75-61ba61b653eb.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/151bc820-bb86-4f56-8e15-99cf67a74d2b.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/1757a926-9233-4896-ae76-b1a7ce043e2e.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/178b39fc-dc74-404a-a75d-2f4c13deb5e0.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/1b6d0b52-75c4-4684-9e96-e63dff4052f0.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/1dbb1696-4636-427f-8cfc-53e356721eed.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/22cbd905-6a6d-4632-888f-fe96c32ad40e.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/26a6115b-35ee-4e99-be88-0e5cdc9d0ad8.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/26f10358-8143-41f5-8845-dfec77914ec0.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/29391054-1d7f-43ab-a5f2-cdba0113d3ed.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/2ad49dce-42bc-4290-aba1-f81f9a080d34.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/2cb1e2ec-fb1c-4bf7-b0ac-3b39f58a410f.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/31b23154-5aab-4b5d-ba85-c2efdf3ee492.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/3355dac3-4fef-4d23-8f0a-526c59149a27.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/346ca2d6-7305-4fa8-8f6c-771e51f8345d.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/36ebc8fd-878d-4819-9b26-d0ef73251fea.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/39ad3a77-96bf-4772-b901-5b4fda5b6e1e.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/3aecac38-d3e6-4863-8d25-74a5506e735c.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/3d3697c7-4f48-4948-b482-2b30aa72a983.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/451a55b4-0107-4443-b272-9df933c8afe8.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/4a696f2e-459b-4d82-956a-23273757066b.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/4e495ec5-b0a6-4039-a0d7-ab2db34fb5aa.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/515f9612-f537-45c1-bdeb-10855a154303.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/54cb0557-e85c-4b21-a3da-7fd947ecc7bc.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/5918471d-9e91-4187-8992-c4c9cb79dd59.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/5d816a4e-a51a-428f-a80e-ea5f1be8c666.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/68877052-115f-4af6-b1d7-ebbe4c108947.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/70050653-4585-436a-a805-07bf942bf480.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/704bfd06-68ac-4e4d-9be7-59ce0fef0cb9.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/78149d1b-7975-40ad-a478-874821ff393b.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/793a3795-56d2-411b-a0ed-fabf7d4eb255.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/7a65dd92-e0bb-4ad3-8c28-3ee76401f571.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/7e1145a4-0074-4b8b-8f86-5364cd06f905.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/7e930523-3323-4980-baf4-69372c9cbcb3.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/8126968a-1a7d-474c-b406-65afd8449cb8.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/83343980-e098-474d-b175-037b437955dc.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/83b866f5-5f45-4b25-ba7a-e3a1429809c4.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/85502b9d-2565-49a4-a682-30e8dbbafb97.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/87e309ad-b2b1-487a-ab2b-cf877201ff07.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/88d94df7-091a-427d-b69b-38bab90a75be.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/8af9c538-e78c-4041-ab9d-1e62883f4524.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/8b39e3a0-99f6-47e3-8e21-eec67e3bd5ea.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/8bbad8a0-7462-4ade-a914-76c9e11593ff.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/8c151f10-daa3-4e5d-9a77-66997d6a5fca.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/8ccc9cfd-da90-41e6-b549-3d4b8d3657f1.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/955ce62e-3dcd-4477-a0de-51853db432e4.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/9737fccf-5919-4b1b-a8a3-b87b1a41fb61.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/9a196270-96d8-4372-9bfc-3b8a189e8800.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/a10906e5-e599-477a-8be9-370baf97a982.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/a27c4966-0c44-437c-9a1c-1c58b1ab3f05.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/aa176408-ad8a-499e-9560-71c11f6fea95.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/ad849abe-7738-42c8-a6e8-be2979e6096f.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/aeaac979-5909-4056-b821-f69439a7a07f.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/b2322206-0e95-4c13-8207-ac6428dc7687.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/b323fe55-6255-4b2a-9c2e-1bf752fca01f.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/b4eea1f5-a861-470f-85f2-3585e28c9982.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/b8e778b1-7a17-4c62-a3cb-61bd6f49f6b0.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/bc3801d1-c45f-4ff8-bb44-6d9915e7cdd5.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/c08f4b1c-e54c-4fcf-9e49-71c38ea7bfbd.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/c1023cc8-a294-4b35-9aa2-d6b96db64a28.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/c25ba9e5-3891-4024-aae9-6ac1e4d4875c.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/c3604280-2b9a-4b6b-8c85-dea55dff936c.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/c483d88c-cad1-4ce1-a763-0ddfd9ca0bd7.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/c4eae1a2-f078-494f-986d-93a8f08e5966.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/c91da725-676a-4af8-bfc9-a2575c635e43.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/ccd0e603-4265-4b1a-91e4-e47c10568b25.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/d3376308-f331-4515-a52c-96b15949e9a9.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/d9f34226-5916-4d0a-9f90-6b2a87a47ae0.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/d9fe6fd0-7764-46c5-82f9-611bd566dc1d.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/db9a24db-fdd2-4473-9561-e6e8e152d334.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/ddae7e43-c5c6-4f6f-a7be-8ac6cb9ae3b6.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/ddb76026-5c60-457b-bcce-e6194cd2f4c7.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/deb346c3-4ec3-429d-9337-f8578a1d60ef.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/dfcb6ee3-0858-4b30-8cbd-dcd68d96b771.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/dfeb5315-3337-480a-bb56-8430cc0abece.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/e3055edd-3b4a-4e97-b062-9e94df174baf.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/e33dc9fa-807b-4a85-8f5c-257b61c447ca.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/e936125e-53eb-4e71-bafe-c027cb550a1d.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/eb5f7620-8f16-4cf2-8d3b-394f3dbfae42.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/ef82c630-b1c1-4d2f-b20d-60735e1b5e57.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/f02b3d6e-5c22-4773-9b87-bec86d9c5519.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/f2d15bce-3f74-4368-be89-65a8db1ad490.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/f8f9630a-f09d-4a20-9d8b-045ba9a892ff.root',
'/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/fc2ae751-787a-446a-8afe-8b5ff7ee8cd5.root',
    )
)

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.GlobalTag.globaltag = '120X_dataRun3_Express_v2'

# Add conditions for trks/PVs refit
# preliminary offline BS
process.GlobalTag.toGet = cms.VPSet(
cms.PSet(
  connect = cms.string("sqlite_file:/afs/cern.ch/work/f/fbrivio/public/BeamSpot/PilotBeam2021/ExpressBeamSpot/BeamSpotObjects_2021_PilotBeams_LumiBased_v1.db"),
  record = cms.string("BeamSpotObjectsRcd"),
  tag = cms.string("BeamSpotObjects_2021_PilotBeams_LumiBased_v1")
  ),
## new alignement
cms.PSet(
  record = cms.string("TrackerAlignmentRcd"),
  tag = cms.string("TrackerAlignment_collisions21_v1")
  ),
## new APE
cms.PSet(
  record = cms.string("TrackerAlignmentErrorExtendedRcd"),
  tag = cms.string("TrackerAlignmentExtendedErrors_collisions21_v0")
  ),
## new SiPixel LA
cms.PSet(
  record = cms.string("SiPixelLorentzAngleRcd"),
  tag = cms.string("SiPixelLorentzAngle_phase1_38T_2021_v2")
  ),
## new SiPixel template DB object
cms.PSet(
  record = cms.string("SiPixelTemplateDBObjectRcd"),
  tag = cms.string("SiPixelTemplateDBObject_phase1_38T_2021_v2")
  ),
## new SiPixel 2D template DB object
cms.PSet(
  record = cms.string("SiPixel2DTemplateDBObjectRcd"),
  tag = cms.string("SiPixel2DTemplateDBObject_phase1_38T_2021_v2")
  ),
## new SiPixel GenErrors
cms.PSet(
  record = cms.string("SiPixelGenErrorDBObjectRcd"),
  tag = cms.string("SiPixelGenErrorDBObject_phase1_38T_2021_v2")
  )
)

process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.TrackRefitter.src = 'generalTracks'
#process.TrackRefitter.src = 'ALCARECOTkAlMinBias'
process.TrackRefitter.NavigationSchool = ''

## PV refit
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import offlinePrimaryVertices 
process.offlinePrimaryVerticesFromRefittedTrks            = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesFromRefittedTrks.TrackLabel = cms.InputTag("TrackRefitter") 

# Comment to use CMSSW default
#process.offlinePrimaryVerticesFromRefittedTrks.vertexCollections.maxDistanceToBeam              = 1
#process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxNormalizedChi2             = 20
#process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minSiliconLayersWithHits      = 5
#process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxD0Significance             = 5.0 
#process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minPixelLayersWithHits        = 2   #

process.errorScaleCal = cms.EDAnalyzer('errorScaleCal',
                                       vtxCollection       = cms.InputTag("offlinePrimaryVerticesFromRefittedTrks"),
                                       trackCollection     = cms.InputTag("TrackRefitter"),
#                                       vtxCollection       = cms.InputTag("offlinePrimaryVertices"),
#                                       trackCollection     = cms.InputTag("generalTracks"),
                                       minVertexNdf        = cms.untracked.double(10.),
                                       minVertexMeanWeight = cms.untracked.double(0.5)
)
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("ntuple_errorScaleCalibration_beammTestLHC_ExpressPhysics_FEVT_newTkAl_newAPE_346512.root"),
                                   closeFileFast = cms.untracked.bool(False)
                                   )

process.p = cms.Path(process.offlineBeamSpot                        +
                     process.TrackRefitter                          +
                     process.offlinePrimaryVerticesFromRefittedTrks +
                     process.errorScaleCal)

#process.p = cms.Path(process.errorScaleCal)

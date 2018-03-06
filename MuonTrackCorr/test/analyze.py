# define basic process
import FWCore.ParameterSet.Config as cms
import os
process = cms.Process("L1Tracklet")
 

# import standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff') ## this needs to match the geometry you are running on
process.load('Configuration.Geometry.GeometryExtended2023D17_cff')     ## this needs to match the geometry you are running on

process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgradePLS3', '')


# input
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

Source_Files = cms.untracked.vstring(
# "/store/relval/CMSSW_9_1_1/RelValSingleMuPt10Extended/GEN-SIM-DIGI-RAW/91X_upgrade2023_realistic_v1_D17-v1/10000/0A0A27B4-153F-E711-ABC3-0025905A60C6.root"
"/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/8C0306E6-4226-E711-A742-24BE05C68681.root"

)
process.source = cms.Source("PoolSource", fileNames = Source_Files,
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop l1tEMTFHitExtras_simEmtfDigis_CSC_HLT',
        'drop l1tEMTFHitExtras_simEmtfDigis_RPC_HLT',
        'drop l1tEMTFTrackExtras_simEmtfDigis__HLT',
    )
)


# remake stubs 
# ===> IMPORTANT !!! stub window tuning as is by default in CMSSW is incorrect !!! <===
process.load('L1Trigger.TrackTrigger.TrackTrigger_cff')
from L1Trigger.TrackTrigger.TTStubAlgorithmRegister_cfi import *
process.TTClusterStub = cms.Path(process.TrackTriggerClustersStubs)


# L1 tracking
process.load("L1Trigger.TrackFindingTracklet.L1TrackletTracks_cff")
process.TTTracks = cms.Path(process.L1TrackletTracks)                         #run only the tracking (no MC truth associators)
process.TTTracksWithTruth = cms.Path(process.L1TrackletTracksWithAssociators) #run the tracking AND MC truth associators)


# # output module
# process.out = cms.OutputModule( "PoolOutputModule",
#                                 fileName = cms.untracked.string("Tracklets.root"),
#                                 fastCloning = cms.untracked.bool( False ),
#                                 outputCommands = cms.untracked.vstring('drop *',
#                                                                        'keep *_TTTrack*_Level1TTTracks_*', 
# #                                                                       'keep *_TTCluster*_*_*',
# #                                                                       'keep *_TTStub*_*_*'
# )
# )
# process.FEVToutput_step = cms.EndPath(process.out)

# process.schedule = cms.Schedule(process.TTClusterStub,process.TTTracksWithTruth,process.FEVToutput_step)


process.Ntuplizer = cms.EDAnalyzer("Ntuplizer",
    # L1MuonPosInputTag = cms.InputTag("simGmtStage2Digis", "imdMuonsEMTFPos", "HLT"),
    # L1MuonNegInputTag = cms.InputTag("simGmtStage2Digis", "imdMuonsEMTFNeg", "HLT"),
    # L1TrackInputTag   = cms.InputTag("TTStubsFromPhase2TrackerDigis", "ClusterAccepted", "HLT"), # or ClusterInclusive ?
    L1MuonEMTFInputTag  = cms.InputTag("simEmtfDigis"),
    L1TrackInputTag     = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks"),
    GenParticleInputTag = cms.InputTag("genParticles"),
)

process.Ntuples = cms.Path(
    process.Ntuplizer
)


process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.L1simulation_step = cms.Path(process.SimL1Emulator)

outputFileName = "TkMuNtuple.root"
process.TFileService = cms.Service('TFileService',
    fileName = cms.string(outputFileName)
)


# process.schedule = cms.Schedule(process.TTClusterStub, process.TTTracksWithTruth, process.L1simulation_step, process.Ntuples)
process.schedule = cms.Schedule(process.TTTracks, process.L1simulation_step, process.Ntuples)


##### screen output stuff
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
# process.MessageLogger.cerr.FwkReport.reportEvery = 1000
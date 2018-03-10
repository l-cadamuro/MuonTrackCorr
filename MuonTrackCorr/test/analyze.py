# define basic process
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import os
process = cms.Process("L1MuTkCorr")
 

# import standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff') ## this needs to match the geometry you are running on
process.load('Configuration.Geometry.GeometryExtended2023D17_cff')     ## this needs to match the geometry you are running on
# the above is the default geometry from L1TT. The one below is a test
# process.load('Configuration.Geometry.GeometryExtended2023D21Reco_cff') ## this needs to match the geometry you are running on
# process.load('Configuration.Geometry.GeometryExtended2023D21_cff')     ## this needs to match the geometry you are running on

process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgradePLS3', '')
# process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2023_realistic_v9', '')


# input
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

###### cmd line opts for batch
options = VarParsing.VarParsing ('analysis')
options.inputFiles = []
options.outputFile = 'TkMuNtuple.root'
options.parseArguments()

if options.inputFiles:
  Source_Files = cms.untracked.vstring(options.inputFiles)
else:
  Source_Files = cms.untracked.vstring(
    '/store/group/l1upgrades/L1MuTrks/MuMu_2to2000_flatOneOverPt_8Mar2018/output/MuMu_FEVTDEBUGHLT_0.root',
  )

process.source = cms.Source("PoolSource", fileNames = Source_Files,
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop l1tEMTFHitExtras_simEmtfDigis_CSC_HLT',
        'drop l1tEMTFHitExtras_simEmtfDigis_RPC_HLT',
        'drop l1tEMTFTrackExtras_simEmtfDigis__HLT',
        'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
        'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
        'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
        'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
        'drop l1tEMTFTrack2016s_simEmtfDigis__HLT',
    ),
    ## lines below are needed for my private production, since events from different files get the same run/lumi
    noEventSort = cms.untracked.bool(True),
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
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


# process.load('Configuration.StandardSequences.SimL1Emulator_cff')
# process.L1simulation_step = cms.Path(process.SimL1Emulator)

# from L1Trigger.L1TMuonEndCap.customise_Phase2C2 import customise as customise_Phase2C2
# process = customise_Phase2C2(process)

from L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi import *
process.simEmtfDigis = simEmtfDigis
process.EMTFemu = cms.Path(process.simEmtfDigis)

# outputFileName = "TkMuNtuple.root"
process.TFileService = cms.Service('TFileService',
    fileName = cms.string(options.outputFile)
)


# process.schedule = cms.Schedule(process.TTClusterStub, process.TTTracksWithTruth, process.L1simulation_step, process.Ntuples)
# process.schedule = cms.Schedule(process.TTTracks, process.L1simulation_step, process.Ntuples)
process.schedule = cms.Schedule(process.TTTracks, process.EMTFemu, process.Ntuples)


##### screen output stuff
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
if options.inputFiles: # likely a cluster job
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000
else: # likely a local test
    process.MessageLogger.cerr.FwkReport.reportEvery = 1

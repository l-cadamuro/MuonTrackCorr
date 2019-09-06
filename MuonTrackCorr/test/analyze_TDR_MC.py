# define basic process
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import os


# process = cms.Process("L1MuTkCorr")
from Configuration.StandardSequences.Eras import eras
process = cms.Process("L1", eras.Phase2_timing)
 

# import standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.Geometry.GeometryExtended2023D41Reco_cff') ## this needs to match the geometry you are running on
process.load('Configuration.Geometry.GeometryExtended2023D41_cff')     ## this needs to match the geometry you are running on
# the above is the default geometry from L1TT. The one below is a test
# process.load('Configuration.Geometry.GeometryExtended2023D21Reco_cff') ## this needs to match the geometry you are running on
# process.load('Configuration.Geometry.GeometryExtended2023D21_cff')     ## this needs to match the geometry you are running on

process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgradePLS3', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '103X_upgrade2023_realistic_v2', '')
print process.GlobalTag.globaltag
# process.GlobalTag = GlobalTag(process.GlobalTag, '100X_upgrade2023_realistic_v1', '')
# process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2023_realistic_v9', '')


# input
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

###### cmd line opts for batch
options = VarParsing.VarParsing ('analysis')
options.inputFiles = []
options.outputFile = 'TkMuNtuple_eras_muonly_wtkmus.root'
options.register ('promptMuOnly',
                  1, # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "Save only prompt mu (0 for false, 1 for true)")
options.register ('muFromTausOnly',
                  0, # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "Save only mu from tau decays (0 for false, 1 for true) - used for tau to 3mu studies")
options.register ('saveTauTo3Mu',
                  0, # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "Save the gen taus that decay to 3mu (0 for false, 1 for true) - used for tau to 3mu studies")

options.parseArguments()

promptMuOnly = False if options.promptMuOnly == 0 else True
print "... saving only prompt muons? ", promptMuOnly

muFromTausOnly = False if options.muFromTausOnly == 0 else True
print "... saving only prompt muons? ", muFromTausOnly

saveTauTo3Mu = False if options.saveTauTo3Mu == 0 else True
print "... saving taus to 3mu? ", saveTauTo3Mu
    
if options.promptMuOnly == 1 and options.muFromTausOnly == 1:
    raise RuntimeError('GEN LEVEL muon options conflict: asking to save "only prompt" and "only from tau"')

if options.inputFiles:
  Source_Files = cms.untracked.vstring(options.inputFiles)
else:
  Source_Files = cms.untracked.vstring(
    # '/store/group/l1upgrades/L1MuTrks/MuMu_2to2000_flatOneOverPt_8Mar2018/output/MuMu_FEVTDEBUGHLT_0.root',
    # '/store/relval/CMSSW_9_3_7/RelValZMM_14/GEN-SIM-DIGI-RAW/PU25ns_93X_upgrade2023_realistic_v5_2023D17PU200-v1/10000/8E2F2F0B-2931-E811-8278-E0071B74AC10.root'
    # '/store/mc/PhaseIIFall17D/SingleMu_FlatPt-2to100/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/008F844C-0E43-E811-A851-A0369FE2C1E4.root',
    # '/store/mc/PhaseIIFall17D/SingleNeutrino/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/80000/00157B11-405C-E811-89CA-0CC47AFB81B4.root'
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_0.root'
    '/store/mc/PhaseIITDRSpring19DR/Nu_E10-pythia8-gun/GEN-SIM-DIGI-RAW/PU200_106X_upgrade2023_realistic_v3-v3/70001/1622E6AA-FCDD-9A4F-8F6A-104DA786EE03.root'
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_0.root',
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_1.root',
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_2.root',
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_3.root',
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_4.root',
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_5.root',
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_6.root',
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_7.root',
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_8.root',
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_9.root',
    #'/store/group/l1upgrades/L1MuTrks/Ds_to_Tau3Mu_pythia8_5Apr2019_5MEvts/output/Tau3Mu_10.root',
  )

process.source = cms.Source("PoolSource", fileNames = Source_Files,
    inputCommands = cms.untracked.vstring(
        'keep *',
    #    'drop l1tEMTFHitExtras_simEmtfDigis_CSC_HLT',
    #    'drop l1tEMTFHitExtras_simEmtfDigis_RPC_HLT',
    #    'drop l1tEMTFTrackExtras_simEmtfDigis__HLT',
    #    'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
    #    'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
    #    'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
    #    'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
    #    'drop l1tEMTFTrack2016s_simEmtfDigis__HLT',
    #    'drop l1tHGCalTowerMapBXVector_hgcalTriggerPrimitiveDigiProducer_towerMap_HLT'
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
    L1EMTFHitInputTag   = cms.InputTag("simEmtfDigis"),
    L1TrackInputTag     = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks"),
    GenParticleInputTag = cms.InputTag("genParticles"),
    TkMuInputTag        = cms.InputTag("L1TkMuons"),
    TkMuStubInputTag    = cms.InputTag("L1TkMuonStub"),
    save_all_L1TTT      = cms.bool(True),
    prompt_mu_only      = cms.bool(promptMuOnly),
    mu_from_tau_only    = cms.bool(muFromTausOnly),
    save_tau_3mu        = cms.bool(saveTauTo3Mu),
)

process.Ntuples = cms.Path(
    process.Ntuplizer
)


process.PrintMuons = cms.EDAnalyzer("PrintMuons",
    emtfTrkToken = cms.InputTag("simEmtfDigis"),
    emtfRegToken = cms.InputTag("simEmtfDigis", "EMTF"),
)
process.PrintMus = cms.Path(
    process.PrintMuons
)


# process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
# process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')

# process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')
# process.hgcl1tpg_step = cms.Path(process.hgcalTriggerPrimitives)

# process.load('SimCalorimetry.EcalEBTrigPrimProducers.ecalEBTriggerPrimitiveDigis_cff')
# process.EcalEBtp_step = cms.Path(process.simEcalEBTriggerPrimitiveDigis)

process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.L1simulation_step = cms.Path(process.SimL1Emulator)

process.load('L1Trigger.L1TTrackMatch.L1TkMuonProducer_cfi')
process.L1MuTkMatch_step = cms.Path(process.L1TkMuons)

process.load('L1Trigger.L1TTrackMatch.L1TkMuonStubProducer_cfi')
process.L1TkMuStubMatch_step = cms.Path(process.L1TkMuonStub)

# from L1Trigger.L1TMuonEndCap.customise_Phase2C2 import customise as customise_Phase2C2
# process = customise_Phase2C2(process)

# from L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi import *
# process.simEmtfDigis = simEmtfDigis
# process.EMTFemu = cms.Path(process.simEmtfDigis)

# outputFileName = "TkMuNtuple.root"
process.TFileService = cms.Service('TFileService',
    fileName = cms.string(options.outputFile)
)

# process.SimL1TMuon = cms.Sequence(process.SimL1TMuonCommon+process.simTwinMuxDigis+process.simBmtfDigis+process.simEmtfDigis+process.simOmtfDigis+process.simGmtCaloSumDigis+process.simGmtStage2Digis+process.me0TriggerPseudoDigiSequence)
from L1Trigger.L1TMuon.simDigis_cff import *
process.SimL1TMuon = cms.Sequence(SimL1TMuon)
process.Muons = cms.Path(process.SimL1TMuon)

## 12 Ott 2018 : Luca : revert manually the TkMu input from kBMTF to BMTF to avoid to run the kBMTF in the sequence
process.L1TkMuons.L1BMTFInputTag  = cms.InputTag("simBmtfDigis","BMTF")

# process.schedule = cms.Schedule(process.TTClusterStub, process.TTTracksWithTruth, process.L1simulation_step, process.Ntuples)
# process.schedule = cms.Schedule(process.EcalEBtp_step,process.hgcl1tpg_step, process.TTTracks, process.L1simulation_step, process.Ntuples)
# process.schedule = cms.Schedule(process.TTTracks, process.Muons, process.L1MuTkMatch_step, process.Ntuples)
process.schedule = cms.Schedule(process.TTTracks, process.Muons, process.L1MuTkMatch_step, process.L1TkMuStubMatch_step, process.Ntuples)
# process.schedule = cms.Schedule(process.PrintMus, process.TTTracks, process.Muons, process.L1MuTkMatch_step, process.Ntuples)


# process.schedule = cms.Schedule(process.TTTracks, process.EMTFemu, process.Ntuples)


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


#from L1Trigger.L1TMuonEndCap.customise_Phase2 import customise as customise_Phase2  
#process = customise_Phase2(process)

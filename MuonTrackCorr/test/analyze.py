import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms
process = cms.Process("TkMuCorr")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = '90X_upgrade2023_realistic_v9'

# SingleMu_FlatPt-8to100/PhaseIISpring17D-NoPU_90X_upgrade2023_realistic_v9-v1/GEN-SIM-DIGI-RAW
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        "/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/8C0306E6-4226-E711-A742-24BE05C68681.root"
    )
)

outputFileName = "TkMuNtuple.root"
process.TFileService = cms.Service('TFileService',
    fileName = cms.string(outputFileName)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.Ntuplizer = cms.EDAnalyzer("Ntuplizer",
    L1MuonPosInputTag = cms.InputTag("simGmtStage2Digis", "imdMuonsEMTFPos", "HLT"),
    L1MuonNegInputTag = cms.InputTag("simGmtStage2Digis", "imdMuonsEMTFNeg", "HLT"),
    L1TrackInputTag   = cms.InputTag("TTStubsFromPhase2TrackerDigis", "ClusterAccepted", "HLT"), # or ClusterInclusive ?
)

process.p = cms.Path(
    process.Ntuplizer
)
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
    input = cms.untracked.int32(2000)
)

Source_Files = cms.untracked.vstring(
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/8C0306E6-4226-E711-A742-24BE05C68681.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/1E927703-4326-E711-9EC9-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/84ABC6F3-4226-E711-BDC3-24BE05C63681.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/063B7709-4326-E711-A2AF-24BE05C68681.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/16619DE4-4226-E711-B865-E0071B740D80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/3C5C3706-4326-E711-8090-5065F381D2E2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/EAD17DFB-4226-E711-A811-24BE05C636C2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/BA2096E7-4226-E711-B292-24BE05C3FBB1.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/7E1EDC07-4326-E711-B794-4C79BA180D49.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/AC05AD08-4326-E711-A574-4C79BA320451.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/289F5A13-4326-E711-9FF4-5065F3811272.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/B018F607-4326-E711-82E8-4C79BA3204B1.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/042D2403-4326-E711-94EC-5065F37D1132.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/586D9D09-4326-E711-964B-24BE05C656C2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/F43BC80F-4326-E711-BE6B-4C79BA320485.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/4E4D347D-4926-E711-A43A-E0071B740D80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/BA15328C-4926-E711-BA1A-24BE05CEFB41.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/B2C3728C-4926-E711-ADDC-24BE05CEFB41.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/2E8EADB5-4926-E711-BC98-A0000620FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/4A1BE7AA-4926-E711-9A5B-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/DAF90082-4926-E711-BEE9-E0071B6C9DD0.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/DCC6EFA0-4926-E711-A790-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/F035C3AE-4926-E711-BE53-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/A2D0E995-4926-E711-B0CC-5065F37D7142.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/E849B99D-4926-E711-8661-5065F381D1E2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/9C6C207E-4926-E711-BA5D-24BE05C656A1.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/0833B49E-4926-E711-BEA0-5065F37D90C2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/F4014BA2-4926-E711-92E7-5065F37D7142.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/A68AAFB2-4926-E711-B16D-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/727E00AC-4926-E711-BC66-24BE05C696F2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/C409DB9E-4926-E711-AB55-24BE05C31802.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/EEE89AA8-4926-E711-B3B2-4C79BA260AFD.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/2832FF6C-4D26-E711-A9D6-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/CE83F5A5-4926-E711-8331-5065F381E182.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/0AC074AE-4926-E711-8712-4C79BA3203F5.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/FE6C2450-4D26-E711-A85B-24BE05C63681.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/3C8B6A67-4D26-E711-8455-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/F25F8C74-4D26-E711-BEBB-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/BEBEE879-4D26-E711-9763-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/340AE58E-4D26-E711-A096-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/D48E5F86-4D26-E711-9767-24BE05C6B7C2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/2EC94971-4D26-E711-B155-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/64372AA1-4D26-E711-A468-24BE05C60802.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/D6F6DB90-4D26-E711-AE11-5065F37D8162.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/604C6578-4D26-E711-9A64-24BE05BD0F32.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/C067826C-4D26-E711-BA3B-5065F38192C2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/C470B077-4D26-E711-91C1-24BE05C4E8E2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/5C0D0C97-4D26-E711-925F-4C79BA18182B.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/F6D1B97E-4F26-E711-9AF5-E0071B7AC5D0.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/E07C63B9-5326-E711-8BA4-E0071B7A08F0.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/8825F4E6-5326-E711-80EE-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/D0CC78E6-5326-E711-87DF-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/AEBA42BA-5326-E711-8C00-24BE05C6E571.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/14F582CF-5326-E711-836D-5065F37D21E2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/F66ED8D2-5326-E711-8412-5065F38112A2.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/CEF9BDF3-5326-E711-B709-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/1CC4AEF9-5326-E711-95B8-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/4CC218D5-5326-E711-BE8D-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/447C21D4-5326-E711-8744-5065F381B222.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/580759D5-5326-E711-A7A0-4C79BA1813A9.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/D46AE9EC-5326-E711-BFF8-5065F37D0132.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/8693ECD7-5326-E711-99D3-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/063545D6-5326-E711-B3D7-5065F37D8152.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/C0F951DC-5326-E711-9F49-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/846F38DA-5326-E711-A61B-5065F37D5172.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/92C11404-7526-E711-A9F4-A0000420FE80.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/C61920AB-D225-E711-AF03-0025907DE2A0.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/8E575B25-E025-E711-84B2-0CC47A0AD792.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/06FEAF34-E025-E711-BF53-0CC47A0AD476.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/726B3021-E025-E711-9F4C-0CC47A0AD63E.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/6219FD87-E625-E711-9853-00259075D714.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/6EE80E86-E725-E711-B2C1-0025907859B8.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/D49C8B81-E625-E711-BCE3-0CC47A57CD00.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/0E743386-E725-E711-A710-0025907859B8.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/1493CC7C-E725-E711-A323-003048CB7B30.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/78E3227C-E725-E711-8905-003048CB7B30.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/D6200F86-E725-E711-9FEB-0025907859B8.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/488FC425-EE25-E711-A506-0025907859B8.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/5C026030-EE25-E711-9D35-0025907D24F0.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/A691AC23-EE25-E711-B1BF-0CC47A0AD630.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/5C47E2B3-F325-E711-A132-002590812700.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/CE9E18BC-FA25-E711-B6A9-00259029E714.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/1A98CBAF-FA25-E711-BDBA-0025907D2212.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/9ABA2BA8-FA25-E711-A110-0CC47A0AD630.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/F63EE179-0126-E711-8162-0025901AEDA4.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/BC2BBC78-0126-E711-BF43-0025901AC3FE.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/10C4732E-0226-E711-9926-002590D9D8BA.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/E69413CE-0726-E711-B88B-0025907DE2A0.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/360D24CD-0726-E711-819F-0CC47AA53D76.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/7406ED20-0E26-E711-9000-0CC47AA53D46.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/20814EC1-1C26-E711-B6BA-0CC47A0AD6C4.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/82C12EAC-2226-E711-B7E4-0CC47AB0B828.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/EA86A0B7-2226-E711-BC9A-0025901AC404.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/54813A81-2826-E711-9217-0CC47A57D164.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/98318487-2F26-E711-BB1C-002590D9D8BE.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/3E999554-4D26-E711-B535-002590FD5A3A.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/D21729AA-6026-E711-A461-0CC47A57CE00.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/70000/388EE055-6726-E711-A3EE-002590FD5A48.root',
    '/store/mc/PhaseIISpring17D/SingleMu_FlatPt-8to100/GEN-SIM-DIGI-RAW/NoPU_90X_upgrade2023_realistic_v9-v1/80000/B6E6E4A4-9E29-E711-8DB8-0CC47AA53D82.root',
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
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

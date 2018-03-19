# MuonTrackCorr

## Install instructions

From the [PhaseII L1 twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TPhase2Instructions)

```
cmsrel CMSSW_10_0_0
cd CMSSW_10_0_0/src
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline phase2-l1t-integration-CMSSW_10_0_0
git cms-merge-topic -u cms-l1t-offline:l1t-phase2-v2.2
#
# Tracklet Tracks
#
git remote add skinnari git@github.com:rekovic/cmssw.git
git fetch skinnari
git cms-merge-topic -u skinnari:Tracklet_10X_10-0-1

git cms-addpkg L1Trigger/L1TCommon
# the following is to fix a bug in EMTF LCTs until the PR num.21933 does get included in the central code
git cherry-pick a129aff3892c613999d8d1bf1ede47018949d607
git-cms-addpkg L1Trigger/CSCTriggerPrimitives

# and finally my code
git clone https://github.com/l-cadamuro/MuonTrackCorr
```

### Install PhaseII private emulator
To install the private development version for the PhaseII from [here](https://github.com/jiafulow/L1TriggerSep2016), add the following lines:
```
cd CMSSW_10_0_0/src
cmsenv
cd CMSSW_10_0_0/tmp
git clone -b phase2-develop git@github.com:jiafulow/L1TriggerSep2016.git L1Trigger
git clone -b l1t-integration-CMSSW_9_4_0 git@github.com:jiafulow/DataFormatsSep2016.git DataFormats
cp -r L1Trigger/L1TMuonEndCap ../src/L1Trigger
cp -r DataFormats/L1TMuon ../src/DataFormats
```

Run the compilation. Likely there will be some incompatibilities between the CMSSW DataFormats and the updated ones. To just run to check all errors do ``scram b --keep-going -k 24``, look at the error messages and compile the corresponding offending lines in the code.
For example, based on tag ``l1t-phase2-v2.2`` you'll need to replace ll. 164 (``if (stub == hit.CSC_LCTDigi()) return true;``) of ``L1Trigger/L1TMuon/src/Phase2/L1TDisplacedMuonStubRecovery.cc`` with ``return true;`` since ``CSC_LCTDigi`` is not defined in the replaced CSC DataFormat.

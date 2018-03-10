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


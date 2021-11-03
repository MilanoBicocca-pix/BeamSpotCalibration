# BeamSpotCalibration

**How to use the package**
```
cmsrel CMSSW_12_0_3  
cd CMSSW_12_0_3/src  
cmsenv  
git clone git@github.com:MilanoBicocca-pix/BeamSpotCalibration.git BeamSpotCalibration 
cd BeamSpotCalibration/errorScaleCal

scram b -j 10
cd test
```

To produce the ntuples, just run
```
cmsRun errorScaleCal_cfg.py
```

Modify the cfg file errorScaleCal_cfg.py in order to aviud the track/vertex refitting if it's not needed.

To analyze the ntuples and produce the resolution and pull plots:
```
root -l readNtuples.C

mkdir pull_resolution_plots
python fitPulls.py
```

Make sure to use a consistent PV selection in the ntuple reader and in the beamspot fit (e.g., Legacy or HP workflow).

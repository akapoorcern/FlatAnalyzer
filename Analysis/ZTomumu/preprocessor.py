from asyncio import events
from modules.corrections import SFevaluator, GetBTagSF, ApplyJetCorrections, GetBtagEff, AttachMuonSF, AttachElectronSF, AttachPerLeptonFR, GetPUSF, ApplyRochesterCorrections, ApplyJetSystematics, AttachPSWeights, AttachPdfWeights, AttachScaleWeights, GetTriggerSF


def preprocess(pars, events, AttachSF=False):
    import modules.ExpressoTools as ET
    import awkward as ak
    import numpy as np
    ###################################
    dataset,isData,histAxisName,year,xsec,sow=pars['dataset'],pars['isData'],pars['histAxisName'],pars['year'],pars['xsec'],pars['sow']
    #events['nEvents']=nEvents
    ################################### Start writing your preprocessor below -> for creating new branches on top of the ones already present in the NanoAOD
    ## some variables are auto available picked up from the sample json
    ## The isData variable is true or false depending on if you are operating on data or mc
    ## The xsec has the xsec value, sow has sum of gen weights
    ## histAxisName is the name of the sample from json (will be used as legends for plots)
    
    if not isData:
        isgentau=abs(events.GenPart.pdgId)==15 # example of creating a mask -> a jagged boolean
        events["GenTaus"]=events.GenPart[isgentau] # like creating a new branch -> this branch is later available

        #let's look at another example
        isgenmu=abs(events.GenPart.pdgId)==13
        events["GenMuons"]=events.GenPart[isgenmu]

        isgenele=abs(events.GenPart.pdgId)==11
        events["GenEles"]=events.GenPart[isgenele]

        isgenpho=abs(events.GenPart.pdgId)==22
        events["GenPhos"]=events.GenPart[isgenpho]
    
        nTauEv = ak.num(events["GenTaus"])
        print(f"SJ!!! inside preprocessor.py, ")


    events["Muon","pt"]=ApplyRochesterCorrections(year, events["Muon"], isData, var='nominal')
    AttachMuonSF(events,"Muon",year=year)
    events["recoMu"]=events.Muon[(events.Muon.mediumId==True) &
                                 (events.Muon.pt > 30) &
                                 (abs(events.Muon.eta)<2.4) &
                                 (events.Muon.pfIsoId>=3)]
    events["Photon","cutBasedBitmap"]=events.Photon.vidNestedWPBitmap # adding because my nano is v9 and the name is vidNestedWPBitmap
    events["recoPho"]=events.Photon[(events.Photon.cutBasedBitmap >=2) & (events.Photon.pt > 10) & (abs(events.Photon.eta)<2.5)]

        
    ################################### Keep the return line as is
    return events

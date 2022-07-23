import os
import argparse

import submit

samples_to_submit = {
    "Training": {
        "HWWPrivate": {
            "subsamples": [
                "BulkGravitonToHHTo4W_JHUGen_MX-600to6000_MH-15to250_v2_ext1",
                "BulkGravitonToHHTo4W_JHUGen_MX-600to6000_MH-15to250_v2",
                "JHUVariableWMass_part1",
                "JHUVariableWMass_part2",
                "JHUVariableWMass_part3",
            ],
            "files_per_job": 20,
            "label": "_H_VV",
            "njets": 2,
        },
        # add more stats of varied mH sample (need to submit)
        # add hh 190 sample (resubmitted miniaod)
        "QCD": {
            "subsamples": [
                "QCD_Pt_300to470",
                "QCD_Pt_470to600",  # probably need to change chunk size because lots of memory errors
                "QCD_Pt_600to800",
                "QCD_Pt_800to1000",
                "QCD_Pt_1000to1400",
            ],
            "files_per_job": 1,
            "label": "_QCD",
            "njets": 1,
            "maxchunks": 1,
        },
        "WJetsToQQ": {
            "subsamples": [
                "WJetsToQQ_HT-400to600",
                "WJetsToQQ_HT-600to800",
                "WJetsToQQ_HT-800toInf",
            ],
            "files_per_job": 2,
            "label": "_VJets",
            "njets": 1,
            "maxchunks": 10,
        },
        "WJetsToLNu": {
            "subsamples": [
                "WJetsToLNu_HT-200To400",
                "WJetsToLNu_HT-400To600",
                "WJetsToLNu_HT-600To800",
                "WJetsToLNu_HT-800To1200",
                "WJetsToLNu_HT-1200To2500",
                "WJetsToLNu_HT-2500ToInf",
            ],
            "files_per_job": 5,
            "label": "_VJets",
            "njets": 1,
        },
        "TTbar": {
            "subsamples": ["TTToSemiLeptonic", "TTToHadronic"],
            "files_per_job": 2,
            "label": "_Top",
            "njets": 2,
            "maxchunks": 2,
        },
        "JetHT2017": {
            # "subsamples": ["JetHT_Run2017B","JetHT_Run2017C","JetHT_Run2017D","JetHT_Run2017E","JetHT_Run2017F"],
            "subsamples": ["JetHT_Run2017C"],
            "files_per_job": 2,
            "label": "_JetHTData",
            "njets": 1,
            "maxchunks": 10,
        },
    },
    "Validation": {
        # add private H4q sample ( need to get access to cmsconnect)
        # add VBF/H4q sample (resubmit crab miniaod)
        "QCDHerwig": {
            "subsamples": ["QCD_Pt_150to3000_herwig"],
            "files_per_job": 1,
            "label": "_QCD",
            "njets": 1,
            "maxchunks": 2,
        },
        "XYH": {
            "subsamples": [
                "NMSSM_XYH_WWbb_MX_1500_MY400",
                "NMSSM_XYH_WWbb_MX_1300_MY200",
                "NMSSM_XYH_WWbb_MX_2000_MY400",
                "NMSSM_XYH_WWbb_MX_3000_MY800",
            ],
            "files_per_job": 40,
            "label": "_H_VV",
            "njets": 2,
        },
        "HWWPrivate": {
            "subsamples": [
                "GluGluToBulkGravitonToHHTo4W_JHUGen_M-2500_narrow",
                "GluGluToHHTo4V_node_cHHH1",
                # "jhu_HHbbWW",
                # "pythia_HHbbWW",
                # "jhu_HHbbZZ",
                # "jhu_HHbbWW_Mar3"
            ],
            "files_per_job": 20,
            "label": "_H_VV",
            "njets": 2,
        },
        "HWW": {
            "subsamples": [
                "GluGluHToWWToLNuQQ",
                "GluGluHToWW_Pt-200ToInf_M-125",
                "GluGluToHToWWTo4q",
                "GluGluToHHTobbVV_node_cHHH1_pn4q",
                "GluGluToHHTobbVV_node_cHHH5_pn4q",
                "VBF_HHTobbVV_CV_1_C2V_2_C3_1_TuneCP5_13TeV-madgraph-pythia8",
                "HWplusJ_HToWW_M-125_TuneCP5_13TeV-powheg-jhugen727-pythia8",
                "HZJ_HToWW_M-125_TuneCP5_13TeV-powheg-jhugen727-pythia8",
                "ttHToNonbb_M125",
            ],
            "files_per_job": 20,
            "label": "_H_VV",
            "njets": 2,
        },
    },
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", default="2017", help="year", type=str)
    parser.add_argument("--tag", default="Test", help="process tag", type=str)
    parser.add_argument("--jet", default="AK8", help="jet", type=str)
    parser.add_argument(
        "--submit", dest="submit", action="store_true", help="submit jobs when created"
    )
    args = parser.parse_args()

    args.script = "run.py"
    args.processor = "input"
    args.outdir = "outfiles"
    args.test = False
    tag = args.tag
    for key, tdict in samples_to_submit.items():
        for sample, sdict in tdict.items():
            args.samples = [sample]
            args.subsamples = sdict["subsamples"]
            args.files_per_job = sdict["files_per_job"]
            args.njets = sdict["njets"]
            args.label = args.jet + sdict["label"]
            args.tag = tag
            if key == "Validation":
                args.tag = f"{args.tag}_Validation"
            if "maxchuncks" in sdict.keys():
                args.maxchunks = sdict["maxchunks"]
            else:
                args.maxchunks = 0
            print(args)
            submit.main(args)

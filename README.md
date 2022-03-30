# HHbbVV

[![Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<p align="left">
  <img width="300" src="https://raw.githubusercontent.com/rkansal47/HHbbVV/main/figure.png" />
</p>

Search for two boosted (high transverse momentum) Higgs bosons (H) decaying to two beauty quarks (b) and two vector bosons (V). The majority of the analysis uses a columnar framework to process input tree-based [NanoAOD](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD) files using the [coffea](https://coffeateam.github.io/coffea/) and [scikit-hep](https://scikit-hep.org) Python libraries.

## Instructions for running coffea processors

General note: Coffea-casa is faster and more convenient, however still somewhat experimental so for large of inputs and/or processors which may require heavier cpu/memory usage (e.g. bbVVSkimmer) condor is recommended.

### For [coffea-casa](https://coffea-casa.readthedocs.io/en/latest/cc_user.html):
1. after following instructions ^ set up an account, open the coffea-casa GUI (https://cmsaf-jh.unl.edu) and create an image
2. open `src/runCoffeaCasa.ipynb`
3. import your desired processor, specify it in the `run_uproot_job` function, and specify your filelist
4. run the first three cells


### To submit with normal condor:

```bash
git clone https://github.com/rkansal47/HHbbVV/
cd HHbbVV
TAG=Aug18_skimmer
python src/condor/submit.py --processor skimmer --tag $TAG --files-per-job 20  # will need python3 (recommended to set up via miniconda)
for i in condor/$TAG/*.jdl; do condor_submit $i; done
```

To test locally first (recommended), can do e.g.:

```bash
mkdir outfiles
python -W ignore src/run.py --starti 0 --endi 1 --year 2017 --processor skimmer --executor iterative --samples HWW --subsamples GluGluToHHTobbVV_node_cHHH1_pn4q
```

#### TODO: instructions for lpcjobqueue (currently quite buggy)

## Processors

### bbVVSkimmer

Applies pre-selection cuts, runs inference with our new HVV tagger, and saves unbinned branches as parquet files.

Parquet and pickle files will be saved in the eos directory of specified user at path `~/eos/bbVV/skimmer/<tag>/<sample_name>/<parquet or pickles>`. Pickles are in the format `{'nevents': int, 'cutflow': Dict[str, int]}`.

### TaggerInputSkimmer

Applies a loose pre-selection cut, saves ntuples with training inputs.

To test locally (in singularity):
```bash
python -W ignore src/run.py --year 2017 --starti 300 --endi 301 --samples HWWPrivate --subsamples jhu_HHbbWW --processor input --label AK15_H_VV
python -W ignore src/run.py --year 2017 --starti 300 --endi 301 --samples QCD --subsamples QCD_Pt_1000to1400 --processor input --label AK15_QCD --njets 1 --maxchunks 1
```

Jobs:
```bash
TAG=Mar29
JETS=AK15

# Training
python3 src/condor/submit.py --processor input --tag ${TAG}_${JETS} --files-per-job 1 --samples QCD --label ${JETS}_QCD --njets 1 --maxchunks 1 --subsamples QCD_Pt_300to470 QCD_Pt_470to600 QCD_Pt_600to800 QCD_Pt_800to1000 QCD_Pt_1000to1400
python3 src/condor/submit.py --processor input --tag ${TAG}_${JETS} --files-per-job 20 --samples HWWPrivate --subsamples BulkGravitonToHHTo4W_JHUGen_MX-600to6000_MH-15to250_v2_ext1 BulkGravitonToHHTo4W_JHUGen_MX-600to6000_MH-15to250_v2 --label ${JETS}_H_VV --njets 2

# Validation
python3 src/condor/submit.py --processor input --tag ${TAG}_${JETS} --files-per-job 20 --samples HWWPrivate --subsamples jhu_HHbbWW GluGluToBulkGravitonToHHTo4W_JHUGen_M-2500_narrow jhu_HHbbZZ pythia_HHbbWW --label ${JETS}_H_VV --njets 2
python3 src/condor/submit.py --processor input --tag ${TAG}_${JETS} --files-per-job 2 --samples HWW --subsamples GluGluToHHTobbVV_node_cHHH1_pn4q --label ${JETS}_H_VV --njets 2
python3 src/condor/submit.py --processor input --tag ${TAG}_${JETS} --files-per-job 1 --samples HWWPrivate --subsamples GluGluToHHTo4V_node_cHHH1 --label ${JETS}_H_VV --njets 2

# Submit
nohup bash -c 'for i in condor/'"${TAG}_${JETS}"'/*.jdl; do condor_submit $i; done' &> tmp/submitout.txt &
```

Or can add `--submit` flag to submit.

Command for copying directories to PRP in background 
```bash 
for i in *; do echo $i && sleep 5 && nohup sh -c "kubectl cp $i hwwtaggerdep-66468dbdd8-dwr4l:/hwwtaggervol/training/ak8_Mar29/ && echo $i" &> $i.txt & done```

# Scripts for downloading AFDB models and Uniprot domains

These are some basic scripts for retrieving data from the AFDB and Uniprot.

## Setup

A file `uniprot_ids.txt` file is expected to contain the Uniprot IDs to process, one on each line.

An example input `uniprot_ids.txt` is included in this repository.

## Download AFDB Structures

```shell
python3 download_models_from_afdb.py
```

This finds the AlphaFold DB URL for each ID in `uniprot_ids.txt` by a query of 3D Beacons. Then 
based on the location in AlphaFold DB, it downloads the following files into the folder `afdb` 
(created if it doesn't already exist):

* `<id>.cif` - the predicted 3D structure, with pLDDT confidence as the b-factor values
* `<id>_PAE.json` - the Predicted Aligned Error of each residue in the predicted structure
* `<id>_PAE.png` - an image of the PAE of the predicted structure
* `<id>_summary.json` - the 3D Beacons query response, containing the URL used for the AlphaFold DB 
                        downloads

Example output is in the folder `afdb`.

IDs for which all of these files already exist will be skipped.

Any IDs which were not found by 3D Beacons will be written to a new file, one ID per line, with the 
filename: `not_in_afdb-YYYY_MM-DD-HH_MM_SS_[A|P]M.txt`
* These may not exist in AFDB, and may need to be folded separately.

Any IDs which encountered an error while attempting to download from AFDB will be written to a new 
file, one ID per line, with the filename: `error_downloading_from_afdb-YYYY_MM-DD-HH_MM_SS_[A|P]M.txt`
* These may still exist in AFDB and just encountered a temporary error, such as a connection 
  interruption. They may be found if the script is run again.

**Optional Arguments:**
* `ids_filename` - use a different ID input file than `uniprot_ids.txt`
* `download_dir` - download to a different directory than `afdb`

## Download UniProt Features

```shell
python3 download_uniprot_features.py
```

This downloads features for each ID in `uniprot_ids.txt` from UniProt in the `.gff` 
format. It downlods the following files into the folder `features` (created if it doesn't already 
exist):

* `<id>.gff` - the UniProt features file

Example output is in the folder `features`.

IDs for which this file already exists will be skipped.

Any IDs which could not be downloaded, either due to the file not being available or connection 
issues, will be written to a new file, one ID per line, with the filename: 
`error_downloading_domains_from_uniprot-YYYY_MM-DD-HH_MM_SS_[A|P]M.txt`

**Optional Arguments:**
* `ids_filename` - use a different ID input file than `uniprot_ids.txt`
* `download_dir` - download to a different directory than `features`

## Get just Domains from UniProt Features

```shell
python3 get_domains_from_gff.py
```

This extracts just the domains out of the `<id>.gff` features in `features` for each ID in 
`uniprot_ids.txt`. It produces the following files into the folder `domains`:
* `<id>.gff` - the UniProt features file containing just domains

Example output is in the folder `domains`.

The `bcbio-gff` package is required:

```
pip install bcbio-gff
```

**Optional Arguments:**
* `ids_filename` - use a different ID input file than `uniprot_ids.txt`
* `features_dir` - use a different input features directory than `features`
* `domains_dir` - save domain feature files to a different directory than `domains`

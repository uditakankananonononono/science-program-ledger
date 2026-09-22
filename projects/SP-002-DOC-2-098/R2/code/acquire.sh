#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/raw
curl -L --fail --retry 3 -o data/raw/heart-disease.zip 'https://archive.ics.uci.edu/static/public/45/heart+disease.zip'
curl -L --fail --retry 3 -o data/raw/UCI_HAR_Dataset.zip 'https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip'
curl -L --fail --retry 3 -o data/raw/ogbg_molhiv.zip 'https://snap.stanford.edu/ogb/data/graphproppred/csv_mol_download/hiv.zip'
sha256sum data/raw/*.zip

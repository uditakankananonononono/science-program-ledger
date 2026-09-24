"""Download + parse Doench 2014 (V1) and Doench 2016 (V2) into tidy CSVs.
V1 context is 34 nt (NNNN[20]NGGNNNNNNN); V2 context is 30 nt (NNNN[20]NGGNNN)
and is right-padded with N to 34 so one feature builder serves both."""
import hashlib, io, urllib.request, warnings
import pandas as pd
warnings.filterwarnings('ignore')

BASE = 'https://raw.githubusercontent.com/MicrosoftResearch/Azimuth/master/azimuth/data/'

def fetch(name):
    with urllib.request.urlopen(BASE + name, timeout=120) as r:
        b = r.read()
    print(name, len(b), 'sha256', hashlib.sha256(b).hexdigest()[:16])
    return b

def pad34(s):
    s = str(s).upper()
    return s + 'N' * (34 - len(s)) if len(s) <= 34 else None

v1 = pd.read_csv(io.BytesIO(fetch('V1_suppl_data.txt')), sep='\t')
v1.columns = ['spacer20', 'ext34', 'strand', 'transcript', 'gene', 'cut_nt',
              'aa_pos', 'pct_peptide', 'annotation', 'activity', 'pct_rank']
v1 = v1[v1['ext34'].str.len() == 34].dropna(subset=['activity', 'pct_rank'])
v1.to_csv('data/v1.csv', index=False)
print('v1', v1.shape, 'genes', v1.gene.nunique())

v2 = pd.read_excel(io.BytesIO(fetch('V2_data.xlsx')), sheet_name='Results', header=7)
v2 = v2.rename(columns={'Extended Spacer(NNNN[20nt]NGGNNN)': 'ext30',
                        'Gene Symbol': 'gene', 'sgRNA Score': 'score',
                        'Low Flag': 'low_flag',
                        'Amino Acid Cut position': 'aa_pos',
                        'Percent Peptide': 'pct_peptide'})
v2 = v2[pd.to_numeric(v2['score'], errors='coerce').notna()].copy()
v2['score'] = v2['score'].astype(float)
v2['ext34'] = v2['ext30'].map(pad34)
v2 = v2.dropna(subset=['ext34'])
v2 = v2[v2['low_flag'].fillna('').astype(str) != 'flag']
v2[['ext34', 'gene', 'aa_pos', 'pct_peptide', 'score']].to_csv('data/v2.csv', index=False)
print('v2', v2.shape, 'genes', v2.gene.nunique())

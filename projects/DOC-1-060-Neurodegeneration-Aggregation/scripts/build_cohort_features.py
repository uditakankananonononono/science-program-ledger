import pandas as pd,numpy as np,pathlib,re,csv
B=pathlib.Path(__file__).resolve().parents[1]; raw=B/'data/raw';out=B/'data/processed';res=B/'results'
phr=['alzheimer','parkinson','huntington','amyotrophic lateral sclerosis','frontotemporal dementia','prion disease','spinocerebellar ataxia','neurodegeneration','neurodegenerative']
P=pd.read_csv(raw/'uniprot_positive_candidates.tsv',sep='\t');N=pd.read_csv(raw/'uniprot_negative_candidates.tsv',sep='\t')
log=[]
def gate(df,label):
 good=[];seen={}
 for _,r in df.sort_values('Entry').iterrows():
  seq=str(r.Sequence);reason=''
  if not 50<=len(seq)<=1200:reason='length'
  elif re.search('[^ACDEFGHIKLMNPQRSTVWY]',seq):reason='nonstandard_residue'
  elif seq in seen:reason='duplicate_sequence'
  elif label==1 and not any(p in str(r.get('Involvement in disease','')).lower() for p in phr):reason='phrase_absent'
  if reason:log.append({'accession':r.Entry,'class':label,'decision':'exclude','reason':reason})
  else:seen[seq]=r.Entry;good.append(r)
 return pd.DataFrame(good)
P=gate(P,1);N=gate(N,0)
used=set();pairs=[]
for _,p in P.sort_values('Entry').iterrows():
 cand=N[~N.Entry.isin(used)].copy();cand=cand[(cand.Length/p.Length>=.8)&(cand.Length/p.Length<=1.25)]
 if cand.empty:log.append({'accession':p.Entry,'class':1,'decision':'exclude','reason':'no_length_match'});continue
 cand['dist']=abs(np.log(cand.Length/p.Length));n=cand.sort_values(['dist','Entry']).iloc[0];used.add(n.Entry);pairs.append((p,n))
for k,(p,n) in enumerate(pairs,1):
 for y,r in [(1,p),(0,n)]:
  log.append({'accession':r.Entry,'class':y,'decision':'include','reason':'','pair_id':k})
rows=[]
hyd={'A':1.8,'R':-4.5,'N':-3.5,'D':-3.5,'C':2.5,'Q':-3.5,'E':-3.5,'G':-.4,'H':-3.2,'I':4.5,'L':3.8,'K':-3.9,'M':1.9,'F':2.8,'P':-1.6,'S':-.8,'T':-.7,'W':-.9,'Y':-1.3,'V':4.2}
for k,(p,n) in enumerate(pairs,1):
 for y,r in [(1,p),(0,n)]:
  s=r.Sequence;vals=np.array([hyd[x]+(.5 if x in 'VIFYW' else 0)-(1 if x in 'DEKR' else 0) for x in s]);win=np.convolve(vals,np.ones(7)/7,'valid');lc=np.mean([len(set(s[i:i+12]))<=6 for i in range(len(s)-11)]) if len(s)>=12 else 0
  rows.append({'accession':r.Entry,'entry_name':r['Entry Name'],'protein_name':r['Protein names'],'length':len(s),'sequence':s,'label':y,'pair_id':k,'agg_max':win.max(),'agg_fraction_ge2':np.mean(win>=2),'agg_top5_mean':np.mean(np.sort(win)[-max(1,int(np.ceil(.05*len(win)))):]),'hydrophobic_fraction':np.mean([x in 'AVILMFWYC' for x in s]),'charged_fraction':np.mean([x in 'DEKR' for x in s]),'aromatic_fraction':np.mean([x in 'FWY' for x in s]),'low_complexity_fraction':lc,'disease_comment':r.get('Involvement in disease','') if y else ''})
pd.DataFrame(rows).to_csv(out/'cohort_features.csv',index=False)
pd.DataFrame(log).to_csv(res/'screening_log.csv',index=False)
print('pairs',len(pairs),'positive gated',len(P),'negative gated',len(N))
if len(pairs)<40:raise SystemExit('LOCKED FEASIBILITY FAILURE')

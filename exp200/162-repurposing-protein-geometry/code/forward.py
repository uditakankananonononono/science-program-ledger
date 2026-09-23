import json, pandas as pd
exec(open('code/run.py').read().split("pos=set()")[0])
cut=json.load(open('results/primary.json'))['kmer_cut']
mo={m['id']:m['name'] for m in json.load(open('data/molecules.json'))}
J=lambda x,y: len(x&y)/len(x|y) if x|y else 0
rows=[]
for d,s in d2a.items():
    for c in km:
        if c in s: continue
        best=max(((J(ipr[a],ipr[c]),J(km[a],km[c]),a) for a in s),key=lambda x:x[0])
        if best[0]>=0.5 and best[1]<cut: rows.append((d,mo.get(d),'|'.join(sorted(gene.get(a) or a for a in s)),gene.get(c) or c,gene.get(best[2]),round(best[0],2),round(best[1],3)))
F=pd.DataFrame(rows,columns=['drug','drug_name','annotated_targets','candidate_target','via_target','interpro_jaccard','kmer_jaccard']).sort_values('interpro_jaccard',ascending=False)
F.to_csv('results/candidate_alternative_targets.csv',index=False); print(len(F),F.drug.nunique()); print(F.head(12).to_string())

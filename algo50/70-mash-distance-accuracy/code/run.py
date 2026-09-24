import numpy as np, json
rng=np.random.default_rng(43)
B='ACGT'
anc=''.join(rng.choice(list(B),50000))
def descendant(p):
    out=[]
    for c in anc:
        if rng.random()<p: out.append(rng.choice([x for x in B if x!=c]))
        else: out.append(c)
    return ''.join(out)
def kmers(s,k):
    return {hash(s[i:i+k]) for i in range(len(s)-k+1)}
res={}
for k in (11,15,21,31):
    for p in (0.01,0.05,0.10,0.15,0.20,0.30,0.40):
        ests=[]
        for _ in range(20):
            d=descendant(p)
            A=kmers(anc,k); D=kmers(d,k)
            J=len(A&D)/len(A|D)
            ests.append(-np.log(2*J/(1+J))/k)
        res[f'k{k}_p{p}']=dict(med=float(np.median(ests)),err=float(np.median(ests)-p))
    print(k,flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
G1=all(abs(res[f'k21_p{p}']['err'])<=0.01 for p in (0.01,0.05,0.10,0.15))
G2=all(all(res[f'k{k}_p{a}']['med']<res[f'k{k}_p{b}']['med'] for a,b in zip((0.01,0.05,0.10,0.15,0.20,0.30),(0.05,0.10,0.15,0.20,0.30,0.40))) for k in (11,15,21,31))
G3=res['k21_p0.4']['med']<0.40
G4=abs(res['k31_p0.3']['err'])>abs(res['k11_p0.3']['err'])
print('G1',G1,[round(res[f'k21_p{p}']['err'],4) for p in (0.01,0.05,0.10,0.15)])
print('G2',G2)
print('G3',G3,res['k21_p0.4']['med'])
print('G4',G4,res['k11_p0.3']['err'],res['k31_p0.3']['err'])

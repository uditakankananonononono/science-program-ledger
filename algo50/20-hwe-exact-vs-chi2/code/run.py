import numpy as np, json
from math import lgamma, exp, log
def exact_p(aa,ab,bb):
    # Wigginton 2005
    n=aa+ab+bb; na=2*aa+ab; nb=2*n-na
    if na==0 or nb==0: return 1.0
    probs=[]
    logp=lambda x: (lgamma(na+1)+lgamma(nb+1)+lgamma(n+1)+ (x*log(2)) - lgamma((na-x)//2+1)-lgamma(x+1)-lgamma((nb-x)//2+1)-lgamma(n+1)) if (na-x)%2==0 and (nb-x)%2==0 else None
    lo=max(0,na-n); hi=min(na,2*n)  # bounds on het count x: x ≡ na mod 2
    xs=[x for x in range(na%2, min(na,nb)+1, 2)]
    lp=np.array([logp(x) for x in xs])
    mx=lp.max(); p=np.exp(lp-mx); p/=p.sum()
    pobs=p[list(xs).index(ab)]
    return float(p[p<=pobs+1e-12].sum())
def chi2_p(aa,ab,bb):
    n=aa+ab+bb; p=(2*aa+ab)/(2*n); q=1-p
    e=np.array([p*p,2*p*q,q*q])*n
    o=np.array([aa,ab,bb])
    x2=((o-e)**2/np.maximum(e,1e-9)).sum()
    from scipy.stats import chi2 as c2
    return float(c2.sf(x2,1))
rng=np.random.default_rng(1)
def sim(n,probs,reps=2000):
    return rng.multinomial(n,probs,reps)
def run(n,p,F=0.0):
    q=1-p
    probs=[p*p+F*p*q,2*p*q*(1-F),q*q+F*p*q]
    draws=sim(n,probs)
    t1c=t1e=0
    for aa,ab,bb in draws:
        t1c+=chi2_p(aa,ab,bb)<0.01
        t1e+=exact_p(aa,ab,bb)<0.01
    return t1c/len(draws),t1e/len(draws)
out={}
out['A_null_maf05_n500']=run(500,0.05)
out['B_null_maf01_n200']=run(200,0.01)
out['C_inbreed_F01_maf02_n500']=run(500,0.2,0.1)
print(json.dumps(out,indent=1))
json.dump(out,open('results/results.json','w'),indent=1)
a,b,c=out['A_null_maf05_n500'],out['B_null_maf01_n200'],out['C_inbreed_F01_maf02_n500']
print('G1',a[0]>=2*a[1],a)
print('G2',0.003<=a[1]<=0.02)
print('G3',c[1]>=c[0]-0.05,c)
print('G4',b[1]<=0.05,b)

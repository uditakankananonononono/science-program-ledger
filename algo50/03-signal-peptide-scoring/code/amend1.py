import json,numpy as np,sys
sys.argv=['x']; exec(open('code/run.py').read().split("# B1 threshold on human")[0])
from sklearn.metrics import matthews_corrcoef
def shift(p,pi_new,pi_old=0.5):
    a=p*pi_new/pi_old; b=(1-p)*(1-pi_new)/(1-pi_old); return a/(a+b)
def em(p,pi_old=0.5):
    pi=0.5
    for _ in range(200):
        new=shift(p,pi,pi_old).mean()
        if abs(new-pi)<1e-6: break
        pi=new
    return pi
m=make_pipeline(StandardScaler(),LogisticRegression(C=0.01,max_iter=2000,class_weight='balanced'))
pcv=cross_val_predict(m,Xtr[2],y,cv=StratifiedKFold(5,shuffle=True,random_state=0),method='predict_proba')[:,1]
pih=y.mean(); ph=shift(pcv,pih); ths=np.quantile(ph,np.linspace(0.5,0.995,300)); mc=[matthews_corrcoef(y,ph>=t) for t in ths]; tau=ths[int(np.argmax(mc))]
m.fit(Xtr[2],y); out={'human_prev':float(pih),'tau_h':float(tau),'human_cv_mcc_at_tau':float(max(mc))}
allp=[];ally=[];allp0=[]
base=json.load(open('results/results.json'))
for o in ['yeast','ecoli']:
    d=te[o]; yy=np.array([x[2] for x in d]); p=m.predict_proba(feats(d)[2])[:,1]; pit=em(p); pr=shift(p,pit)>=tau
    out[o]={'true_prev':float(yy.mean()),'em_prev':float(pit),'mcc_corrected':float(matthews_corrcoef(yy,pr)),'mcc_uncorrected':base[o]['P']['mcc'],'recall':float(pr[yy==1].mean()),'FPR':float(pr[yy==0].mean())}
    allp.append(pr); ally.append(yy)
out['pooled_mcc_corrected']=float(matthews_corrcoef(np.concatenate(ally),np.concatenate(allp)))
json.dump(out,open('results/amend1.json','w'),indent=1); print(json.dumps(out,indent=1))

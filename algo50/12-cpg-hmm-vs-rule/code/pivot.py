import numpy as np, json
exec(open('code/run.py').read().split("# window eval")[0])
# post-process states
segs=[];i=0; n=len(states)
lab=states.copy()
# merge island(1) segments separated by <200bp
arr=states
# find runs
runs=[]; i=0
while i<n:
    j=i
    while j<n and arr[j]==arr[i]: j+=1
    runs.append([i,j,arr[i]]); i=j
merged=[]; k=0
pp=np.zeros(n,int)
i=0
cur=None
for r in runs:
    if r[2]==1:
        if cur is not None and r[0]-cur[1]<200:
            cur[1]=r[1]
        else:
            if cur: merged.append(cur)
            cur=[r[0],r[1]]
    if r[2]==0 and cur is None and not merged:
        continue
if cur: merged.append(cur)
merged=[m for m in merged if m[1]-m[0]>=200]
for a,b in merged: pp[a:b]=1
# window eval with pp
W=200; step=100
wins=[]
for s in range(0,len(tseq)-W+1,step):
    a=half+s; b=half+s+W
    lab=mask[a:b].mean()>=0.5
    vit=pp[max(0,s-1):max(0,s-1)+W-1].mean()>=0.5 if s>0 else False
    wins.append((lab,vit))
y=np.array([w[0] for w in wins]); pred=np.array([w[1] for w in wins])
tp=np.sum(pred&y); p=tp/max(1,pred.sum()); r=tp/max(1,y.sum()); f1=2*p*r/max(1e-9,p+r)
test_isl=[(max(s,half)-half,min(e,half+len(tseq))-half) for s,e in isl if e>half]
covered=sum(1 for s,e in test_isl if pp[s:e].mean()>=0.5)
out={'F1':f1,'precision':p,'recall':r,
     'seg_median':float(np.median([b-a for a,b in merged])),
     'annot_median':float(np.median([e-s for s,e in test_isl])),
     'island_recall':covered/max(1,len(test_isl))}
print(json.dumps(out,indent=1))
json.dump(out,open('results/pivot_metrics.json','w'),indent=1)
base=json.load(open('results/results.json'))
print('P1 F1>=RULE+0.10:',f1,base['RULE'][0])
print('P2 seg median in [0.5x,2x]:',out['seg_median'],out['annot_median'])
print('P3 recall>=0.70:',out['island_recall'])

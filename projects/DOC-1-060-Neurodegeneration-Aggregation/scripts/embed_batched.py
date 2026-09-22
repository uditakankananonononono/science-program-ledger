import pandas as pd,numpy as np,torch,pathlib,json,datetime,hashlib
from transformers import AutoTokenizer,AutoModel
B=pathlib.Path(__file__).resolve().parents[1];d=pd.read_csv(B/'data/processed/cohort_features.csv');name='facebook/esm2_t6_8M_UR50D';tok=AutoTokenizer.from_pretrained(name);mod=AutoModel.from_pretrained(name).eval()
chunks=[]
for pi,s in enumerate(d.sequence):
 for st in range(0,len(s),1000):chunks.append((pi,s[st:st+1000]))
sums=np.zeros((len(d),320),np.float64);maxs=np.full((len(d),320),-np.inf,np.float32);counts=np.zeros(len(d),int)
chunks.sort(key=lambda x:len(x[1]))
for st in range(0,len(chunks),16):
 z=chunks[st:st+16];ss=[x[1] for x in z];x=tok(ss,return_tensors='pt',padding=True)
 with torch.no_grad():e=mod(**x).last_hidden_state.numpy()
 for j,(pi,s) in enumerate(z):
  q=e[j,1:len(s)+1];sums[pi]+=q.sum(0);counts[pi]+=len(q);maxs[pi]=np.maximum(maxs[pi],q.max(0))
 if st%160==0:print(st,'/',len(chunks))
a=np.c_[sums/counts[:,None],maxs].astype('float32');np.save(B/'data/processed/esm2_mean_max.npy',a)
(B/'provenance/model_artifact.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model':name,'shape':list(a.shape),'pooling':'mean+max; nonoverlapping chunks <=1000 residues; batched padding masked from pooling','sha256':hashlib.sha256((B/'data/processed/esm2_mean_max.npy').read_bytes()).hexdigest()},indent=2)+'\n')

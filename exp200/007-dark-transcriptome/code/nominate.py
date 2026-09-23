import torch; torch.set_num_threads(1)
import sys,json,numpy as np,torch.nn as nn
sys.path.insert(0,'code')
from model import GPT,encode
net=GPT(); net.load_state_dict(torch.load('results/ckpt.pt',weights_only=True)['model']); net.eval()
lossf=nn.CrossEntropyLoss(reduction='none')
def ll(seqs):
    out=[]
    with torch.no_grad():
        for i in range(0,len(seqs),32):
            x=torch.tensor(np.stack([encode(s) for s in seqs[i:i+32]]))
            inp,tgt=x[:,:-1],x[:,1:]
            lg=net(inp); mask=tgt<4
            l=-lossf(lg.reshape(-1,4),tgt.clamp(max=3).reshape(-1)).reshape(inp.shape)
            out+=((l*mask).sum(1)/mask.sum(1)).tolist()
    return np.array(out)
rows=[json.loads(l) for l in open('/tmp/007_noncode.jsonl')]
rng=np.random.default_rng(1); idx=rng.permutation(len(rows))[:500]
real=[rows[i]['seq'] for i in idx]; shuf=[rows[i]['shuf'] for i in idx]
d=ll(real)-ll(shuf)
top=np.argsort(d)[::-1][:3]
out=[{'id':rows[idx[t]]['id'],'delta':float(d[t]),'len':len(real[t]),'head':real[t][:80]} for t in top]
json.dump(out,open('results/nominations.json','w'),indent=1)
print(json.dumps(out,indent=1))

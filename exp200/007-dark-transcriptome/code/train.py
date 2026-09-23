import torch; torch.set_num_threads(1)
import sys,json,time,numpy as np,torch.nn as nn
sys.path.insert(0,'code')
from model import GPT,encode
start=int(sys.argv[1]); steps=int(sys.argv[2])
net=GPT(); opt=torch.optim.Adam(net.parameters(),lr=3e-4)
if start>0:
    ck=torch.load('results/ckpt.pt',weights_only=True)
    net.load_state_dict(ck['model']); opt.load_state_dict(ck['opt'])
import os
if os.path.exists('/tmp/007_X.npy'):
    X=torch.from_numpy(np.load('/tmp/007_X.npy'))
else:
    rows=[];nt=0
    for line in open('/tmp/007_train.jsonl'):
        r=json.loads(line); rows.append(r['seq']); nt+=len(r['seq'])
        if nt>=30_000_000: break
    X=torch.tensor(np.stack([encode(s) for s in rows]))
    np.save('/tmp/007_X.npy',X.numpy())
print('corpus tensor',tuple(X.shape))
lossf=nn.CrossEntropyLoss()
n=len(X); bs=32; t0=time.time()
for st in range(start,min(start+steps,(n+bs-1)//bs)):
    x=X[st*bs:(st+1)*bs].long()
    inp,tgt=x[:,:-1],x[:,1:]
    logits=net(inp); mask=tgt<4
    loss=lossf(logits[mask],tgt[mask])
    opt.zero_grad(); loss.backward(); opt.step()
    if st%50==0: print('step',st,'loss',round(float(loss),4),'t',round(time.time()-t0,1))
torch.save({'model':net.state_dict(),'opt':opt.state_dict(),'step':start+steps},'results/ckpt.pt')
print('saved at step',start+steps,'of',(n+bs-1)//bs)

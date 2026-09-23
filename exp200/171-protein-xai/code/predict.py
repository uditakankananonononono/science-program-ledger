"""Usage: python3 predict.py SEQUENCE [topk]  -> ranked candidate catalytic residues (ESM-2 8M + trained head, exp200/171)."""
import sys,json,torch,torch.nn as nn,os
from transformers import AutoTokenizer,AutoModel
D=os.path.join(os.path.dirname(__file__),'..','results')
tok=AutoTokenizer.from_pretrained('facebook/esm2_t6_8M_UR50D');lm=AutoModel.from_pretrained('facebook/esm2_t6_8M_UR50D').eval()
net=nn.Sequential(nn.Linear(320,128),nn.ReLU(),nn.Dropout(.2),nn.Linear(128,1));net.load_state_dict(torch.load(os.path.join(D,'pivot1_head.pt')));net.eval()
def score(seq):
    seq=seq[:1000]
    with torch.no_grad(): h=lm(**tok(seq,return_tensors='pt')).last_hidden_state[0,1:-1];return torch.sigmoid(net(h).squeeze(-1)).tolist()
if __name__=='__main__':
    s=sys.argv[1];k=int(sys.argv[2]) if len(sys.argv)>2 else 10;p=score(s)
    for i in sorted(range(len(p)),key=lambda i:-p[i])[:k]: print(f'{s[i]}{i+1}\t{p[i]:.3f}')

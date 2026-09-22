import pandas as pd,numpy as np,torch,pathlib,json,hashlib,datetime
from transformers import AutoTokenizer,AutoModel
B=pathlib.Path(__file__).resolve().parents[1]; d=pd.read_csv(B/'data/processed/residue_labels.csv')
map3={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
name='facebook/esm2_t6_8M_UR50D'; tok=AutoTokenizer.from_pretrained(name); model=AutoModel.from_pretrained(name).eval()
outs=[]
for pid,g in d.groupby('pdb_id',sort=True):
 g=g.sort_values('seq_index'); seq=''.join(map3[x] for x in g.aa3)
 x=tok(seq,return_tensors='pt',add_special_tokens=True)
 with torch.no_grad(): z=model(**x).last_hidden_state[0,1:len(seq)+1].cpu().numpy().astype('float32')
 assert len(z)==len(g); outs.append(z); print(pid,len(seq),z.shape)
np.save(B/'data/processed/esm2_embeddings.npy',np.concatenate(outs))
meta={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model':name,'dimensions':320,'rows':sum(map(len,outs)),'file_sha256':hashlib.sha256((B/'data/processed/esm2_embeddings.npy').read_bytes()).hexdigest()}
(B/'provenance/model_artifact.json').write_text(json.dumps(meta,indent=2)+'\n')

# usage: sw.py worker nworkers ; resumable, writes results/sw_rows/<i>.npy (scores of i vs j>=i)
import json,sys,os,time,numpy as np
from Bio import Align
from Bio.Align import substitution_matrices
w,nw,budget=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3])
d=json.load(open('data/set.json')); S=[x['seq'] for x in d]; n=len(S)
al=Align.PairwiseAligner(mode='local',substitution_matrix=substitution_matrices.load('BLOSUM62'),open_gap_score=-11,extend_gap_score=-1)
os.makedirs('results/sw_rows',exist_ok=True); t0=time.time()
# balance: row i costs n-i; assign rows by interleaving
for i in range(w,n,nw):
    fn=f'results/sw_rows/{i}.npy'
    if os.path.exists(fn): continue
    if time.time()-t0>budget: break
    np.save(fn,np.array([al.score(S[i],S[j]) for j in range(i,n)],dtype=np.float32))

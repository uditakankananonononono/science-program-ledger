def ktsp_pairs(Xa,ya,top=200):
    v=np.argsort(-Xa.var(0))[:top];P1=Xa[ya==1][:,v];P0=Xa[ya==0][:,v]
    s=np.abs((P1[:,:,None]<P1[:,None,:]).mean(0)-(P0[:,:,None]<P0[:,None,:]).mean(0));np.fill_diagonal(s,0)
    iu=np.dstack(np.unravel_index(np.argsort(-s,axis=None),s.shape))[0];out=[];used=set()
    for i,j in iu:
        if i in used or j in used: continue
        out.append((v[i],v[j],1 if (P1[:,i]<P1[:,j]).mean()>(P0[:,i]<P0[:,j]).mean() else -1));used|={i,j}
        if len(out)>=9: break
    return out
def ktsp_score(Z,pairs,k): return np.sum([s*(Z[:,i]<Z[:,j]) for i,j,s in pairs[:k]],0)

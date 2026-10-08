"""Exact discrete-corridor primal and Farkas verification, no continuous claim."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent/'f3'))
from verify import Invalid,vector,keys,load_bytes,scalar_text

def data(m):
    keys(m,('x','target','dt','B','lower','upper','limit','slew','previous'))
    x=vector(m['x'],cap=4);d=len(x);target=vector(m['target'],d,4);dt=vector(m['dt']);cap=vector(m['limit'],cap=4);a=len(cap)
    rate=vector(m['slew'],a,4);prev=vector(m['previous'],a,4)
    if any(v<=0 for v in dt+cap) or any(v<0 for v in rate) or any(abs(v)>c for v,c in zip(prev,cap)):raise Invalid('model bounds')
    if type(m['B']) is not list or len(m['B'])!=d:raise Invalid('map dimension')
    B=[vector(row,a,4) for row in m['B']];Ls=[];Us=[]
    if type(m['lower']) is not list or type(m['upper']) is not list or len(m['lower'])!=len(dt)+1 or len(m['upper'])!=len(dt)+1:raise Invalid('node dimension')
    for l,u in zip(m['lower'],m['upper']):
        l=vector(l,d,4);u=vector(u,d,4)
        if any(v>w for v,w in zip(l,u)):raise Invalid('node interval')
        Ls.append(l);Us.append(u)
    return x,target,dt,B,Ls,Us,cap,rate,prev

def assemble(m):
    x,target,dt,B,Ls,Us,cap,rate,prev=data(m);a=len(cap);n=len(dt);size=a*n;A=[];b=[];labels=[]
    def add(row,rhs,label):A.append(row);b.append(rhs);labels.append(label)
    for k in range(n):
        for j in range(a):
            for sign,name in ((1,'upper'),(-1,'lower')):
                row=[0]*size;row[k*a+j]=sign;add(row,cap[j],f'actuator:{k}:{j}:{name}')
    for k in range(n):
        for j in range(a):
            for sign,name in ((1,'upper'),(-1,'lower')):
                row=[0]*size;row[k*a+j]=sign
                if k:row[(k-1)*a+j]=-sign
                add(row,rate[j]*dt[k]+sign*(prev[j] if k==0 else 0),f'slew:{k}:{j}:{name}')
    for node,(l,u) in enumerate(zip(Ls,Us)):
        for i in range(len(x)):
            for sign,name in ((1,'upper'),(-1,'lower')):
                row=[sign*t*v if k<node else 0 for k,t in enumerate(dt) for v in B[i]]
                add(row,u[i]-x[i] if sign==1 else x[i]-l[i],f'node:{node}:{i}:{name}')
    for i in range(len(x)):
        for sign,name in ((1,'upper'),(-1,'lower')):
            row=[sign*t*v for t in dt for v in B[i]];add(row,sign*(target[i]-x[i]),f'terminal:{i}:{name}')
    return A,b,labels

def text(v):
    if type(v) is list:return [text(a) for a in v]
    return scalar_text(v)

def check(m,w):
    try:
        A,b,labels=assemble(m)
        if w is None:return {'status':'UNAVAILABLE','reason':'missing witness'}
        if type(w) is not dict or w.get('kind') not in ('primal','farkas'):raise Invalid('witness kind')
        if w['kind']=='farkas':
            keys(w,('kind','multipliers'));lam=vector(w['multipliers'],len(A),400)
            if any(v<0 for v in lam):raise Invalid('negative multiplier')
            station=[sum(row[j]*v for row,v in zip(A,lam)) for j in range(len(A[0]))]
            if any(station):raise Invalid('nonstationary multipliers')
            rhs=sum(v*c for v,c in zip(lam,b))
            return {'status':'INFEASIBLE' if rhs<0 else 'UNAVAILABLE','reason':'strict Farkas contradiction' if rhs<0 else 'noncontradictory multipliers','combined_rhs':scalar_text(rhs),'stationarity':text(station)}
        keys(w,('kind','controls'));u=vector(w['controls'],len(A[0]),32)
        if any(sum(v*c for v,c in zip(row,u))>rhs for row,rhs in zip(A,b)):raise Invalid('primal inequality violation')
        x,target,dt,B,Ls,Us,cap,rate,prev=data(m);a=len(cap);controls=[u[k*a:(k+1)*a] for k in range(len(dt))];old=prev;path=[x[:]]
        for t,row in zip(dt,controls):
            if any(abs(v)>c or abs(v-p)>r*t for v,c,p,r in zip(row,cap,old,rate)):raise Invalid('independent control replay')
            old=row;path.append([v+t*sum(c*q for c,q in zip(br,row)) for v,br in zip(path[-1],B)])
        if any(v<l or v>h for row,lo,hi in zip(path,Ls,Us) for v,l,h in zip(row,lo,hi)):raise Invalid('independent node replay')
        if path[-1]!=target:raise Invalid('independent terminal replay')
        return {'status':'FEASIBLE','reason':'exact discrete corridor and independent replay','controls':text(controls),'path':text(path)}
    except Invalid as e:return {'status':'INVALID','reason':str(e)}

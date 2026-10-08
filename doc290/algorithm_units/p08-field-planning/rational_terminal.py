"""Exact square-invertible-map terminal solver; restricted established algebra."""
from fractions import Fraction as F
from rational_support import rational
from integral_lift import lift

def solve_terminal(initial,target,dt,B,limit,slew,previous):
    x=list(map(rational,initial));y=list(map(rational,target));matrix=[list(map(rational,row)) for row in B];n=len(x)
    if not n or len(y)!=n or len(matrix)!=n or any(len(row)!=n for row in matrix):raise ValueError('only square maps matching state dimension supported')
    # Validate time/bound contract independently of reachability verdict.
    cap=list(map(rational,limit));rate=list(map(rational,slew));prev=list(map(rational,previous));times=list(map(rational,dt))
    if any(len(v)!=n for v in (cap,rate,prev)):raise ValueError('actuator dimension')
    # Zero integral may be infeasible; obtain bounds from a feasible constant-previous schedule.
    anchor=[sum(times)*p for p in prev];interval=lift(times,cap,rate,prev,anchor)
    A=[row+[b-a] for row,a,b in zip(matrix,x,y)]
    for k in range(n):
        pivot=next((i for i in range(k,n) if A[i][k]),None)
        if pivot is None:raise ValueError('singular map unsupported; not an infeasibility verdict')
        A[k],A[pivot]=A[pivot],A[k];divisor=A[k][k];A[k]=[v/divisor for v in A[k]]
        for i in range(n):
            if i!=k:
                factor=A[i][k];A[i]=[a-factor*b for a,b in zip(A[i],A[k])]
    z=[row[-1] for row in A];lo=interval['lower_integrals'];hi=interval['upper_integrals']
    violations=[{'actuator':j,'required':a,'lower':l,'upper':h} for j,(a,l,h) in enumerate(zip(z,lo,hi)) if a<l or a>h]
    if violations:return {'status':'exact_model_unreachable','unique_integrals':z,'violations':violations}
    witness=lift(times,cap,rate,prev,z);terminal=[a+sum(b*c for b,c in zip(row,z)) for a,row in zip(x,matrix)]
    if terminal!=y:raise RuntimeError('exact terminal replay failed')
    return {'status':'exact_model_reachable','unique_integrals':z,'witness':witness,'terminal':terminal,
            'scope':'supplied rational square invertible constant-map model only; no physical precision or safety claim'}

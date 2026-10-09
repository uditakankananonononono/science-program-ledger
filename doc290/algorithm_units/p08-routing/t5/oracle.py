"""Independent original incoming-edge DFS, no checker topology consumption."""
def minimum(s):
    G=s['graph'];forbidden={(tuple(r[0]),tuple(r[1])) for r in s['forbidden']};best=[]
    def visit(vertex,incoming,seen,cost):
        if vertex==s['goal']:best.append(cost);return
        for i,e in enumerate(G[vertex]):
            outgoing=(vertex,i)
            if incoming is not None and (incoming,outgoing) in forbidden:continue
            state=(e['target'],outgoing)
            if state in seen:continue
            visit(e['target'],outgoing,seen|{state},cost+e['exposure'])
    visit(s['start'],None,{(s['start'],None)},0)
    return min(best) if best else None

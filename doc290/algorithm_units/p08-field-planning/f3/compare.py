"""Frozen symbolic-verdict comparison and separate descriptive floating baseline."""
import hashlib,json,os,sys
from pathlib import Path
from fractions import Fraction as F
from verify import load_bytes,verify,Invalid
ROOT=Path(__file__).resolve().parent

def agreed(expected,result):return expected==result['status']

def run(output):
    # Gate every source/fixture/environment identity before analysis/solver import.
    pins=json.loads((ROOT/'manifest.json').read_text())
    for name,digest in pins['files'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise Invalid('identity mismatch '+name)
    env=json.loads((ROOT/'environment.json').read_text())
    if sys.version!=env['python'] or any(os.environ.get(k)!='1' for k in env['thread_keys']):raise Invalid('environment mismatch')
    cases=load_bytes((ROOT/'cases.json').read_bytes())
    rows=[]
    for case in cases:
        result=verify(case['model'],case['witness'])
        rows.append({'name':case['name'],'expected':case['expected'],'result':result,'agreement':agreed(case['expected'],result),'input_sha256':hashlib.sha256(json.dumps(case,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
    # Floating baseline is never imported by the exact verifier or used for its verdict.
    sys.path.insert(0,str(ROOT.parent))
    import numpy,scipy
    if scipy.__version__!=env['scipy'] or numpy.__version__!=env['numpy']:raise Invalid('baseline version mismatch')
    from minimax import minimax_terminal
    baseline=[]
    for case in cases:
        if case['expected']!='VERIFIED':continue
        m=case['model']; name=case['name']
        def floats(v):return [floats(x) if type(x) is list else float(F(x)) for x in v]
        try:
            result=minimax_terminal(floats(m['x']),floats(m['dt']),floats(m['maps']),floats(m['limit']),floats(m['slew']),floats(m['previous']),floats(m['targets']))
            item={'name':name,'result':result}
            if result.get('status')=='primal_checked':
                diff=F(result['worst_terminal_coordinate_error'])-F(case['witness']['z'][-1]);item['binary_float_objective_minus_exact']=f'{diff.numerator}/{diff.denominator}'
        except Exception as e:item={'name':name,'exception_type':type(e).__name__,'exception':str(e)}
        baseline.append(item)
    report={'rows':rows,'agreement_count':sum(r['agreement'] for r in rows),'row_count':len(rows),'baseline':baseline,'scope':'supplied rational models only; disclosed development fixtures; no novelty/physiology/superiority'}
    Path(output).write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])

"""Numerical failure audit. Does not repair or tune pinned tracking implementation."""
import json,hashlib,sys,os,re,fractions,warnings,contextlib,_hashlib,_json,_sre
from pathlib import Path
from unittest.mock import patch
from fractions import Fraction as F
import numpy as np
import numpy.linalg._umath_linalg
sys.path.append(str(Path(__file__).resolve().parents[2]/'p08-field-planning'/'f3'))
from verify import load_bytes,Invalid
ROOT=Path(__file__).resolve().parent

def snapshot(array):
    a=np.asarray(array);owned=a.copy(order='C');raw=owned.tobytes(order='C')
    return {'dtype':a.dtype.str,'shape':list(a.shape),'strides':list(a.strides),'bytes_hex':raw.hex(),'sha256':hashlib.sha256(raw).hexdigest()}

def finite(value):
    if value is None:return True
    return bool(np.isfinite(np.asarray(value)).all())

def encode(v):
    if isinstance(v,np.ndarray):return encode(v.tolist())
    if isinstance(v,np.generic):return encode(v.item())
    if isinstance(v,float) and not np.isfinite(v):return {'nonfinite':'NaN' if np.isnan(v) else ('+Inf' if v>0 else '-Inf')}
    if type(v) is list:return [encode(a) for a in v]
    if type(v) is dict:return {k:encode(a) for k,a in v.items()}
    return v

def decode_numeric(v):
    if v is None:return None
    if type(v) is list:return [decode_numeric(a) for a in v]
    if type(v) is bool or type(v) not in (int,str):raise Invalid('input numeric grammar')
    if type(v) is str and (len(v)>80 or not re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?',v)):raise Invalid('input decimal grammar')
    f=float(v)
    if not np.isfinite(f):raise Invalid('input nonfinite')
    return f

def exc(e):return {'type':type(e).__name__,'message':str(e)}

def run_case(case,filter_class):
    # Fixtures are pinned before call; still reject fields/kinds outside prescribed grammar.
    required={'name','state','P','q','dt','measurement','R','inject','expected'}
    if type(case) is not dict or set(case) not in (required,required|{'oracle'}) or case['inject'] not in (None,'raise','nan','inf') or case['expected'] not in ('VALID','REFUSE'):raise Invalid('case schema')
    state=np.array(decode_numeric(case['state']),float);P=np.array(decode_numeric(case['P']),float)
    q=decode_numeric(case['q']);dt=decode_numeric(case['dt'])
    z=None if case['measurement'] is None else np.array(decode_numeric(case['measurement']),float)
    R=None if case['R'] is None else np.array(decode_numeric(case['R']),float)
    callers={'state':state,'P':P,'measurement':z,'R':R};caller_before={k:snapshot(v) for k,v in callers.items() if v is not None}
    row={'name':case['name'],'expected':case['expected'],'input_sha256':hashlib.sha256(json.dumps(case,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'caller_before':caller_before}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        try:f=filter_class(state,P,q)
        except Exception as e:
            row.update(stage='constructor',outcome='EXCEPTION',exception=exc(e),atomic_preserved=None,success=False)
        else:
            before={'state':snapshot(f.state),'P':snapshot(f.covariance)};row['owned_before']=before
            try:
                def injected(a,b):
                    if case['inject']=='raise':raise np.linalg.LinAlgError('K1 injected solve failure')
                    return np.full(np.asarray(b).shape,np.nan if case['inject']=='nan' else np.inf)
                context=patch('numpy.linalg.solve',side_effect=injected) if case['inject'] else contextlib.nullcontext()
                with context:result=f.step(dt,z,R)
            except Exception as e:
                row.update(stage='step',outcome='EXCEPTION',exception=exc(e))
            else:
                fields={k:finite(result.get(k)) for k in ('state','covariance','innovation','nis')}
                row.update(stage='step',outcome='RETURN',return_finite=fields,returned=encode(result))
                if case['expected']=='VALID':
                    oracle=case['oracle']
                    def values(v):return [values(a) if type(a) is list else float(F(a)) for a in v]
                    agreements={}
                    for source,key in (('state','state'),('P','covariance'),('innovation','innovation'),('nis','nis')):
                        target=oracle[source];actual=result[key]
                        if target is None:agreements[source]=actual is None
                        else:
                            target=values(target) if type(target) is list else float(F(target))
                            agreements[source]=bool(np.allclose(actual,target,rtol=0,atol=1e-12))
                    agreements['observed']=result['observed']==(z is not None);row['oracle_agreement']=agreements
            after={'state':snapshot(f.state),'P':snapshot(f.covariance)};row['owned_after']=after
            row['atomic_preserved']=before==after
            row['success']=(case['expected']=='REFUSE' and row['outcome']=='EXCEPTION' and row['atomic_preserved']) or (case['expected']=='VALID' and row['outcome']=='RETURN' and all(row['return_finite'].values()) and all(row['oracle_agreement'].values()))
        row['warnings']=[{'category':w.category.__name__,'message':str(w.message)} for w in caught]
    row['caller_after']={k:snapshot(v) for k,v in callers.items() if v is not None}
    row['caller_values_preserved']=row['caller_before']==row['caller_after']
    row['assessment']='PASS' if row['success'] else 'MISMATCH'
    return row

def gate():
    pins=json.loads((ROOT/'manifest.json').read_text())
    for name,digest in pins['files'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise Invalid('identity mismatch '+name)
    env=json.loads((ROOT/'environment.json').read_text())
    if sys.version!=env['python'] or np.__version__!=env['numpy'] or any(os.environ.get(k)!='1' for k in env['thread_keys']):raise Invalid('environment mismatch')
    for name,identity in env['runtime_sources'].items():
        path=Path(identity['path'])
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=identity['sha256']:raise Invalid('runtime source mismatch '+name)
    for name in env['module_names']:
        module=sys.modules.get(name)
        if module is None or (str(Path(module.__file__).resolve()) if getattr(module,'__file__',None) else str(Path(sys.executable).resolve()))!=env['runtime_sources'][name]['path']:raise Invalid('loaded module mismatch '+name)
    if str(Path(sys.executable).resolve())!=env['runtime_sources']['python_executable']['path']:raise Invalid('executable path mismatch')

def run(output):
    gate();cases=load_bytes((ROOT/'cases.json').read_bytes())
    sys.path.insert(0,str(ROOT.parent));from kalman import ConstantVelocity
    rows=[run_case(c,ConstantVelocity) for c in cases]
    report={'rows':rows,'row_count':len(rows),'pass_count':sum(r['success'] for r in rows),'mismatch_count':sum(not r['success'] for r in rows),'scope':'exposed numerical software controls, not calibration/invention','all_caller_values_preserved':all(r['caller_values_preserved'] for r in rows)}
    Path(output).write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n')
if __name__=='__main__':run(sys.argv[1])

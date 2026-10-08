"""Numerical failure audit. Does not repair or tune pinned tracking implementation."""
import json,hashlib,sys,os,re,fractions,warnings,contextlib,_hashlib,_json,_sre,math
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

def oracle_agreement(result,oracle):
    expected_keys={'total_records','scored_records','excluded_missing_truth','position_rmse','velocity_rmse','nees','mean_nees','scope'}
    if type(result) is not dict or set(result)!=expected_keys:return {'keys':False}
    agreed={'keys':True}
    for key,source in (('total_records','total'),('scored_records','scored'),('excluded_missing_truth','excluded')):
        agreed[key]=type(result[key]) is int and result[key]==oracle[source]
    for key,source in (('position_rmse','position_squared'),('velocity_rmse','velocity_squared'),('mean_nees','mean')):
        value=oracle[source];actual=result[key]
        if value is None:agreed[key]=actual is None
        else:
            want=math.sqrt(float(F(value))) if source.endswith('squared') else float(F(value))
            agreed[key]=type(actual) in (int,float) and abs(actual-want)<=1e-12
    agreed['nees']=type(result['nees']) is list and len(result['nees'])==len(oracle['nees']) and all(type(a) in (int,float) and abs(a-float(F(v)))<=1e-12 for a,v in zip(result['nees'],oracle['nees']))
    return agreed

def run_case(case,evaluate):
    required={'name','truth','estimated','covariances','available','inject','expected'}
    if type(case) is not dict or set(case) not in (required,required|{'oracle'}) or case['inject'] not in (None,'raise','nan') or case['expected'] not in ('VALID','REFUSE'):raise Invalid('case schema')
    def numeric(v):
        if type(v) is dict:
            if case['name'] not in ('V3','V4','R2','R3') or v!={'nonfinite':'NaN'}:raise Invalid('nonfinite fixture tag')
            return np.nan
        if type(v) is list:return [numeric(a) for a in v]
        return decode_numeric(v)
    if type(case['available']) is not list or any(type(v) not in (int,bool) for v in case['available']):raise Invalid('availability schema')
    inputs=[np.array(numeric(case[k]),float) for k in ('truth','estimated','covariances')]+[np.array(case['available'])]
    before=[snapshot(i) for i in inputs];row={'name':case['name'],'expected':case['expected'],'input_sha256':hashlib.sha256(json.dumps(case,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'input_before':before}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        try:
            def injected(a,b):
                if case['inject']=='raise':raise np.linalg.LinAlgError('K3 injected solve failure')
                return np.full(np.asarray(b).shape,np.nan)
            context=patch('numpy.linalg.solve',side_effect=injected) if case['inject'] else contextlib.nullcontext()
            with context:result=evaluate(*inputs)
        except Exception as e:row.update(outcome='EXCEPTION',exception=exc(e))
        else:
            fields={k:finite(result.get(k)) for k in ('total_records','scored_records','excluded_missing_truth','position_rmse','velocity_rmse','nees','mean_nees')}
            row.update(outcome='RETURN',return_finite=fields,returned=encode(result))
            if case['expected']=='VALID':row['oracle_agreement']=oracle_agreement(result,case['oracle'])
        row['warnings']=[{'category':w.category.__name__,'message':str(w.message)} for w in caught]
    row['input_after']=[snapshot(i) for i in inputs];row['inputs_preserved']=before==row['input_after']
    row['success']=(case['expected']=='REFUSE' and row['outcome']=='EXCEPTION' and row['inputs_preserved']) or (case['expected']=='VALID' and row['outcome']=='RETURN' and row['inputs_preserved'] and all(row['return_finite'].values()) and all(row['oracle_agreement'].values()))
    row['assessment']='PASS' if row['success'] else 'MISMATCH';return row

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
    sys.path.insert(0,str(ROOT.parent));from metrics import evaluate
    rows=[run_case(c,evaluate) for c in cases]
    report={'rows':rows,'row_count':len(rows),'pass_count':sum(r['success'] for r in rows),'mismatch_count':sum(not r['success'] for r in rows),'scope':'exposed numerical software controls, not calibration/invention','all_inputs_preserved':all(r['inputs_preserved'] for r in rows)}
    Path(output).write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n')
if __name__=='__main__':run(sys.argv[1])

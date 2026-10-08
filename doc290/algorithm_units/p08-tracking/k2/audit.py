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

def isolation(outputs,inputs):
    aliases={'output_input':[[bool(np.shares_memory(o,i)) for i in inputs] for o in outputs],'output_output':bool(np.shares_memory(outputs[0],outputs[1]))}
    base=[snapshot(i) for i in inputs];checks=[]
    for index in range(2):
        own=outputs[index];other=outputs[1-index];before=snapshot(own);other_before=snapshot(other)
        old=own.flat[0].copy();new=0.0 if old!=0 else 1.0
        try:
            own.flat[0]=new
            changed=snapshot(own)!=before
            checks.append({'actually_changed':changed,'inputs_unchanged':base==[snapshot(i) for i in inputs],'other_output_unchanged':other_before==snapshot(other)})
        finally:own.flat[0]=old
        checks[-1]['restored']=snapshot(own)==before
    return aliases,checks

def run_case(case,smooth_function):
    keys=('means','covs','predictions','pcs','Fs');required={'name',*keys,'inject','expected'}
    if type(case) is not dict or set(case) not in (required,required|{'oracle_means','oracle_covs'}) or case['inject'] not in (None,'raise','nan','inf') or case['expected'] not in ('VALID','REFUSE'):raise Invalid('case schema')
    def numeric(v):
        if type(v) is dict:
            if case['name']!='R2' or v!={'nonfinite':'NaN'}:raise Invalid('nonfinite fixture tag')
            return np.nan
        if type(v) is list:return [numeric(a) for a in v]
        return decode_numeric(v)
    inputs=[np.array(numeric(case[k]),float) for k in keys]
    n=len(inputs[0])
    if n==1:
        inputs[2]=inputs[2].reshape((0,4));inputs[3]=inputs[3].reshape((0,4,4));inputs[4]=inputs[4].reshape((0,4,4))
    before=[snapshot(i) for i in inputs];row={'name':case['name'],'expected':case['expected'],'input_sha256':hashlib.sha256(json.dumps(case,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'input_before':before}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        try:
            def injected(a,b):
                if case['inject']=='raise':raise np.linalg.LinAlgError('K2 injected solve failure')
                return np.full(np.asarray(b).shape,np.nan if case['inject']=='nan' else np.inf)
            context=patch('numpy.linalg.solve',side_effect=injected) if case['inject'] else contextlib.nullcontext()
            with context:means,covs=smooth_function(*inputs)
        except Exception as e:row.update(outcome='EXCEPTION',exception=exc(e))
        else:
            outputs=[means,covs];finite_flags=[finite(o) for o in outputs];shape_ok=means.shape==(n,4) and covs.shape==(n,4,4)
            row.update(outcome='RETURN',output_finite=finite_flags,output_shape_ok=shape_ok,returned=encode({'means':means,'covs':covs}),output_before_probe=[snapshot(o) for o in outputs])
            if case['expected']=='VALID':
                def values(v):return [values(a) if type(a) is list else float(F(a)) for a in v]
                row['oracle_agreement']=[shape_ok and bool(np.allclose(o,values(case[k]),rtol=0,atol=1e-12)) for o,k in zip(outputs,('oracle_means','oracle_covs'))]
            try:row['alias_flags'],row['isolation_probes']=isolation(outputs,inputs)
            except Exception as e:row['probe_exception']=exc(e)
            row['output_after_probe']=[snapshot(o) for o in outputs]
        row['warnings']=[{'category':w.category.__name__,'message':str(w.message)} for w in caught]
    row['input_after']=[snapshot(i) for i in inputs];row['inputs_preserved']=before==row['input_after']
    if case['expected']=='REFUSE':row['success']=row['outcome']=='EXCEPTION' and row['inputs_preserved']
    else:
        row['success']=row['outcome']=='RETURN' and row['inputs_preserved'] and row['output_shape_ok'] and all(row['output_finite']) and all(row['oracle_agreement']) and 'probe_exception' not in row and not any(any(a) for a in row['alias_flags']['output_input']) and not row['alias_flags']['output_output'] and all(all(probe.values()) for probe in row['isolation_probes'])
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
    sys.path.insert(0,str(ROOT.parent));from smoother import smooth
    rows=[run_case(c,smooth) for c in cases]
    report={'rows':rows,'row_count':len(rows),'pass_count':sum(r['success'] for r in rows),'mismatch_count':sum(not r['success'] for r in rows),'scope':'exposed numerical software controls, not calibration/invention','all_inputs_preserved':all(r['inputs_preserved'] for r in rows)}
    Path(output).write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n')
if __name__=='__main__':run(sys.argv[1])

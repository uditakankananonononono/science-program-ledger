#!/usr/bin/env python3
"""Deterministic review-support dossier validator. Does not score safety."""
import json,sys,hashlib
REQ={'schema_version','protocol_sha256','domain','config_id','dimensions','provenance'}
DIMS={'dependence','feature_shift','missingness','prevalence','calibration','instability'}
def validate(x):
 if not isinstance(x,dict): raise ValueError('root must be object')
 miss=REQ-set(x)
 if miss: raise ValueError('missing fields: '+','.join(sorted(miss)))
 if x['schema_version']!='1.0': raise ValueError('unsupported schema_version')
 if x['protocol_sha256']!='1e4fd59df50e558be7ed7dbae866a2313cd083aa60d932a370adf5b3ad11185f': raise ValueError('protocol hash mismatch')
 d=x['dimensions']
 if not isinstance(d,dict): raise ValueError('dimensions must be object')
 missd=DIMS-set(d)
 if missd: raise ValueError('missing dimensions: '+','.join(sorted(missd)))
 for k in DIMS:
  if not isinstance(d[k],(int,float)) or isinstance(d[k],bool) or not 0<=d[k]<=1: raise ValueError(f'invalid dimension {k}')
 p=x['provenance']
 if not isinstance(p,list) or not p or any(not isinstance(i,str) or not i.strip() for i in p): raise ValueError('provenance must be nonempty string array')
 return {'valid':True,'boundary':'review support only; not clinical-safety, regulatory, diagnostic, treatment, or deployment certification','record_sha256':hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
def main():
 try: print(json.dumps(validate(json.load(open(sys.argv[1]))),sort_keys=True))
 except Exception as e: print(json.dumps({'valid':False,'error':str(e)},sort_keys=True));sys.exit(2)
if __name__=='__main__': main()

"""Checkpointed per-mask development QC; no failure suppression."""
import argparse,json,time,zipfile,hashlib,math
from pathlib import Path
from hrf_extract import extract_member


def file_hash(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def pipeline_hash():
    import numpy, scipy, skimage, PIL
    root=Path(__file__).parent
    text='|'.join(file_hash(root/name) for name in ('hrf_extract.py','mask_graph.py','routing.py'))
    text+='|'+'|'.join(m.__version__ for m in (numpy,scipy,skimage,PIL))
    return hashlib.sha256(text.encode()).hexdigest()


def run_batch(sources,output,seconds=75):
    if isinstance(seconds,bool) or not isinstance(seconds,(int,float)) or not math.isfinite(seconds) or seconds<0:
        raise ValueError('seconds must be finite and nonnegative')
    if len({dataset for dataset,_ in sources})!=len(sources):
        raise ValueError('duplicate dataset identifier')
    hashes={dataset:file_hash(archive) for dataset,archive in sources}
    pipeline=pipeline_hash()
    output=Path(output)
    rows=[]
    if output.exists():rows=[json.loads(s) for s in output.read_text().splitlines() if s]
    expected=[]
    for dataset,archive in sources:
        with zipfile.ZipFile(archive) as z:
            members=sorted(n for n in z.namelist() if not n.endswith('/') and n.lower().endswith(('.png','.tif','.tiff')))
        expected.extend((dataset,archive,n) for n in members)
    expected_keys={(dataset,member) for dataset,_,member in expected}
    done=set()
    for row in rows:
        key=(row.get('dataset'),row.get('member'))
        if key not in expected_keys or key in done or row.get('status') not in ('passed','failed'):
            raise ValueError('checkpoint has duplicate, unknown or malformed record')
        if row.get('archive_sha256')!=hashes[key[0]] or row.get('pipeline_sha256')!=pipeline:
            raise ValueError('checkpoint provenance mismatch; use a new output for changed inputs/pipeline')
        done.add(key)
    start=time.monotonic()
    with output.open('a') as f:
        for dataset,archive,member in expected:
            if (dataset,member) in done:continue
            if time.monotonic()-start>=seconds:break
            before=time.monotonic()
            try:
                row,_=extract_member(archive,member)
                row.update(status='passed')
            except Exception as e:
                row={'member':member,'status':'failed','error_type':type(e).__name__,'error':str(e)}
            row.update(dataset=dataset,elapsed_seconds=time.monotonic()-before,archive_sha256=hashes[dataset],pipeline_sha256=pipeline)
            f.write(json.dumps(row)+'\n');f.flush()
            rows.append(row);done.add((dataset,member))
    counts={}
    for dataset,_ in sources:
        group=[r for r in rows if r['dataset']==dataset]
        counts[dataset]={'expected':sum(d==dataset for d,_,_ in expected),'processed':len(group),
                         'passed':sum(r['status']=='passed' for r in group),'failed':sum(r['status']=='failed' for r in group)}
    return {'counts':counts,'complete':all(v['processed']==v['expected'] for v in counts.values()),
            'scope':'full-mask extraction/component-count QC only, not anatomy/flow/independent validation'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('sources');p.add_argument('output');p.add_argument('--seconds',type=float,default=75)
    a=p.parse_args();sources=json.loads(Path(a.sources).read_text())
    print(json.dumps(run_batch(sources,a.output,a.seconds),indent=2))

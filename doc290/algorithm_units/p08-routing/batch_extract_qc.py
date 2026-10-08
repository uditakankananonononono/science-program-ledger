"""Checkpointed per-mask development QC; no failure suppression."""
import argparse,json,time,zipfile
from pathlib import Path
from hrf_extract import extract_member


def run_batch(sources,output,seconds=75):
    output=Path(output)
    rows=[]
    if output.exists():rows=[json.loads(s) for s in output.read_text().splitlines() if s]
    done={(r['dataset'],r['member']) for r in rows}
    expected=[]
    for dataset,archive in sources:
        with zipfile.ZipFile(archive) as z:
            members=sorted(n for n in z.namelist() if not n.endswith('/') and n.lower().endswith(('.png','.tif','.tiff')))
        expected.extend((dataset,archive,n) for n in members)
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
            row.update(dataset=dataset,elapsed_seconds=time.monotonic()-before)
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

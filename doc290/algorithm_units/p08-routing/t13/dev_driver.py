"""Real subprocess synthetic operational controls, never corpus methods."""
import sys,os,time,json
from pathlib import Path
from durable import transact,finalize,atomic
RUN=Path(sys.argv[1]);point=sys.argv[2];limit=int(sys.argv[3]) if len(sys.argv)>3 else 40
plan=[{'number':k,'method':'synthetic','order':['synthetic','synthetic'],'input':'outside-corpus'} for k in range(4)]
def validate(e,r):
    if r!={'status':'PASS','number':e['number'],'value':e['number']**2}:raise ValueError('synthetic schema/result')
def hook(p):
    if p==point:
        # outside run directory so it is not accepted as a production run file
        mark=RUN.with_name(RUN.name+'-ready');mark.write_text(p);time.sleep(30)
# launch evidence lives outside the run state
log=RUN.with_name(RUN.name+'-launches.txt')
def execute(e):
    with open(log,'a') as f:f.write(str(e['number'])+'\n');f.flush();os.fsync(f.fileno())
    return {'status':'PASS','number':e['number'],'value':e['number']**2}
if point in ('finalize','finalreport'):
    def finish(path,rs):
        atomic(path/'report.json',{'slots':[r['slot'] for r in rs]},True)
        if point=='finalreport':hook('finalreport')
    r=finalize(RUN,plan,{'dev':'fixed'},validate,finish)
else:r=transact(RUN,plan,{'dev':'fixed'},validate,execute,limit=limit,ceiling=.05 if point=='guard' else 60,headroom=7,hook=hook)
print(json.dumps(r))

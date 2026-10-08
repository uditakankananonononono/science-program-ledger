"""R2 static XLS cached cell inventory; no endpoint admission or execution."""
import hashlib,json,sys,time,urllib.request,xlrd
from pathlib import Path
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def download(url, limit, budget, opener=None):
    opener = opener or urllib.request.build_opener(NoRedirect())
    req = urllib.request.Request(url, headers={'Accept-Encoding': 'identity', 'User-Agent': 'source-admission/2'})
    data = bytearray(); start = time.monotonic()
    with opener.open(req, timeout=20) as r:
        if r.status != 200 or r.geturl() != url:
            raise ValueError('status or redirected URL')
        if r.headers.get('Content-Encoding', 'identity').lower() != 'identity':
            raise ValueError('nonidentity transport')
        length = r.headers.get('Content-Length'); declared = None
        if length is not None:
            if not length.isdigit(): raise ValueError('invalid content length')
            declared = int(length)
            if declared > min(limit, budget[0]): raise ValueError('declared byte cap')
        while True:
            if time.monotonic() - start > 40: raise ValueError('transport deadline')
            remaining = min(limit-len(data), budget[0])
            if remaining <= 0:
                if declared == len(data): break
                raise ValueError('cap boundary without EOF proof')
            chunk = r.read(min(65536, remaining))
            if not chunk: break
            budget[0] -= len(chunk)
            if len(chunk) > remaining: raise ValueError('stream byte cap')
            data.extend(chunk)
        if declared is not None and len(data) != declared: raise ValueError('truncated content length')
    return bytes(data)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def verify(raw,s):
    if len(raw)!=s['metadata_size'] or hashlib.md5(raw).hexdigest()!=s['metadata_md5']:raise ValueError('pinned identity')
def inventory(book,caps):
    # All dimensional caps checked before any cell inventory is exposed.
    if book.nsheets>caps['sheets']:raise ValueError('sheet cap')
    sheets=book.sheets();count=0
    for s in sheets:
        if s.nrows>caps['rows_per_sheet'] or s.ncols>caps['columns_per_sheet']:raise ValueError('dimension cap')
        count+=s.nrows*s.ncols
    if count>caps['cells_total']:raise ValueError('cell cap')
    result=[]
    for i,s in enumerate(sheets,1):
        cells=[]
        for r in range(s.nrows):
            for c in range(s.ncols):
                cell=s.cell(r,c)
                cells.append({'row_1based':r+1,'column_1based':c+1,'ctype':cell.ctype,'value':cell.value,
                 'value_status':'static cached value; formula origin/recalculation unresolved'})
        result.append({'sheet_ordinal':i,'name':s.name,'rows':s.nrows,'columns':s.ncols,'visibility':s.visibility,
         'merged_ranges_0based_halfopen':[list(m) for m in s.merged_cells],'cells':cells})
    return {'sheets':result,'cell_count':count,'ctype_names':{str(getattr(xlrd,k)):k for k in dir(xlrd) if k.startswith('XL_CELL_')},
      'claims':'syntax/cached cell inventory only; formula absence/fresh recalculation NOT established',
      'visual_binding':'NOT performed by parser; mandatory separate native pixel inspection'}
def parse(raw,caps):
    book=xlrd.open_workbook(file_contents=raw,formatting_info=True,on_demand=False)
    try:return inventory(book,caps)
    finally:book.release_resources()
def run(folder,retained=None):
    root=Path(__file__).parent
    for line in (root/'freeze-hashes.sha256').read_text().splitlines():
        h,n=line.split('  ',1)
        if sha((root/n).read_bytes())!=h:raise ValueError('freeze hash '+n)
    e=json.loads((root/'environment.json').read_text())
    if e['python']!=sys.version or e['xlrd_version']!=xlrd.__version__:raise ValueError('environment pin')
    modules=Path(xlrd.__file__).parent
    for n,h in e['xlrd_modules'].items():
        if sha((modules/n).read_bytes())!=h:raise ValueError('parser module pin '+n)
    sel=json.loads((root/'selection.json').read_text());s=sel['files'][0]
    if sel['article_id']!=5174419 or len(sel['files'])!=1 or sha((root/'record-metadata.json').read_bytes())!=sel['metadata_sha256']:raise ValueError('selection pin')
    out=Path(folder);out.mkdir(exist_ok=False);(out/'sources').mkdir();rec={**s,'status':'unavailable'}
    try:
        if retained is None:raw=download(s['url'],sel['max_file_bytes'],[sel['max_total_source_bytes']])
        else:
            with (Path(retained)/s['path']).open('rb') as f:raw=f.read(sel['max_file_bytes']+1)
            if len(raw)>sel['max_file_bytes']:raise ValueError('retained cap')
        (out/'sources'/s['path']).write_bytes(raw);rec.update(bytes=len(raw),sha256=sha(raw),received_md5=hashlib.md5(raw).hexdigest())
        verify(raw,s);rec['status']='verified'
    except Exception as ex:rec['error']=type(ex).__name__+': '+str(ex)
    dump(out/'inputs.json',[rec])
    if rec['status']!='verified':inv={'outcome':'scoped unavailable: original identity not verified','analysis_performed':False,'visual_performed':False}
    else:
        try:inv={'outcome':'mandatory native pixel inspection and manual endpoint/trial ledger required','inventory':parse(raw,e['caps'])}
        except Exception as ex:inv={'outcome':'unresolved XLS parser/cap','error':type(ex).__name__+': '+str(ex),'partial_inventory_exposed':False,'visual_performed':False}
    dump(out/'inventory.json',inv)
    dump(out/'manifest.json',{'code_sha256':sha((root/'admit.py').read_bytes()),'environment':e,'outputs':{p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}})
if __name__=='__main__':run(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)

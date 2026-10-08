"""A3 selected README raw text only. Never load CSV or execute source."""
import hashlib,json,os,re,sys,zipfile
from pathlib import Path
import scanner as a
def dump(p,x):a.dump(p,x)
def identity(f,sel):
 h=a.hashfile(f)
 if h!={'bytes':sel['archive_bytes'],'md5':sel['archive_md5'],'sha256':sel['archive_sha256']}:raise ValueError('full original identity')
 return h
def lines(raw,sel):
 text=raw.decode('utf-8',errors='strict');records=[];offset=0
 for m in re.finditer(r'\r\n|\r|\n',text):
  body=text[offset:m.start()];term=m.group();records.append({'line_ordinal_1based':len(records)+1,'text':body,'terminator':{'\r\n':'CRLF','\r':'CR','\n':'LF'}[term]});offset=m.end()
 if offset<len(text):records.append({'line_ordinal_1based':len(records)+1,'text':text[offset:],'terminator':'NONE'})
 if len(records)>sel['max_text_lines'] or any(len(r['text'])>sel['max_line_characters'] for r in records):raise ValueError('text caps')
 return {'status':'literal_UTF8_CR_LF_line_inventory','lines':records,'empty_original':not raw,'final_terminator':records[-1]['terminator'] if records else 'EMPTY','raw_sha256_discovered':a.sha(raw),'raw_bytes':len(raw),'grammar':'Only CRLF/CR/LF delimit lines; VT/FF/NEL/U+2028/U+2029 remain literal. No fictitious empty line after final delimiter; blank delimited lines preserved.'}
def read_selected(f,sel,caps):
 h=identity(f,sel);state=os.fstat(f.fileno());inv=a.directory(f,caps)
 selected=sel['files'][0]
 matches=[e for e in inv['entries'] if e['filename']==selected['filename']]
 if matches!=[selected]:raise ValueError('full selected central/ordinal agreement')
 with zipfile.ZipFile(f,'r') as z:
  infos=z.infolist();info=infos[selected['ordinal_1based']-1]
  if info.filename!=selected['filename']:raise ValueError('selected ordinal')
  raw=bytearray()
  with z.open(info,'r') as member:
   while True:
    chunk=member.read(min(65536,sel['max_decompressed_bytes']-len(raw)+1))
    if not chunk:break
    raw.extend(chunk)
    if len(raw)>sel['max_decompressed_bytes']:raise ValueError('decompressed cap')
  if len(raw)!=selected['uncompressed_size']:raise ValueError('exact original README byte size')
 if identity(f,sel)!=h or os.fstat(f.fileno())!=state:raise ValueError('original mutation')
 return bytes(raw)
def pins():return {**a.pins(),'scanner_sha256':a.sha(Path(a.__file__).read_bytes())}
def run(folder,archive):
 here=Path(__file__).parent
 for l in (here/'freeze-hashes.sha256').read_text().splitlines():
  h,n=l.split('  ',1)
  if a.sha((here/n).read_bytes())!=h:raise ValueError('freeze '+n)
 if pins()!=json.loads((here/'environment.json').read_text()):raise ValueError('environment')
 sel=json.loads((here/'selection.json').read_text());caps=json.loads((here/'directory-caps.json').read_text());out=Path(folder);out.mkdir(exist_ok=False)
 r={'status':'unavailable','partial_text_inventory_exposed':False}
 try:
  with Path(archive).open('rb') as f:raw=read_selected(f,sel,caps)
  r=lines(raw,sel);(out/'README.raw').write_bytes(raw)
 except Exception as ex:r.update(error=type(ex).__name__+': '+str(ex))
 dump(out/'inventory.json',r);dump(out/'manifest.json',{'environment':pins(),'outputs':{p.name:a.sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}})
if __name__=='__main__':run(sys.argv[1],sys.argv[2])

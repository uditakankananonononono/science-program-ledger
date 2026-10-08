import json,os,urllib.request,struct,time,zlib,zipfile,hashlib
root='/tmp/unit165/';assert json.load(open(root+'raw-stream-verification.json'))['match'];d=json.load(open(root+'live-api.json'));f=next(f for f in d['files'] if f['key']=='sEMG_data.zip');inv=json.load(open(root+'raw-inventory.json'));os.makedirs(root+'dev_raw',exist_ok=True)
def get(s,e):
 with urllib.request.urlopen(urllib.request.Request(f['links']['self'],headers={'Range':f'bytes={s}-{e}'}),timeout=15) as r:
  assert r.status==206 and r.headers.get('Content-Range')==f"bytes {s}-{e}/{f['size']}";b=r.read();assert len(b)==e-s+1;return b
start=time.time()
for sid in [1,3,5,7,9,11,13]:
 out=root+f'dev_raw/subject_{sid}.zip';comp=out+'.compressed';progress=out+'.progress.json'
 if os.path.exists(out+'.verified.json'):continue
 m=next(x for x in inv if x['name']==f'sEMG_data/subject_{sid}.zip')
 if os.path.exists(progress):state=json.load(open(progress));dataoff=state['data_offset']
 else:
  h=get(m['offset'],m['offset']+29);assert h[:4]==b'PK\x03\x04';n,x=struct.unpack_from('<HH',h,26);dataoff=m['offset']+30+n+x;json.dump({'data_offset':dataoff},open(progress,'w'));time.sleep(2)
 offset=os.path.getsize(comp) if os.path.exists(comp) else 0
 while offset<m['compressed_size']:
  count=min(32*1024*1024,m['compressed_size']-offset);b=get(dataoff+offset,dataoff+offset+count-1)
  with open(comp,'ab') as w:w.write(b)
  offset+=count;print('DEV',sid,offset,'/',m['compressed_size'],flush=True);time.sleep(2)
  if time.time()-start>35:return_flag=True;break
 if offset==m['compressed_size']:
  de=zlib.decompressobj(-15);crc=0;sha=hashlib.sha256();size=0
  with open(comp,'rb') as r,open(out,'wb') as w:
   while True:
    b=r.read(1024*1024)
    if not b:break
    u=de.decompress(b);w.write(u);crc=zlib.crc32(u,crc);sha.update(u);size+=len(u)
   u=de.flush();w.write(u);crc=zlib.crc32(u,crc);sha.update(u);size+=len(u)
  assert size==m['size'] and crc==m['crc'] and de.eof
  z=zipfile.ZipFile(out);assert z.testzip() is None
  meta={'subject':sid,'bytes':size,'crc32':crc,'sha256':sha.hexdigest(),'publisher_archive_md5_verified':True,'members':z.namelist()}
  json.dump(meta,open(out+'.verified.json','w'),indent=2);os.remove(comp);print('VERIFIED',meta,flush=True)
 if time.time()-start>35:break

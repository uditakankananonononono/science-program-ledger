import ctypes,ctypes.util,json,urllib.request,time,os,base64
root='/tmp/unit165/';f=next(f for f in json.load(open(root+'live-api.json'))['files'] if f['key']=='sEMG_data.zip')
lib=ctypes.CDLL(ctypes.util.find_library('crypto'));ctx=ctypes.create_string_buffer(92)
p=root+'hash-progress.json';state=json.load(open(p)) if os.path.exists(p) else None
if state:ctypes.memmove(ctx,base64.b64decode(state['ctx']),92);off=state['bytes']
else:lib.MD5_Init(ctx);off=0
start=time.time()
while off<f['size'] and time.time()-start<50:
 end=min(off+32*1024*1024,f['size'])-1
 req=urllib.request.Request(f['links']['self'],headers={'Range':f'bytes={off}-{end}'})
 with urllib.request.urlopen(req,timeout=30) as r:
  assert r.status==206 and r.headers.get('Content-Range')==f"bytes {off}-{end}/{f['size']}"
  data=r.read();assert len(data)==end-off+1
 lib.MD5_Update(ctx,data,len(data));off=end+1
 json.dump({'bytes':off,'ctx':base64.b64encode(ctx.raw).decode(),'purpose':'MD5 cryptographic accumulator, not sensor payload'},open(p,'w'))
 print(off,round(time.time()-start,1),flush=True)
 time.sleep(2)
if off==f['size']:
 digest=ctypes.create_string_buffer(16);lib.MD5_Final(digest,ctx);h=digest.raw.hex()
 out={'url':f['links']['self'],'bytes':off,'expected_md5':f['checksum'],'actual_md5':h,'match':'md5:'+h==f['checksum'],'operation':'complete byte sequence hash-only in ranged segments; no TEST payload parsed or stored'}
 json.dump(out,open(root+'raw-stream-verification.json','w'),indent=2);print(out)

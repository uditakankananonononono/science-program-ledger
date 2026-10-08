"""Q5 scanner adapted from separately pinned A2 original; directory only."""
import json,re,stat,struct,zipfile
def extras(raw):
 pos=0
 while pos<len(raw):
  if pos+4>len(raw):raise ValueError('malformed extra header')
  typ,n=struct.unpack_from('<HH',raw,pos);pos+=4
  if pos+n>len(raw) or typ==1:raise ValueError('malformed/ZIP64 extra')
  pos+=n
def unsafe(name,flag,creator,attr):
 if '\x00' in name or flag&1 or flag&64:raise ValueError('NUL/encrypted entry')
 normalized=name.replace('\\','/')
 if normalized.startswith('/') or re.match('^[A-Za-z]:',normalized) or '..' in normalized.split('/'):raise ValueError('unsafe absolute/drive/traversal name')
 if creator>>8==3 and stat.S_ISLNK(attr>>16):raise ValueError('symlink entry')
def directory(f,sel):
 f.seek(0,2);size=f.tell();f.seek(max(0,size-65557));tail=f.read(65557);start=size-len(tail);candidates=[]
 for i in range(len(tail)-21):
  if tail[i:i+4]==b'PK\x05\x06':
   fields=struct.unpack_from('<4s4H2IH',tail,i)
   if i+22+fields[-1]==len(tail):candidates.append((start+i,fields))
 if len(candidates)!=1:raise ValueError('missing/conflicting exact EOF EOCD')
 offset,(_,disk,cdisk,n_disk,n,cdsize,cdoffset,clen)=candidates[0]
 if disk or cdisk or n_disk!=n:raise ValueError('multipart/count mismatch')
 if n in (65535,) or cdsize==4294967295 or cdoffset==4294967295:raise ValueError('ZIP64 sentinel')
 if offset>=20:
  f.seek(offset-20)
  if f.read(4)==b'PK\x06\x07':raise ValueError('ZIP64 locator')
 if n>sel['max_entries'] or cdsize>sel['max_central_directory_bytes'] or cdoffset+cdsize!=offset or cdoffset>size:raise ValueError('directory caps/range/end alignment')
 f.seek(cdoffset);cd=f.read(cdsize)
 if len(cd)!=cdsize:raise ValueError('truncated central directory')
 pos=0;records=[];allocation_charge=0
 while pos<len(cd):
  if len(records)>=n or pos+46>len(cd):raise ValueError('central count/header bounds')
  v=struct.unpack_from('<4s6H3I5H2I',cd,pos)
  sig,creator,need,flag,comp,tm,dt,crc,csize,usize,nlen,elen,mlen,dstart,iattr,eattr,hoff=v
  if sig!=b'PK\x01\x02' or dstart or need>=45 or 4294967295 in (csize,usize,hoff):raise ValueError('central malformed/ZIP64/multipart')
  end=pos+46+nlen+elen+mlen
  if end>len(cd) or hoff>=cdoffset:raise ValueError('central record/name/local range')
  if nlen>16384 or elen>4096 or mlen>4096:raise ValueError('raw variable-field cap')
  # Conservative Python-record/string plus escaped/hex serialized-output bound.
  charge=8192+64*(nlen+elen+mlen)
  allocation_charge+=charge
  if allocation_charge>67108864:raise ValueError('aggregate record/output allocation cap')
  namebytes=cd[pos+46:pos+46+nlen];extra=cd[pos+46+nlen:pos+46+nlen+elen];comment=cd[pos+46+nlen+elen:end]
  name=namebytes.decode('utf-8' if flag&2048 else 'cp437',errors='strict');extras(extra);unsafe(name,flag,creator,eattr)
  if len(name)>sel['max_member_name_characters']:raise ValueError('member name cap')
  records.append({'filename':name,'raw_filename_hex':namebytes.hex(),'flags':flag,'compression':comp,'crc':crc,'compressed_size':csize,'uncompressed_size':usize,'header_offset':hoff,'create_version':creator,'required_version':need,'dos_time':tm,'dos_date':dt,'disk_start':dstart,'internal_attr':iattr,'external_attr':eattr,'extra_hex':extra.hex(),'comment_hex':comment.hex()});pos=end
 if len(records)!=n or pos!=cdsize:raise ValueError('central actual count/bytes mismatch')
 if len({r['filename'] for r in records})!=len(records):raise ValueError('duplicate name')
 # Central-declared minimum local header plus name/extra/compressed data spans.
 # No local bytes read: conservative over-rejection possible if local/central extra differ.
 spans=sorted((a['header_offset'],a['header_offset']+30+len(bytes.fromhex(a['raw_filename_hex']))+len(bytes.fromhex(a['extra_hex']))+a['compressed_size']) for a in records)
 for i,(lo,hi) in enumerate(spans):
  if lo<0 or hi>cdoffset or hi<lo or (i and lo<spans[i-1][1]):raise ValueError('central-declared local span bounds/overlap')
 # Allocation now bounded by fully scanned central bytes and entry count, not EOCD alone.
 with zipfile.ZipFile(f,'r') as z:
  infos=z.infolist()
  if len(infos)!=n or z.start_dir!=cdoffset:raise ValueError('ZipFile count/start mismatch')
  for ordinal,(a,b) in enumerate(zip(records,infos),1):
   for key,other in [('filename',b.filename),('flags',b.flag_bits),('compression',b.compress_type),('crc',b.CRC),('compressed_size',b.compress_size),('uncompressed_size',b.file_size),('header_offset',b.header_offset),('external_attr',b.external_attr),('extra_hex',b.extra.hex()),('comment_hex',b.comment.hex()),('required_version',b.extract_version),('internal_attr',b.internal_attr)]:
    if a[key]!=other:raise ValueError('parser disagreement '+key)
   if a['create_version']!=b.create_system*256+b.create_version:raise ValueError('creator disagreement')
   a.update(ordinal_1based=ordinal,filename_repr=repr(a['filename']),datetime=list(b.date_time))
 return {'status':'complete_bounded_directory_metadata','entries':records,'entry_count':n,'central_directory_bytes':cdsize,'central_directory_offset':cdoffset,'EOCD_offset':offset,'comment_hex':tail[-clen:].hex() if clen else '', 'allocation_charge':allocation_charge,'claims':'central directory only; local minimum-span bounds are conservative central declarations, not verified local headers/member CRC/content/extraction'}

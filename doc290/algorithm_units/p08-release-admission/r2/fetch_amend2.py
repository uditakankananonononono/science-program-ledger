"""Finite once-validated address failover before HTTP bytes only."""
import hashlib,http.client,ipaddress,json,socket,ssl,sys,urllib.parse,urllib.request
from pathlib import Path
import admit,fetch_amend1 as previous
class Connection(previous.PinnedHTTPSConnection):
    def __init__(self,host,ip,timeout=20):
        super().__init__(host,ip,timeout);self.connect_called=False
    def connect(self):
        if self.connect_called:raise ValueError('automatic reconnect forbidden')
        self.connect_called=True;super().connect()
        self.auto_open=0 # http.client cannot reconnect after explicit TLS boundary.

def request(url,checked,step,connection_factory=Connection):
    p=urllib.parse.urlsplit(url);addresses=tuple(checked['dns_addresses'])
    attempts=[];step['address_attempts']=attempts
    c=None
    for ip in addresses:
        if not ipaddress.ip_address(ip).is_global:raise ValueError('invalid connection address')
        a={'address':ip};attempts.append(a);candidate=connection_factory(p.hostname,ip)
        try:candidate.connect() # EXPLICIT connect + TLS, before putrequest/endheaders.
        except Exception as e:
            a['error']=type(e).__name__+': '+str(e);candidate.close();continue
        a['status']='TLS_connected';c=candidate;step['successful_address']=ip;break
    if c is None:raise OSError('all validated addresses failed connection/TLS')
    # Outside address loop: ANY write/read/status failure stops, no failover/resend.
    path=urllib.parse.urlunsplit(('', '',p.path or '/',p.query,''))
    try:
        c.putrequest('GET',path,skip_host=True,skip_accept_encoding=True)
        for k,v in {'Host':p.netloc,'Accept-Encoding':'identity','User-Agent':'source-admission/redirect-amend2'}.items():c.putheader(k,v)
        c.endheaders()
        return previous.PinnedResponse(c.getresponse(),c,url)
    except Exception:
        c.close();raise

def fetch(url,limit,budget,chain,resolver=socket.getaddrinfo,requester=request):
    current=url;seen=set();hops=0
    while True:
        step={'requested_url':current};chain.append(step)
        try:
            if current in seen:raise ValueError('redirect loop before request')
            checked=previous.target(current,resolver);step['validated_dns']=checked['dns_addresses'];seen.add(current)
            r=requester(current,checked,step)
            try:
                step['status']=r.status
                if r.geturl()!=current:raise ValueError('unrecorded redirect')
                if r.status in (301,302,303,307,308):
                    loc=r.headers.get('Location');step['raw_location']=loc
                    if hops>=3:raise ValueError('fourth redirect before destination request')
                    if not isinstance(loc,str) or not loc or any(ord(c)<=32 or ord(c)==127 for c in loc) or '#' in loc or '\\' in loc:raise ValueError('malformed Location')
                    destination=urllib.parse.urljoin(current,loc);step['resolved_url']=destination
                    # Syntax checks + DNS happen ONCE in next iteration before request.
                    # No request is sent before previous.target validates the destination.
                    if destination in seen:raise ValueError('loop before destination request')
                    current=destination;hops+=1;continue
                if r.status!=200:raise ValueError('final status not200')
                step['final_url']=current
                return admit.download(current,limit,budget,previous.ResponseOpener(r))
            finally:r.close()
        except Exception as e:step['error']=type(e).__name__+': '+str(e);raise

def run(folder):
    root=Path(__file__).parent
    for manifest in ['freeze-hashes.sha256','amend1-hashes.sha256','amend2-hashes.sha256']:
        for line in (root/manifest).read_text().splitlines():
            h,n=line.split('  ',1)
            if hashlib.sha256((root/n).read_bytes()).hexdigest()!=h:raise ValueError('hash mismatch '+n)
    sel=json.loads((root/'selection.json').read_text());s=sel['files'][0]
    out=Path(folder);out.mkdir(exist_ok=False);(out/'sources').mkdir();chain=[]
    rec={**s,'status':'unavailable','parser_calls':0,'visual_performed':False,'redirect_chain':chain}
    try:
        raw=fetch(s['url'],sel['max_file_bytes'],[sel['max_total_source_bytes']],chain)
        (out/'sources'/s['path']).write_bytes(raw);rec.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),md5=hashlib.md5(raw).hexdigest())
        admit.verify(raw,s);rec['status']='verified'
    except Exception as e:rec['error']=type(e).__name__+': '+str(e)
    (out/'identity.json').write_text(json.dumps(rec,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])

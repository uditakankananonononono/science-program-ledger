"""Amendment1 identity-only fetch; no parser/visual calls."""
import hashlib,http.client,ipaddress,json,socket,ssl,sys,urllib.error,urllib.parse,urllib.request
from pathlib import Path
import admit

def target(url,resolver=socket.getaddrinfo):
    if not isinstance(url,str) or any(ord(c)<=32 or ord(c)==127 for c in url) or '#' in url or '\\' in url:raise ValueError('URL controls/fragment/backslash')
    p=urllib.parse.urlsplit(url)
    if p.scheme!='https' or p.username is not None or p.password is not None or not p.hostname or p.port not in (None,443):raise ValueError('HTTPS host/port/credentials')
    host=p.hostname.lower()
    if host.endswith('.') or '%' in host or not all(c in 'abcdefghijklmnopqrstuvwxyz0123456789.-' for c in host) or '.' not in host:raise ValueError('host syntax/local')
    try:ipaddress.ip_address(host)
    except ValueError:pass
    else:raise ValueError('literal IP')
    if host=='localhost' or host.endswith(('.localhost','.local','.internal','.home','.lan')):raise ValueError('local host')
    answers=resolver(host,443,type=socket.SOCK_STREAM)
    if not answers:raise ValueError('empty DNS')
    ips=sorted({a[4][0] for a in answers})
    if any(not ipaddress.ip_address(ip).is_global for ip in ips):raise ValueError('DNS nonpublic target')
    return {'url':url,'dns_addresses':ips}

class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self,host,ip,timeout=20):
        self.validated_ip=ip
        super().__init__(host,port=443,timeout=timeout,context=ssl.create_default_context())
    def connect(self):
        if not ipaddress.ip_address(self.validated_ip).is_global:raise ValueError('connection IP not public')
        # Numeric address only; original hostname is never resolved at connect time.
        self.sock=socket.create_connection((self.validated_ip,443),self.timeout,self.source_address)
        try:self.sock=self._context.wrap_socket(self.sock,server_hostname=self.host)
        except Exception:
            self.sock.close();raise
class PinnedResponse:
    def __init__(self,response,connection,url):
        self.response=response;self.connection=connection;self.url=url
        self.status=response.status;self.headers=response.headers
    def geturl(self):return self.url
    def read(self,n):return self.response.read(n)
    def close(self):
        self.response.close();self.connection.close()
    def __enter__(self):return self
    def __exit__(self,*args):self.close()
def request_pinned(url,checked):
    p=urllib.parse.urlsplit(url);ip=checked['dns_addresses'][0]
    c=PinnedHTTPSConnection(p.hostname,ip)
    path=urllib.parse.urlunsplit(('', '',p.path or '/',p.query,''))
    try:
        c.putrequest('GET',path,skip_host=True,skip_accept_encoding=True)
        for key,value in {'Host':p.netloc,'Accept-Encoding':'identity','User-Agent':'source-admission/redirect-amend1'}.items():c.putheader(key,value)
        c.endheaders()
        return PinnedResponse(c.getresponse(),c,url)
    except Exception:
        c.close();raise

class ResponseOpener:
    def __init__(self,r):self.r=r
    def open(self,req,timeout):return self.r

def fetch(url,limit,budget,chain,opener=None,resolver=socket.getaddrinfo):
    current=url;seen=set();hops=0
    while True:
        step={'requested_url':current};chain.append(step)
        try:
            if current in seen:raise ValueError('redirect loop before request')
            checked=target(current,resolver);step['validated_dns']=checked['dns_addresses'];seen.add(current)
            req=urllib.request.Request(current,headers={'Accept-Encoding':'identity','User-Agent':'source-admission/redirect-amend1'})
            if opener is None:r=request_pinned(current,checked)
            else:
                try:r=opener.open(req,timeout=20)
                except urllib.error.HTTPError as e:r=e
            status=getattr(r,'status',getattr(r,'code',None));step['status']=status
            if r.geturl()!=current:r.close();raise ValueError('unrecorded implicit redirect')
            if status in (301,302,303,307,308):
                loc=r.headers.get('Location');step['raw_location']=loc;r.close()
                if hops>=3:raise ValueError('fourth redirect stopped before destination request')
                if not isinstance(loc,str) or not loc or any(ord(c)<=32 or ord(c)==127 for c in loc) or '#' in loc or '\\' in loc:raise ValueError('malformed Location')
                destination=urllib.parse.urljoin(current,loc);step['resolved_url']=destination
                target(destination,resolver) # check BEFORE ever requesting the hop
                if destination in seen:raise ValueError('redirect loop before destination request')
                current=destination;hops+=1;continue
            if status!=200:r.close();raise ValueError('final status not200')
            target(r.geturl(),resolver);step['final_url']=r.geturl()
            return admit.download(current,limit,budget,ResponseOpener(r))
        except Exception as e:
            step['error']=type(e).__name__+': '+str(e);raise

def run(folder):
    root=Path(__file__).parent
    for manifest in ['freeze-hashes.sha256','amend1-hashes.sha256']:
        for line in (root/manifest).read_text().splitlines():
            h,n=line.split('  ',1)
            if hashlib.sha256((root/n).read_bytes()).hexdigest()!=h:raise ValueError('manifest mismatch '+n)
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

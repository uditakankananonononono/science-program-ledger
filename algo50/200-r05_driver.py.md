#!/usr/bin/env python3
"""R-05 (unit 200) driver. Implements PREREG 200 (v5). Subcommands:
 meta  : parse uniprot_sprot.dat.gz -> meta TSV (acc, created, sequpdate, signal ranges)
 genctl: generate control sets (seed per draw) + manifest
 l1    : mmseqs2 easy-search (frozen command) -> hits JSON
 l2    : exhaustive parasail Smith-Waterman -> hits JSON
 n1    : NCBI blastp nr singles (state file, resumable, courtesy rules)
 n2    : NCBI blastp short-adjust batched, report-only
 score : apply hit rule + gate G + labels -> result JSON
 dates : drift dating of flipped NCBI hits (efetch create-date, earliest over identical proteins)
 udates: drift dating of flipped UniProt hits (later of entry creation and last sequence update, from meta TSV)
"""
import sys, os, json, gzip, math, random, hashlib, time, re, subprocess, collections, argparse, datetime
# ---------- constants (frozen) ----------
AA = "ACDEFGHIKLMNPQRSTVWY"
HYDRO = set("AVILMFWC")
ENT_TOL, HYD_TOL, KR_TOL = 0.15, 0.15, 0.10
MAXDRAW = 10000
CREATED_MAX = "2026-09-01"
DRAWS = {1: 200200, 2: 200201}
SUBMIT_SPACING = 15
POLL_SPACING = 60
MAX_INFLIGHT = 3
CAP_24H = 90
RID_TIMEOUT = 3600
MAX_RESUB = 2
NCBI = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
TOOL = "algo50-r05-audit"
EMAIL = os.environ.get("R05_EMAIL", "sspou3@mail.instinct.com")  # agent mailbox as NCBI contact (parent decision)
UA = "algo50-r05-audit/1.0 (public ledger science-program-ledger)"
MMSEQS_CMD = ("easy-search {q} {db} {out} {tmp} -s 7.5 -e 10 --threads 2 --max-seqs 1000 "
              "--alignment-mode 3 --cov-mode 2 -c 0.0 "
              "--format-output query,target,pident,alnlen,qstart,qend,tstart,tend,qlen,evalue,bits,qaln,taln")
SW_OPEN, SW_EXT = 12, 1
L2_PREFILTER_SCORE = 20   # lenient; any hit-rule-qualifying alignment of a >=13-mer scores far above this

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def shas(s): return hashlib.sha256(s.encode()).hexdigest()
def opn(p): return gzip.open(p, 'rt') if p.endswith('.gz') else open(p)
def read_fasta(p):
    out, name, buf = [], None, []
    with opn(p) as f:
        for l in f:
            if l.startswith('>'):
                if name is not None: out.append((name, ''.join(buf)))
                name, buf = l[1:].strip(), []
            else: buf.append(l.strip())
    if name is not None: out.append((name, ''.join(buf)))
    return out
def write_fasta(p, items):
    with open(p, 'w') as f:
        for n, s in items: f.write(f">{n}\n{s}\n")

def entropy(s):
    c = collections.Counter(s); n = len(s)
    return -sum(v / n * math.log2(v / n) for v in c.values())
def hydro_frac(s): return sum(ch in HYDRO for ch in s) / len(s)
def kr_frac(s): return sum(ch in 'KR' for ch in s) / len(s)
def kmers(s, k=6): return {s[i:i + k] for i in range(len(s) - k + 1)}

# ---------- hit rule ----------
def hsp_stats(qaln, taln, qstart, qend, qlen):
    alnlen = len(qaln)
    ident = sum(a == b and a != '-' for a, b in zip(qaln, taln))
    return ident / alnlen, (qend - qstart + 1) / qlen, alnlen
def classify(hsps):
    """hsps: list of dict(identity, coverage, subject...). Each HSP stands alone (no merging)."""
    if any(h['coverage'] >= 0.8 and h['identity'] >= 0.9 for h in hsps): return 'NOT_NOVEL'
    if any(h['coverage'] >= 0.8 and h['identity'] >= 0.7 for h in hsps): return 'NEAR'
    return 'NOVEL'
def best_hsp(hsps):
    c = [h for h in hsps if h['coverage'] >= 0.8]
    return max(c, key=lambda h: h['identity']) if c else None

def clopper_pearson_lower(k, n, a=0.05):
    if k == 0: return 0.0
    lo, hi = 0.0, k / n
    # solve P(X>=k | p) = a/2 for p by bisection
    def tail(p): return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))
    lo, hi = 0.0, 1.0
    for _ in range(100):
        m = (lo + hi) / 2
        if tail(m) < a / 2: lo = m
        else: hi = m
    return (lo + hi) / 2

# ---------- meta ----------
def cmd_meta(a):
    out = open(a.out, 'w'); acc = None; created = upd = None; sig = []
    mon = {m: i for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split(), 1)}
    def iso(s):
        d, m, y = s.split('-'); return f"{y}-{mon[m]:02d}-{int(d):02d}"
    with opn(a.dat) as f:
        for l in f:
            if l.startswith('AC   ') and acc is None: acc = l[5:].split(';')[0].strip()
            elif l.startswith('DT   '):
                if 'integrated into' in l: created = iso(l[5:16])
                elif 'sequence version' in l: upd = iso(l[5:16])
            elif l.startswith('FT   SIGNAL'):
                m = re.search(r'(\d+)\.\.(\d+)', l); 
                if m: sig.append(f"{m.group(1)}-{m.group(2)}")
            elif l.startswith('//'):
                out.write(f"{acc}\t{created}\t{upd}\t{','.join(sig)}\n"); acc = created = upd = None; sig = []
    out.close()

def load_meta(p):
    m = {}
    for l in open(p):
        acc, c, u, sg = l.rstrip('\n').split('\t')
        m[acc] = (c, u, sg)
    return m
def acc_of(name):
    return name.split('|')[1] if name.startswith(('sp|', 'tr|')) else name.split()[0]

# ---------- genctl ----------
def mutate(s, rng, n):
    pos = rng.sample(range(len(s)), n); l = list(s); rec = []
    for p in sorted(pos):
        r = rng.choice([x for x in AA if x != l[p]]); rec.append((p + 1, l[p], r)); l[p] = r
    return ''.join(l), rec

def cmd_genctl(a):
    cands = read_fasta(a.cands); cands.sort()
    cand_k = set().union(*[kmers(s) for _, s in cands])
    sp = read_fasta(a.sprot); meta = load_meta(a.meta)
    pool = [(acc_of(n), s) for n, s in sp
            if len(s) >= 13 and meta.get(acc_of(n), ('9999',))[0] <= CREATED_MAX]
    seed = DRAWS[a.draw]; rng = random.Random(seed)
    items, manifest, used = [], [], set()
    for cname, cs in cands:
        L = len(cs); e0, h0, k0 = entropy(cs), hydro_frac(cs), kr_frac(cs)
        found = None
        for t in range(MAXDRAW):
            acc, s = pool[rng.randrange(len(pool))]
            if len(s) < L: continue
            off = rng.randrange(len(s) - L + 1); w = s[off:off + L]
            if set(w) - set(AA): continue                      # excludes X/B/Z/U/O
            if (acc, off) in used: continue
            if abs(entropy(w) - e0) > ENT_TOL or abs(hydro_frac(w) - h0) > HYD_TOL or abs(kr_frac(w) - k0) > KR_TOL: continue
            if kmers(w) & cand_k: continue
            found = (acc, off, w, t + 1); break
        base = dict(candidate=cname, length=L, draw=a.draw, seed=seed)
        if found is None:
            for cl in ('C1', 'C2', 'C3'): manifest.append(dict(base, cls=cl, status='unmatched'))
        else:
            acc, off, w, tries = found; used.add((acc, off))
            sg = meta[acc][2]
            sigov = any(int(x.split('-')[0]) <= off + L and int(x.split('-')[1]) > off for x in sg.split(',') if x)
            common = dict(base, status='ok', source_acc=acc, offset0=off, tries=tries, source_created=meta[acc][0],
                          entropy=round(entropy(w), 4), hydro=round(hydro_frac(w), 4), kr=round(kr_frac(w), 4),
                          signal_overlap=sigov)
            manifest.append(dict(common, cls='C1', seq=w, subs=[]))
            w2, r2 = mutate(w, rng, 1); manifest.append(dict(common, cls='C2', seq=w2, subs=r2))
            w3, r3 = mutate(w, rng, 2); manifest.append(dict(common, cls='C3', seq=w3, subs=r3))
        for _ in range(1000):
            l = list(cs); rng.shuffle(l); sh = ''.join(l)
            if sh != cs: break
        manifest.append(dict(base, cls='C4', status='ok', seq=sh, subs=[]))
    for i, m in enumerate(manifest):
        m['qid'] = f"d{a.draw}_{m['cls']}_{cands_index(cands, m['candidate']):02d}"
    os.makedirs(a.outdir, exist_ok=True)
    for cl in ('C1', 'C2', 'C3', 'C4'):
        write_fasta(f"{a.outdir}/draw{a.draw}_{cl}.fa", [(m['qid'], m['seq']) for m in manifest if m['cls'] == cl and m['status'] == 'ok'])
    json.dump(dict(draw=a.draw, seed=seed, sprot_sha256=sha(a.sprot), sprot_dat_sha256=sha(a.dat), meta_tsv_sha256=sha(a.meta), cands_sha256=sha(a.cands), n_unmatched=sum(m['status'] != 'ok' for m in manifest), controls=manifest),
              open(f"{a.outdir}/draw{a.draw}_manifest.json", 'w'), indent=1)
    print('draw', a.draw, 'ok', sum(m['status'] == 'ok' for m in manifest), 'unmatched', sum(m['status'] != 'ok' for m in manifest))
def cands_index(cands, name): return [n for n, _ in cands].index(name)

# ---------- parsing of results into uniform hsp records ----------
def parse_m8(path, qlens):
    res = collections.defaultdict(list)
    for l in open(path):
        f = l.rstrip('\n').split('\t')
        q, t, pid, alnlen, qs, qe, ts, te, qlen, ev, bits, qaln, taln = f
        idn, cov, al = hsp_stats(qaln, taln, int(qs), int(qe), int(qlen))
        res[q].append(dict(subject=t, identity=idn, coverage=cov, alnlen=al, evalue=float(ev), mmseqs_pident=float(pid)))
    return res
def parse_ncbi_json2(obj):
    """returns {query_title: dict(hsps=[...], nhits=int, header=dict)}"""
    out = {}
    for bo in obj['BlastOutput2']:
        rp = bo['report']; s = rp['results']['search']; qlen = s['query_len']
        hsps = []
        for h in s.get('hits', []):
            d0 = h['description'][0]
            for hs in h['hsps']:
                idn = hs['identity'] / hs['align_len']; cov = (hs['query_to'] - hs['query_from'] + 1) / qlen
                hsps.append(dict(subject=d0.get('accession'), title=d0.get('title'), taxid=d0.get('taxid'), identity=idn,
                                 coverage=cov, alnlen=hs['align_len'], evalue=hs['evalue']))
        out[s['query_title'] if 'query_title' in s else s['query_id']] = dict(
            hsps=hsps, nhits=len(s.get('hits', [])), at_cap=len(s.get('hits', [])) >= 100,
            header=dict(version=rp.get('version'), db=rp.get('search_target'), params=rp.get('params')))
    return out

# ---------- L1 ----------
def cmd_l1(a):
    qs = read_fasta_dir(a.qfa); os.makedirs(a.outdir, exist_ok=True)
    allq = f"{a.outdir}/all_queries.fa"; write_fasta(allq, qs)
    out = f"{a.outdir}/l1.m8"
    cmd = [a.mmseqs] + MMSEQS_CMD.format(q=allq, db=a.sprot, out=out, tmp=f"{a.outdir}/tmp", **{}).split()
    ver = subprocess.run([a.mmseqs, 'version'], capture_output=True, text=True).stdout.strip()
    defaults = subprocess.run([a.mmseqs, 'easy-search', '-h'], capture_output=True, text=True).stdout
    dflt = [l.strip() for l in defaults.splitlines() if re.search(r'--min-seq-id|--gap-open|--gap-extend|--seed-sub-mat|--sub-mat', l)]
    print('mmseqs version', ver, '\ndefaults:', *dflt, sep='\n  ')
    subprocess.run(cmd, check=True)
    res = parse_m8(out, None)
    json.dump(dict(arm='L1', mmseqs_version=ver, binary_sha256=sha(a.mmseqs), command=' '.join(cmd), sprot_sha256=sha(a.sprot),
                   defaults=dflt, queries=[q for q, _ in qs],
                   hsps={q: res.get(q, []) for q, _ in qs}), open(f"{a.outdir}/l1_hits.json", 'w'))
def read_fasta_dir(paths):
    out = []
    for p in paths: out += read_fasta(p)
    return out

# ---------- L2 ----------
def _l2_worker(args):
    import parasail
    qid, q, sprot_path = args
    mat = parasail.blosum62; prof = parasail.profile_create_16(q, mat)
    hsps = []
    with opn(sprot_path) as f:
        name, buf = None, []
        def handle(name, t):
            r = parasail.sw_striped_profile_16(prof, t, SW_OPEN, SW_EXT)
            if r.score >= L2_PREFILTER_SCORE:
                tr = parasail.sw_trace_striped_16(q, t, SW_OPEN, SW_EXT, mat)
                tb = tr.traceback; qa, ta = tb.query, tb.ref
                nq = sum(ch != '-' for ch in qa)
                qs = tr.end_query + 2 - nq   # 1-based start; end_query is 0-based inclusive end
                qe = tr.end_query + 1
                idn, cov, al = hsp_stats(qa, ta, qs, qe, len(q))
                hsps.append(dict(subject=acc_of(name), identity=idn, coverage=cov, alnlen=al, score=tr.score))
        for l in f:
            if l.startswith('>'):
                if name is not None: handle(name, ''.join(buf))
                name, buf = l[1:].strip(), []
            else: buf.append(l.strip())
        if name is not None: handle(name, ''.join(buf))
    return qid, hsps
def cmd_l2(a):
    import parasail, multiprocessing as mp
    qs = read_fasta_dir(a.qfa); os.makedirs(a.outdir, exist_ok=True)
    with mp.Pool(2) as p: res = dict(p.map(_l2_worker, [(n, s, a.sprot) for n, s in qs], chunksize=1))
    json.dump(dict(arm='L2', parasail_version=parasail.__version__ if hasattr(parasail, '__version__') else 'unknown',
                   matrix='BLOSUM62', gap_open=SW_OPEN, gap_extend=SW_EXT, prefilter_score=L2_PREFILTER_SCORE,
                   sprot_sha256=sha(a.sprot), queries=[n for n, _ in qs], hsps=res), open(f"{a.outdir}/l2_hits.json", 'w'))

# ---------- NCBI runner ----------
import urllib.request, urllib.parse, urllib.error, zoneinfo
class Throttle(Exception): pass
_fail = [0]
def http(url, data=None):
    """Transient errors (HTTP 429/5xx, URL/socket errors) are retried with backoff; 3 consecutive failures raise Throttle (run stops)."""
    body = urllib.parse.urlencode(data).encode() if data else None
    while True:
        req = urllib.request.Request(url, data=body, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                _fail[0] = 0; return r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504): raise
            err = f"HTTP {e.code}"
        except (urllib.error.URLError, OSError, TimeoutError) as e:
            err = f"net {e}"
        _fail[0] += 1
        if _fail[0] >= 3: raise Throttle(f"{err} x3 consecutive")
        time.sleep(60 * _fail[0])
def in_window(now_utc):
    et = now_utc.astimezone(zoneinfo.ZoneInfo('America/New_York'))
    return et.weekday() >= 5 or et.hour >= 21 or et.hour < 5
def n1_params(kind):
    if kind == 'N1':
        return dict(tool=TOOL, email=EMAIL, CMD='Put', PROGRAM='blastp', DATABASE='nr', EXPECT='10', HITLIST_SIZE='100', FORMAT_TYPE='JSON2_S')
    return dict(tool=TOOL, email=EMAIL, CMD='Put', PROGRAM='blastp', DATABASE='nr', EXPECT='20000', HITLIST_SIZE='100', FORMAT_TYPE='JSON2_S',
                SHORT_QUERY_ADJUST='true', MATRIX='PAM30', GAPCOSTS='9 1', FILTER='F', COMPOSITION_BASED_STATISTICS='0')
def cmd_ncbi(a, kind):
    if not EMAIL: sys.exit('R05_EMAIL not set (NCBI contact address required)')
    state_p = f"{a.outdir}/{kind}_state.json"; os.makedirs(f"{a.outdir}/raw", exist_ok=True)
    if os.path.exists(state_p): st = json.load(open(state_p))
    else:
        qs = read_fasta_dir(a.qfa)   # order of qfa list = frozen order
        if kind == 'N1': items = [dict(id=n, fasta=f">{n}\n{s}\n", qhash=shas(s)) for n, s in qs]
        else:
            items = []
            for i in range(0, len(qs), 32):
                ch = qs[i:i + 32]
                items.append(dict(id=f"{kind}_batch{i // 32}", fasta=''.join(f">{n}\n{s}\n" for n, s in ch), qhash=shas(''.join(s for _, s in ch)), members=[n for n, _ in ch]))
        st = dict(items=[dict(i, status='queued', attempts=0, submits=[], rid=None, polls=[]) for i in items], submit_times=[], stopped=None)
    def save(): json.dump(st, open(state_p, 'w'), indent=1)
    last_submit = 0; last_poll = {}
    try:
        while True:
            now = time.time(); utc = datetime.datetime.now(datetime.timezone.utc)
            inflight = [i for i in st['items'] if i['status'] == 'running']
            queued = [i for i in st['items'] if i['status'] == 'queued']
            if kind == 'N1' and not st.get('early_stop_checked'):
                pre = [i for i in st['items'] if not i['id'].startswith('d2_')]
                if all(i['status'] in ('done', 'not_run') for i in pre):
                    if early_stop(pre, a.ctl):
                        for i in st['items']:
                            if i['id'].startswith('d2_') and i['status'] == 'queued': i['status'] = 'not_run'; i['note'] = 'not run (G already failed in draw 1)'
                        st['early_stop'] = True
                    st['early_stop_checked'] = True; save(); continue
            if not inflight and not queued: break
            # submit
            recent = [t for t in st['submit_times'] if now - t < 86400]
            if queued and len(inflight) < MAX_INFLIGHT and now - last_submit >= SUBMIT_SPACING and len(recent) < CAP_24H and in_window(utc):
                it = queued[0]
                prm = n1_params(kind); prm['QUERY'] = it['fasta']
                txt = http(NCBI, prm)
                m = re.search(r'RID = (\S+)', txt); r = re.search(r'RTOE = (\d+)', txt)
                last_submit = time.time(); st['submit_times'].append(last_submit)
                it['attempts'] += 1
                if not m: it['submits'].append(dict(t=last_submit, error='no RID')); it['status'] = 'queued' if it['attempts'] <= MAX_RESUB else 'not_run'
                else:
                    it.update(rid=m.group(1), rtoe=int(r.group(1)) if r else None, status='running', t_submit=last_submit)
                    it['submits'].append(dict(t=last_submit, utc=utc.isoformat(), et=utc.astimezone(zoneinfo.ZoneInfo('America/New_York')).isoformat(), rid=m.group(1)))
                save(); continue
            # poll
            for it in inflight:
                if now - last_poll.get(it['rid'], 0) < POLL_SPACING: continue
                if now - it['t_submit'] > RID_TIMEOUT:
                    it['status'] = 'queued' if it['attempts'] <= MAX_RESUB else 'not_run'; it['polls'].append(dict(t=now, status='TIMEOUT')); save(); continue
                txt = http(NCBI + '?' + urllib.parse.urlencode(dict(tool=TOOL, email=EMAIL, CMD='Get', FORMAT_OBJECT='SearchInfo', RID=it['rid'])))
                last_poll[it['rid']] = time.time()
                s = re.search(r'Status=(\w+)', txt); s = s.group(1) if s else 'UNKNOWN'
                it['polls'].append(dict(t=time.time(), status=s))
                if s == 'READY':
                    body = http(NCBI + '?' + urllib.parse.urlencode(dict(tool=TOOL, email=EMAIL, CMD='Get', FORMAT_TYPE='JSON2_S', RID=it['rid'])))
                    p = f"{a.outdir}/raw/{kind}_{it['id']}_{it['rid']}.json"; open(p, 'w').write(body)
                    it.update(status='done', raw=p, raw_sha256=sha(p))
                elif s in ('FAILED', 'UNKNOWN'):
                    it['status'] = 'queued' if it['attempts'] <= MAX_RESUB else 'not_run'
                save(); time.sleep(2)
            time.sleep(5)
    except Throttle as e:
        st['stopped'] = f"THROTTLE: {e}"; save(); print('STOP', e); sys.exit(3)
    save(); print(kind, 'finished', collections.Counter(i['status'] for i in st['items']))

def early_stop(pre_items, ctl):
    """True if draw-1 C1 or C2 point sensitivity < 0.80 (N1)."""
    calls = {}
    for it in pre_items:
        if it['status'] == 'done':
            for q, rec in parse_ncbi_json2(json.load(open(it['raw']))).items(): calls[it['id']] = classify(rec['hsps'])
    man = json.load(open(f"{ctl}/draw1_manifest.json"))['controls']
    for cl in ('C1', 'C2'):
        ms = [m for m in man if m['cls'] == cl]   # denominator = all manifest controls; unmatched or not run = not flagged
        if ms and sum(m['status'] == 'ok' and calls.get(m['qid']) == 'NOT_NOVEL' for m in ms) / len(ms) < 0.80: return True
    return False

# ---------- score ----------
def cmd_score(a):
    man = {d: json.load(open(f"{a.ctl}/draw{d}_manifest.json")) for d in (1, 2)}
    cand_ids = [n for n, _ in read_fasta(a.cands)]
    arms = {}
    for arm in a.arms:   # name=path
        name, p = arm.split('=')
        arms[name] = load_arm(name, p)
    out = {}
    for name, hs in arms.items():
        o = dict(per_query={}, cls={})
        for qid, rec in hs.items(): o['per_query'][qid] = dict(call=classify(rec['hsps']), best=best_hsp(rec['hsps']), at_cap=rec.get('at_cap'), n=len(rec['hsps']))
        for d in (1, 2):
            for cl in ('C1', 'C2', 'C3', 'C4'):
                ms = [m for m in man[d]['controls'] if m['cls'] == cl]
                calls = [o['per_query'].get(m['qid'], {}).get('call', 'NOT_RUN') if m['status'] == 'ok' else 'UNMATCHED' for m in ms]
                n = len(ms); nn = sum(c == 'NOT_NOVEL' for c in calls); nv = sum(c == 'NOVEL' for c in calls)
                o['cls'][f"d{d}_{cl}"] = dict(n=n, not_novel=nn, novel=nv, near=sum(c == 'NEAR' for c in calls), not_run=sum(c in ('NOT_RUN', 'UNMATCHED') for c in calls),
                                              sens=nn / n if n else None, cp95_lower=clopper_pearson_lower(nn, n) if n else None)
        g, near_thr = True, True
        draws = (1,) if name == 'N2' else (1, 2)   # N2 is run on draw 1 only
        for d in draws:
            for cl, thr in (('C1', 30), ('C2', 28)):
                c = o['cls'][f"d{d}_{cl}"]
                if c['not_novel'] < thr: g = False
                if c['sens'] is None or c['sens'] < 0.80: near_thr = False
        s_ok = all(o['cls'][f"d{d}_C4"]['novel'] + o['cls'][f"d{d}_C4"]['near'] >= 0.95 * o['cls'][f"d{d}_C4"]['n'] for d in draws)
        o['G_pass'] = g; o['G_label'] = 'pass' if g else ('inconclusive (near threshold)' if near_thr else 'uninformative'); o['S_pass'] = s_ok
        cc = [o['per_query'].get(c, {}).get('call', 'NOT_RUN') for c in cand_ids]
        o['A_no_not_novel'] = sum(c in ('NOVEL', 'NEAR') for c in cc); o['A_near'] = sum(c == 'NEAR' for c in cc)
        o['A_not_novel_ids'] = [c for c, k in zip(cand_ids, cc) if k == 'NOT_NOVEL']; o['A_not_run'] = sum(c == 'NOT_RUN' for c in cc)
        out[name] = o
    json.dump(out, open(a.out, 'w'), indent=1, default=str)
    for n, o in out.items(): print(n, 'G', o['G_label'], 'S', o['S_pass'], 'A', o['A_no_not_novel'], '/32 near', o['A_near'], 'not_novel', o['A_not_novel_ids'])
def load_arm(name, p):
    d = json.load(open(p))
    if name in ('L1', 'L2'): return {q: dict(hsps=h) for q, h in d['hsps'].items()}
    out = {}   # N1/N2: p is a state file
    base = os.path.dirname(p)
    for it in d['items']:
        if it['status'] == 'done': out.update(parse_ncbi_json2(json.load(open(it['raw']))))
    return out

# ---------- dates (drift) ----------
def cmd_dates(a):
    import xml.etree.ElementTree as ET
    res = {}
    for acc in a.accs:
        time.sleep(0.5)
        try:
            ipg = http(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id={acc}&rettype=ipg&retmode=xml&tool=algo50-r05&email={EMAIL}")
            ids = sorted(set(re.findall(r'accver="([^"]+)"', ipg)) | {acc})[:40]
        except Exception as e: ids = [acc]
        dates = {}
        for i in ids:
            time.sleep(0.5)
            try:
                gb = http(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id={i}&rettype=gb&retmode=xml&tool=algo50-r05&email={EMAIL}")
                m = re.search(r'<GBSeq_create-date>([^<]+)', gb)
                if m: dates[i] = datetime.datetime.strptime(m.group(1), '%d-%b-%Y').date().isoformat()
            except Exception as e: dates[i] = f"error:{e}"
        ok = [v for v in dates.values() if not v.startswith('error')]
        res[acc] = dict(members=dates, earliest=min(ok) if ok else None)
    json.dump(res, open(a.out, 'w'), indent=1); print(json.dumps(res)[:600])

def cmd_udates(a):
    meta = load_meta(a.meta); res = {}
    for acc in a.accs:
        c, u, _ = meta.get(acc, (None, None, ''))
        res[acc] = dict(created=c, seq_update=u, date=max(x for x in (c, u) if x) if (c or u) else None)
    json.dump(res, open(a.out, 'w'), indent=1); print(res)

def main():
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('meta'); p.add_argument('--dat'); p.add_argument('--out')
    p = sp.add_parser('genctl'); p.add_argument('--cands'); p.add_argument('--sprot'); p.add_argument('--meta'); p.add_argument('--draw', type=int); p.add_argument('--outdir'); p.add_argument('--dat')
    for n in ('l1', 'l2', 'n1', 'n2'):
        p = sp.add_parser(n); p.add_argument('--qfa', nargs='+'); p.add_argument('--outdir'); p.add_argument('--sprot'); p.add_argument('--mmseqs'); p.add_argument('--ctl')
    p = sp.add_parser('score'); p.add_argument('--ctl'); p.add_argument('--cands'); p.add_argument('--arms', nargs='+'); p.add_argument('--out')
    p = sp.add_parser('udates'); p.add_argument('--accs', nargs='+'); p.add_argument('--meta'); p.add_argument('--out')
    p = sp.add_parser('dates'); p.add_argument('--accs', nargs='+'); p.add_argument('--out')
    a = ap.parse_args()
    {'meta': cmd_meta, 'genctl': cmd_genctl, 'l1': cmd_l1, 'l2': cmd_l2, 'score': cmd_score, 'dates': cmd_dates, 'udates': cmd_udates,
     'n1': lambda a: cmd_ncbi(a, 'N1'), 'n2': lambda a: cmd_ncbi(a, 'N2')}[a.cmd](a)
if __name__ == '__main__': main()

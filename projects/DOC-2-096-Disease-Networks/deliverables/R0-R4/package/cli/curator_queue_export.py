#!/usr/bin/env python3
"""Read-only curator-queue exporter for frozen DOC-2-096 R0-R4 outputs.

Selects frozen rows by explicit round/status fields and exports them in a
stable sorted order. Every exported row carries the source round, the frozen
claim status, the source artifact path, the source artifact SHA-256, and the
original row identifier. This tool does not score, rank, infer, merge evidence
across rounds, or change labels. It makes no network calls and writes nothing.
"""
import argparse, csv, hashlib, json, os, sys

ROUND_DIRS = {
 'R0': 'frozen/rounds/DOC-2-096-R0-negative-evidence-20260921.tar-ee188207/DOC-2-096-R0-negative-evidence',
 'R1': 'frozen/rounds/DOC-2-096-R1-temporal-20260921.tar-7285855e/DOC-2-096-R1-temporal',
 'R2': 'frozen/rounds/DOC-2-096-R2-archives-20260921.tar-b0e91108/DOC-2-096-R2-archives',
 'R3': 'frozen/rounds/DOC-2-096-R3-ranking-20260921.tar-d6826c64/DOC-2-096-R3-ranking',
 'R4': 'frozen/rounds/DOC-2-096-R4-competing-risks-20260921.tar-ed93bfa9/DOC-2-096-R4-competing-risks',
}
# Frozen claim statuses, quoted from each round's frozen README/report.
STATUS = {
 'R0': 'Locked-gate success, with bounded claim',
 'R1': 'CLEAN TEMPORAL-IDENTIFIABILITY STOP',
 'R2': 'LOCKED-GATE FAILURE',
 'R3': 'LOCKED RANKING GATE FAILURE',
 'R4': 'PREDICTIVE TRIAGE CLOSED; DESCRIPTIVE TOPOLOGY RETAINED',
}
# Frozen files each status label must appear in (custody check).
STATUS_SOURCE = {
 'R0': 'README.md', 'R1': 'README.md', 'R2': 'README.md', 'R3': 'README.md',
 'R4': 'report/FULL_TECHNICAL_REPORT.md',
}
# Exportable frozen CSV tables. id_fields name the original identifier
# columns; 'row' means the 1-based frozen file row number is the identifier.
TABLES = {
 'R0': {
  'source_replication':    {'path': 'results/source_replication.csv',    'id': ('source',), 'rows': 4},
  'stratified_instability':{'path': 'results/stratified_instability.csv','id': ('row',),    'rows': 88},
 },
 'R2': {
  'locked_temporal_metrics':{'path': 'results/locked_temporal_metrics.csv','id': ('transition','model'), 'rows': 6},
  'negative_controls':      {'path': 'results/negative_controls.csv',      'id': ('control',), 'rows': 2},
  'temporal_metrics':       {'path': 'results/temporal_metrics.csv',      'id': ('transition','model'), 'rows': 6},
 },
 'R4': {
  'competing_risk_metrics': {'path': 'results/competing_risk_metrics.csv', 'id': ('target','feature','split'), 'rows': 24},
 },
}
# Frozen gate/summary JSONs surfaced verbatim by `round-summary`.
SUMMARIES = {
 'R0': 'results/gate_decision.json',
 'R1': 'results/temporal_identifiability.json',
 'R2': 'results/gate_decision.json',
 'R3': 'results/ranking.json',
 'R4': 'results/gate.json',
}

def sha(path):
    with open(path, 'rb') as fh: return hashlib.sha256(fh.read()).hexdigest()

def rdir(root, rnd): return os.path.join(root, ROUND_DIRS[rnd])

def load_rows(root, rnd, table):
    spec = TABLES[rnd][table]
    p = os.path.join(rdir(root, rnd), spec['path'])
    with open(p, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    return p, spec, rows

def original_id(spec, row, idx):
    if spec['id'] == ('row',): return 'row%d' % idx
    return '|'.join(row.get(k, '') for k in spec['id'])

def resolve_round(args):
    if args.status is not None:
        hits = [r for r in sorted(STATUS) if STATUS[r] == args.status]
        if not hits:
            print('no frozen round carries status: %s' % args.status, file=sys.stderr); sys.exit(2)
        return hits[0]
    return args.round

def manifest_check(root):
    p = os.path.join(root, 'MANIFEST.sha256'); listed = {}; bad = []
    with open(p, encoding='utf-8') as f:
        for line in f:
            h, rel = line.rstrip('\n').split('  ', 1); listed[rel] = h
    for rel, h in listed.items():
        q = os.path.join(root, rel)
        if not os.path.isfile(q): bad.append('missing ' + rel); continue
        if sha(q) != h: bad.append('hash ' + rel)
    actual = []
    for dp, _, fs in os.walk(root):
        for n in fs:
            rel = os.path.relpath(os.path.join(dp, n), root)
            if rel != 'MANIFEST.sha256': actual.append(rel)
    extra = sorted(set(actual) - set(listed))
    if extra: bad.extend('unlisted ' + x for x in extra)
    return bad

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('verify'); sp.add_parser('rounds'); sp.add_parser('tables'); sp.add_parser('summary')
    p = sp.add_parser('round-summary'); p.add_argument('round', choices=sorted(ROUND_DIRS))
    p = sp.add_parser('export')
    p.add_argument('--round', choices=sorted(ROUND_DIRS))
    p.add_argument('--status', help='exact frozen claim status label; selects its round')
    p.add_argument('--table', required=True)
    p.add_argument('--format', choices=('tsv', 'json'), default='tsv')
    a = ap.parse_args(); root = os.path.abspath(a.root)

    if a.cmd == 'verify':
        bad = manifest_check(root); checks = []
        for rnd in sorted(TABLES):
            for tbl in sorted(TABLES[rnd]):
                _, spec, rows = load_rows(root, rnd, tbl)
                checks.append(('%s/%s' % (rnd, tbl), len(rows) == spec['rows'], len(rows), spec['rows']))
        for rnd in sorted(STATUS):
            spath = os.path.join(rdir(root, rnd), STATUS_SOURCE[rnd])
            ok = os.path.isfile(spath) and STATUS[rnd] in open(spath, encoding='utf-8').read()
            checks.append(('%s status label' % rnd, ok, 1 if ok else 0, 1))
        for side in ('figures/r0_source_instability.SOURCE.sha256',
                     'figures/r2_locked_transport.SOURCE.sha256',
                     'figures/r4_competing_risk_enrichment.SOURCE.sha256'):
            q = os.path.join(root, side); ok = False
            if os.path.isfile(q):
                h, rel = open(q, encoding='utf-8').read().split('  ', 1)
                t = os.path.join(root, rel.strip())
                ok = os.path.isfile(t) and sha(t) == h
            checks.append((side, ok, 1 if ok else 0, 1))
        print('MANIFEST ' + ('PASS' if not bad else 'FAIL'))
        for name, ok, got, want in checks:
            print('%s %s rows=%d expected=%d' % (name, 'PASS' if ok else 'FAIL', got, want))
        ok = not bad and all(c[1] for c in checks)
        print('AUDIT RESULT: ' + ('PASS' if ok else 'FAIL'))
        if bad:
            for x in bad: print('  ' + x)
        return 0 if ok else 1

    if a.cmd == 'rounds':
        for rnd in sorted(ROUND_DIRS):
            print('%s\t%s\t%s' % (rnd, STATUS[rnd], ROUND_DIRS[rnd].split('/')[-1]))
        return 0

    if a.cmd == 'tables':
        for rnd in sorted(TABLES):
            for tbl in sorted(TABLES[rnd]):
                spec = TABLES[rnd][tbl]
                p = os.path.join(rdir(root, rnd), spec['path'])
                print('%s\t%s\t%s\t%s' % (rnd, tbl, ROUND_DIRS[rnd] + '/' + spec['path'], sha(p)))
        return 0

    if a.cmd == 'summary':
        out = {'package': 'DOC-2-096-R0-R4', 'kind': 'read-only curator-queue exporter',
               'constraint': 'no scoring, ranking, inference, cross-round merge, or label change',
               'rounds': {}}
        for rnd in sorted(ROUND_DIRS):
            with open(os.path.join(rdir(root, rnd), SUMMARIES[rnd]), encoding='utf-8') as f:
                gate = json.load(f)
            out['rounds'][rnd] = {'claim_status': STATUS[rnd], 'frozen_summary': gate}
        print(json.dumps(out, sort_keys=True, indent=2)); return 0

    if a.cmd == 'round-summary':
        with open(os.path.join(rdir(root, a.round), SUMMARIES[a.round]), encoding='utf-8') as f:
            print(f.read().rstrip('\n'))
        return 0

    if a.cmd == 'export':
        rnd = resolve_round(a)
        if rnd not in TABLES or a.table not in TABLES[rnd]:
            print('no frozen exportable table %s for round %s' % (a.table, rnd), file=sys.stderr); return 2
        p, spec, rows = load_rows(root, rnd, a.table)
        rel = ROUND_DIRS[rnd] + '/' + spec['path']; src_sha = sha(p)
        keyed = [(original_id(spec, row, i + 1), row) for i, row in enumerate(rows)]
        keyed.sort(key=lambda kr: kr[0])
        meta = {'source_round': rnd, 'claim_status': STATUS[rnd],
                'source_artifact': rel, 'source_sha256': src_sha}
        if a.format == 'json':
            out = [dict(meta, original_id=oid, row=row) for oid, row in keyed]
            print(json.dumps(out, sort_keys=True, indent=2)); return 0
        fields = list(rows[0].keys())
        w = csv.writer(sys.stdout, delimiter='\t', lineterminator='\n')
        w.writerow(['source_round', 'claim_status', 'source_artifact', 'source_sha256', 'original_id'] + fields)
        for oid, row in keyed:
            w.writerow([rnd, STATUS[rnd], rel, src_sha, oid] + [row[k] for k in fields])
        return 0

if __name__ == '__main__': sys.exit(main())

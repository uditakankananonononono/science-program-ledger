#!/usr/bin/env python3
import hashlib, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CLI = os.path.join(ROOT, 'cli', 'curator_queue_export.py'); GOLD = os.path.join(HERE, 'golden')
def run(root, *args): return subprocess.run([sys.executable, CLI, '--root', root, *args], capture_output=True)
def main():
    fail = []
    goldens = [
        ('rounds', ('rounds',)),
        ('tables', ('tables',)),
        ('export_r0', ('export', '--round', 'R0', '--table', 'source_replication')),
        ('export_r2', ('export', '--round', 'R2', '--table', 'locked_temporal_metrics')),
        ('export_status', ('export', '--status', 'PREDICTIVE TRIAGE CLOSED; DESCRIPTIVE TOPOLOGY RETAINED', '--table', 'competing_risk_metrics')),
    ]
    for name, args in goldens:
        p = run(ROOT, *args); want = open(os.path.join(GOLD, name + '.txt'), 'rb').read()
        ok = p.returncode == 0 and p.stdout == want
        print('[%s] golden %s' % ('PASS' if ok else 'FAIL', name)); fail += [] if ok else [name]
    p = run(ROOT, 'verify'); ok = p.returncode == 0 and b'AUDIT RESULT: PASS' in p.stdout
    print('[%s] verify' % ('PASS' if ok else 'FAIL')); fail += [] if ok else ['verify']
    a = run(ROOT, 'export', '--round', 'R4', '--table', 'competing_risk_metrics').stdout
    b = run(ROOT, 'export', '--round', 'R4', '--table', 'competing_risk_metrics').stdout
    ok = a == b and hashlib.sha256(a).hexdigest() == open(os.path.join(GOLD, 'export_r4.sha256')).read().strip()
    print('[%s] deterministic full export' % ('PASS' if ok else 'FAIL')); fail += [] if ok else ['export']
    p = run(ROOT, 'export', '--round', 'R1', '--table', 'source_replication')
    ok = p.returncode == 2 and b'no frozen exportable table' in p.stderr
    print('[%s] no cross-round table invention' % ('PASS' if ok else 'FAIL')); fail += [] if ok else ['scope']
    tmp = tempfile.mkdtemp(prefix='doc2096-corrupt-')
    try:
        shutil.copytree(ROOT, os.path.join(tmp, 'p'))
        q = os.path.join(tmp, 'p', 'frozen', 'rounds', 'DOC-2-096-R2-archives-20260921.tar-b0e91108',
                         'DOC-2-096-R2-archives', 'results', 'negative_controls.csv')
        d = open(q, 'rb').read(); open(q, 'wb').write(d.replace(b'0.19095275590551186', b'0.19095275590551187', 1))
        p = run(os.path.join(tmp, 'p'), 'verify')
        ok = p.returncode == 1 and b'AUDIT RESULT: FAIL' in p.stdout
        print('[%s] corruption detected' % ('PASS' if ok else 'FAIL')); fail += [] if ok else ['corruption']
    finally: shutil.rmtree(tmp)
    print('ALL TESTS PASS' if not fail else 'TESTS FAILED: ' + ', '.join(fail)); return bool(fail)
if __name__ == '__main__': sys.exit(main())

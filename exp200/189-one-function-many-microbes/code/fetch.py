import subprocess, random, time, os, re
random.seed(0)
def get(u): return subprocess.run(['curl','-s','--max-time','60',u],capture_output=True,text=True).stdout
L=open('data/genome_list.tsv').read()
rows=[l.split('\t') for l in L.strip().split('\n') if l.startswith('T')]
cand=random.sample(rows,900); info={}
for i in range(0,900,10):
    b=cand[i:i+10]; txt=get('https://rest.kegg.jp/get/'+'+'.join('gn:'+r[0] for r in b))
    for ent in txt.split('///'):
        m=re.search(r'^ENTRY\s+(T\d+)',ent,re.M); lin=re.search(r'^\s*LINEAGE\s+(.+)$',ent,re.M); nm=re.search(r'^ORG_CODE\s+(\S+)',ent,re.M)
        if m and lin and nm: info[m.group(1)]=(nm.group(1).strip(),lin.group(1).strip())
    time.sleep(0.2)
open('data/lineages.tsv','w').write(''.join(f'{t}\t{c}\t{l}\n' for t,(c,l) in info.items()))
pro=[(t,c,l) for t,(c,l) in info.items() if l.split(';')[0].strip() in ('Bacteria','Archaea')]
bygenus={}
for t,c,l in pro: bygenus.setdefault(l.split(';')[-2].strip(),[]).append((t,c,l))
pick=[random.choice(v) for k,v in sorted(bygenus.items())]; pick=random.sample(pick,min(150,len(pick)))
os.makedirs('data/modules',exist_ok=True)
open('data/sample.tsv','w').write(''.join(f'{t}\t{c}\t{l}\n' for t,c,l in pick))
for t,c,l in pick:
    open(f'data/modules/{c}.tsv','w').write(get(f'https://rest.kegg.jp/link/module/{c}')); time.sleep(0.15)
print('prok',len(pro),'genera',len(bygenus),'picked',len(pick))

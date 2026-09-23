import urllib.request, json, sys, time
fams="PF00089 PF00069 PF00106 PF00561 PF00067 PF00071 PF00128 PF00085 PF00112 PF00026 PF00501 PF00378 PF00300 PF00248 PF00107 PF00144 PF00155 PF00202 PF00255 PF00462".split()
for f in fams:
    url=f"https://rest.uniprot.org/uniprotkb/search?query=reviewed:true+AND+xref:pfam-{f}&fields=accession,sequence,ft_act_site,ft_binding&format=json&size=400"
    for t in range(3):
        try:
            d=urllib.request.urlopen(url,timeout=60).read(); break
        except Exception as e: time.sleep(3)
    open(f'data/{f}.json','wb').write(d); print(f,len(json.loads(d)['results']))
